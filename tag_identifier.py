from google_search_scraper import GoogleSearchTagGenerator
import stanza
from nltk.tokenize import word_tokenize
import string
from utils.helper_class import HelperClass
import logging
import logging.handlers
import os
import pandas
from multiprocessing import Pool
from utils.decorators import timeit
PARENT_DIR = os.getcwd()

logger = logging.getLogger(__name__)


class TagIdentifier:

    def __init__(self, store_ml_data: bool = True):

        self.parent_dir = PARENT_DIR
        self.reference_dir = r"%s\assets\reference_dict" % PARENT_DIR
        self.store_ml_data = store_ml_data


        self.helper = HelperClass()
        self.google_search_scraper = GoogleSearchTagGenerator()
        self.sports_leagues = ["nfl", "nhl", "nba", "football", "mlb", "ncaab", "ncaafb"]
        self.sports_with_references = ["american_football", "basketball", "football", "hockey", "baseball"]
        # TODO handle football/soccer vs american football
        self.all_sports = ["american_football", "basketball", "football", "hockey", "baseball", "tennis",
                           "swimming", "track", "olympics", "lacrosse", "rugby", "soccer"]

        self.sports_team_dict = self.set_team_dict()
        self.sports_player_dict = self.set_player_dict()
        self.sports_terms_dict = self.set_sports_terms_dict()

    def setup_logger(self):
        pass


    def set_team_dict(self):
        """
        Set team dictionary for class
        """
        tmp_dict = {}
        for league in self.sports_leagues:
            # Dont have football team info (soccer)
            if league == "football":
                pass
            else:
                tmp_dict[league] = self.helper.read_json_file(file_path=self.reference_dir,
                                                              file_name=f"{league}_team_dict.json")
        return tmp_dict

    def set_player_dict(self):
        tmp_dict = {}
        for league in self.sports_leagues:
            # Dont have football (soccer) , ncaab, ncaafb player info
            if league in ["football", "ncaab", "ncaafb"]:
                pass
            else:
                tmp_dict[league] = self.helper.read_json_file(file_path=self.reference_dir,
                                                              file_name=f"{league}_player_dict.json")
        return tmp_dict

    def set_sports_terms_dict(self):
        tmp_dict = {}
        for sport in self.sports_with_references:
            tmp_dict[sport] = self.helper.read_pickled_file(file_path=self.reference_dir,
                                                            file_name=f"{sport}_terms.data")
        return tmp_dict

    def generate_tags(self, summary_list: list):
        """
        :param summary_list: list of topics identified for each podcase
        :return: a list of dictionaries, each dictionary is a tag
        Entinty Recognition: https://www.nltk.org/book/ch07.html
        """

        logging.info("Starting Generate Tags")
        podcast_tags = []


        for index, summary in enumerate(summary_list):

            summary_tag_list = []

            # Google Results is used after iterating through a summary if there are no valid tags, this is the
            # Cumulative string for the entire summary
            google_search_results: str = ''
            untaged_words: list = []

            token_dict_list = self.helper.get_token_dict_from_nlp(summary)
            print("Token DIct List", token_dict_list)
            logger.info(f"Token Dict List for: {summary} : {token_dict_list}")
            # NLP Couldnt find any clear tokens
            if len(token_dict_list) == 0:
                token_dict_list = self.helper.get_token_dict_manual(summary)
                logger.info(f"Manual Dict List for: {summary} : {token_dict_list}")

            for token in token_dict_list:

                tmp_tag_list: list = []
                tmp_tag_list += self.get_tags_using_dict(token)

                if len(tmp_tag_list) == 0:
                    # Creating a list of untaged words that will later be google searched
                    untaged_words.append(token["text"])

                else:
                    logger.info(f"Adding tags to {summary}: {tmp_tag_list}")
                    summary_tag_list += tmp_tag_list

            if len(untaged_words) != 0:
                logging.info("Untaged Words: %s" % untaged_words)
                summary_tag_list += self.get_tags_from_unknown_words(untaged_words, self.store_ml_data)


            summary_tag_obj = {"Summary": summary, "Tags": summary_tag_list}
            logger.info(f"Appending to Final Podcast Summary: {summary_tag_obj}")

            podcast_tags.append(summary_tag_obj)
            logger.info(f"Adding {summary_tag_obj} to Podcast Tags")

        logger.info(f"Completed Anlysis of {summary_list} : {podcast_tags}")
        return podcast_tags


    def get_tags_using_dict(self, token_dict):
        """
        :param token_dict: Dictionary with token information
        :return: a list of tags
        ORG: Organization
        PERSON: Person
        GPE: Geo-political Entities (Florida, Auburn.. etc.)
        """
        # Tampa Bay Buccaneers is a person? {'text': "Tampa Bay Buccaneers'", 'type': 'PERSON', 'start_char': 10, 'end_char': 31}

        tmp_tag_dict_list: list = []
        logger.debug(f"Get Tags Using Dict: {token_dict}")

        # Todo how to handle Tampa Bay Buccaneers being considered a person
        # TODO identify which sport they are actually talking about i.e. Auburn vs. Florida (Which sports basketball? football?)
        if token_dict["type"] in ["ORG", "PERSON", "GPE"]:
            tmp_tag_dict_list += self.get_team_tags(token_dict)
            tmp_tag_dict_list += self.get_person_tags(token_dict)

        # If League is mentioned in a tokenized word i.e ESPN NBA, this would tag for NBA
        matching = [league for league in self.sports_leagues if league in token_dict['text'].lower()]
        if matching:
            tmp_tag_dict_list.append({"type": "league", "value": matching[0]})

        if len(tmp_tag_dict_list) == 0:
            tmp_tag_dict_list += self.get_sports_terms_tag(token_dict)

        logger.info(f"get_tags_using_dict response: {tmp_tag_dict_list}")
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
        logger.debug(f"Team Name: {team_name}, Team Name no Punc: {team_name_no_punc}")
        for league in self.sports_team_dict.keys():
            # TODO Handle if there are multiple teams with the same name
            if team_name in self.sports_team_dict[league]:
                logger.debug(f"Team Exists in {league}")
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
                logger.debug(f"Team Exists in {league}")
                org_tags.append({"type": "team", "value": self.sports_player_dict[league][player_name]})
                org_tags.append({"type": "person", "value": player_name})
                org_tags.append({"type": "league", "value": league})
                break

            if player_name_no_punc in self.sports_player_dict[league]:
                logger.debug(f"Team Exists in {league}")
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
                logger.debug(f"Term exists in {sport}")
                org_tags.append({"type": "sport", "value": sport})
                break
        return org_tags


    def get_tags_from_unknown_words(self, untaged_words: list, store_ml_data: bool):
        """
        :param untaged_words: list of untagged words
        :return:
        google_search_tags -- the tags determined by the google search results
        ml_info = machine learning reference data
        """
        ml_dict: dict = {}
        google_search_tags = []

        for index , word in enumerate(untaged_words):
            # TODO Parallelize get_google_search_results
            word_search_results: str = self.google_search_scraper.get_google_search_results(word)
            word_search_tokens: dict = self.helper.get_token_dict_from_nlp(word_search_results)
            for token in word_search_tokens:
                tag_list = self.get_tags_using_dict(token)
                ml_dict = self.helper.append_to_existing_dict(word, ml_dict, tag_list)

                google_search_tags += tag_list

        if store_ml_data is True:
            self.helper.add_to_ml_data(ml_dict,
                                   file_path=r"%s\data\tag_generation_pending_validation" % self.parent_dir,
                                   file_name="tag_token_pending_validation.json"
                                   )

        return google_search_tags

