from google_search_term_identifier import GoogleSearchClass
import pickle
import json
import stanza
from nltk.tokenize import word_tokenize
import string
from helper_class import HelperClass
import logging
import logging.handlers


class GenerateTags(GoogleSearchClass):

    def __init__(self):
        self.tag_logger = logging.getLogger("Tag_Logger")
        self.helper = HelperClass()

        # TODO FIX path
        self.reference_dir = r"C:\Users\runni_000\PycharmProjects\podcastProject\assets\reference_dict"
        self.sports_leagues = ["nfl", "nhl", "nba", "football", "mlb", "ncaab", "ncaafb"]
        self.sports = ["american_football", "basketball", "football", "hockey", "baseball"]

        self.sports_team_dict = self.set_team_dict()
        self.sports_player_dict = self.set_player_dict()
        self.sports_terms_dict = self.set_sports_terms_dict()

    def set_team_dict(self):
        """
        Set team dictionary for class
        """
        tmp_dict = {}
        for league in self.sports_leagues:
            # Dont have football team info
            if league == "football":
                pass
            else:
                tmp_dict[league] = self.helper.read_json_file(file_path=self.reference_dir,
                                                              file_name=f"{league}_team_dict.json")
        return tmp_dict

    def set_player_dict(self):
        tmp_dict = {}
        for league in self.sports_leagues:
            # Dont have football team info
            if league in ["football", "ncaab", "ncaafb"]:
                pass
            else:
                tmp_dict[league] = self.helper.read_json_file(file_path=self.reference_dir,
                                                              file_name=f"{league}_player_dict.json")
        return tmp_dict

    def set_sports_terms_dict(self):
        tmp_dict = {}
        for sport in self.sports:
            tmp_dict[sport] = self.helper.read_pickled_file(file_path=self.reference_dir,
                                                            file_name=f"{sport}_terms.data")
        return tmp_dict

    def generate_tags(self, summary_list: list):
        """
        :param summary_list: list of topics identified for each podcase
        :return: a list of dictionaries, each dictionary is a tag
        Entinty Recognition: https://www.nltk.org/book/ch07.html
        """
        podcast_tags = []
        # TODO Move back to __init__ , moved for quicker testing
        self.nlp = stanza.Pipeline('en')  # This sets up a default neural pipeline in English

        for index, summary in enumerate(summary_list):

            summary_tag_list = []

            # Google Results is used after iterating through a summary if there are no valid tags, this is the
            # Cumulative string for the entire summary
            google_results: str = ''

            token_dict_list = self.get_token_dict(summary)
            self.tag_logger.info(f"Token Dict List for: {summary} :", token_dict_list)
            # NLP Couldnt find any clear tokens
            if len(token_dict_list) == 0:
                token_dict_list = self.get_token_dict_manual(summary)
                self.tag_logger.info(f"Manual Dict List for: {summary} :", token_dict_list)

            for token in token_dict_list:

                tmp_tag_list: list = []
                tmp_tag_list += self.get_tags_using_dict(token)

                if len(tmp_tag_list) == 0:
                    # Convert Tag using google search
                    google_results += self.get_google_search_results(token["text"])
                    self.tag_logger.info(f"Google Search for: {token['text']} results:", google_results)
                else:
                    self.tag_logger.info(f"Adding tags to {summary}:", tmp_tag_list)
                    summary_tag_list += tmp_tag_list

            # If google was required
            if len(google_results) != 0:

                token_dict_google_list = self.get_token_dict(google_results)
                self.tag_logger.info(f"Tokenized Google Results: {token_dict_google_list}")

                for token in token_dict_google_list:
                    tmp_tag_list: list = []
                    tmp_tag_list += self.get_tags_using_dict(token)
                    summary_tag_list += tmp_tag_list

            summary_tag_obj = {"Summary": summary, "Tags": summary_tag_list}
            self.tag_logger.info(f"Appending to Final Podcast Summary: {summary_tag_obj}")
            podcast_tags.append(summary_tag_obj)

        return podcast_tags

    def get_token_dict(self, summary: str):
        """
        Take a summary provided from a podcast and return a tokenized dictionary
        :param summary: A list of words in string format
        :return: tokenized dictionary
        """
        token_span_list = self.nlp(summary).entities
        token_dict_list = self.helper.convert_span_list_to_dict_list(token_span_list)
        return token_dict_list

    def get_tags_using_dict(self, token_dict):
        """
        :param token_dict: Dictionary with token information
        :return: a list of tags
        """
        # Tampa Bay Buccaneers is a person? {'text': "Tampa Bay Buccaneers'", 'type': 'PERSON', 'start_char': 10, 'end_char': 31}

        tmp_tag_dict_list: list = []
        print("Get Tags Using Dict", token_dict)

        # Todo how to handle Tampa Bay Buccaneers being considered a person
        if token_dict["type"] == "ORG" or token_dict["type"] == "PERSON":
            tmp_tag_dict_list += self.get_team_tags(token_dict)
            tmp_tag_dict_list += self.get_person_tags(token_dict)
        else:
            tmp_tag_dict_list += self.get_sports_terms_tag(token_dict)

        self.tag_logger.info("get_tags_using_dict response", tmp_tag_dict_list)
        return tmp_tag_dict_list

    def get_token_dict_manual(self, summary: str):
        """
        This is used to determine the tokens without using standford nlp
        :param summary: Summary
        :return: dict
        """
        # Tokenizing Data, breaks up into words/ phrases
        token_dict_list = []
        token_list = word_tokenize(summary)
        # Removing Stop words and punctuation from data
        clean_data = [word for word in token_list if
                      not word in self.helper.eng_stop_words and not word in string.punctuation]

        for word in clean_data:
            token_dict_list.append({"text": word, "type": "UNKNOWN"})

        return token_dict_list

    def get_team_tags(self, token_dict: object):

        org_tags = []
        team_name = token_dict["text"]
        # Sometime names have punctuation that will screw it up, checking if it without punctuation is contained
        # IN List
        team_name_no_punc = self.helper.remove_punctuation_from_text(team_name)
        print("Tame Name", team_name, team_name_no_punc)
        for league in self.sports_team_dict.keys():
            # TODO Handle if there are multiple teams with the same name
            if team_name in self.sports_team_dict[league]:
                print(f"Team Exists in {league}")
                org_tags.append({"type": "team", "value": self.sports_team_dict[league][team_name]})
                org_tags.append({"type": "league", "value": league})
                break
            if team_name_no_punc in self.sports_team_dict[league]:
                org_tags.append({"type": "team", "value": self.sports_team_dict[league][team_name_no_punc]})
                org_tags.append({"type": "league", "value": league})
                break
        return org_tags

    def get_person_tags(self, token_dict: object):

        org_tags = []
        player_name = token_dict["text"]
        # Sometime names have punctuation that will screw it up, checking if it without punctuation is contained
        # IN List
        player_name_no_punc = self.helper.remove_punctuation_from_text(player_name)
        for league in self.sports_player_dict.keys():

            if player_name in self.sports_player_dict[league]:
                print(f"Team Exists in {league}")
                org_tags.append({"type": "team", "value": self.sports_player_dict[league][player_name]})
                org_tags.append({"type": "person", "value": player_name})
                org_tags.append({"type": "league", "value": league})
                break

            if player_name_no_punc in self.sports_player_dict[league]:
                print(f"Team Exists in {league}")
                org_tags.append({"type": "team", "value": self.sports_player_dict[league][player_name_no_punc]})
                org_tags.append({"type": "person", "value": player_name_no_punc})
                org_tags.append({"type": "league", "value": league})
                break

        return org_tags

    def get_sports_terms_tag(self, token_dict: object):

        org_tags = []
        for sport in self.sports_terms_dict.keys():
            # TODO Handle if there are multiple teams with the same name
            # Todo Handle Case Sensitive
            if token_dict["text"] in self.sports_terms_dict[sport]:
                print(f"Term exists in {sport}")
                org_tags.append({"type": "sport", "value": sport})
                break
        return org_tags


if __name__ == "__main__":

    generate_tags = GenerateTags()
# results = x.generate_tags(["TB12 declining?"])
    results = generate_tags.generate_tags(["Cowboys lose Browns bounce back",
                           "Bucs win",
                           "TB12 declining?",
                           "Burfict suspended"])

    r_2 = generate_tags.generate_tags(["Bucs win",
                       "TB12 declining?",
                       "Burfict suspended",
                       "Pick ems Week 5",
                       "Clemson escapes",
                       "Auburn vs Florida",
                       "ESPN NBA top 10",
                       "Breakout players",
                       "CA Pass bill for college players",
                       "Baseball update"])

    print("Final Results",results)
    print("Final Reulsts ",r_2)
