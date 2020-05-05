from nltk.tokenize import word_tokenize
from typing import *
import string
import logging
import logging.handlers
import os

from src.main.utils.helper_class import HelperClass
from src.main.utils.decorators import debug

PARENT_DIR = os.getcwd()
logger = logging.getLogger(__name__)


class TagIdentifier:

    def __init__(self, store_ml_data: bool = True):
        self.store_ml_data = store_ml_data
        self.helper = HelperClass()

    @debug
    def generate_tags_on_genre(self, description: str, genre: str) -> List[Dict] :
        if genre == "sports":
            sports_tags = self.generate_sports_tags(description)
            return self.helper.filter_duplicates_from_dict_list(sports_tags, "value")
        else:
            general_tags = self.generate_tags_non_specific(description)
            return self.helper.filter_duplicates_from_dict_list(general_tags, "value")

    @debug
    def generate_sports_tags(self, description: str):

        description_tags: List[Dict] = []

        key_words = self.helper.get_key_word_dict(description)

        description_tags += self.check_sport_and_league(description)

        for word in key_words:

            if word['text'].lower() in self.helper.SPORTS_LEAGUES:
                # Handling sports leagues in other method skipping this
                continue
            word_tags = self.get_tags_using_sports_dict(word)
            if len(word_tags) == 0:
                google_results = self.helper.get_google_search_results(word['text'])
                google_key_words = self.helper.get_key_word_dict(google_results)
                for google_word in google_key_words:
                    google_word_tags = self.get_tags_using_sports_dict(google_word)
                    description_tags += google_word_tags
            else:
                description_tags += word_tags
        return description_tags



    def generate_tags_non_specific(self, description) -> List[Dict]:
        return []

    @debug
    def check_sport_and_league(self, description: str) -> List[Dict]:
        """
        If League is mentioned in a tokenized word i.e ESPN NBA, this would tag for NBA
        Done before any words are tokenized for a quick check
        :param description: String/Text of Summary
        :return: List of tags
        """

        sport_and_league_tags: list = []
        matching_league = [league for league in self.helper.SPORTS_LEAGUES if league in description.lower()]
        if matching_league:
            for index, value in enumerate(matching_league):
                sport_and_league_tags.append({"type": "league", "value": value})

        matching_sport = [sport for sport in self.helper.ALL_SPORTS if sport in description.lower()]
        if matching_sport:
            for index, value in enumerate(matching_sport):
                sport_and_league_tags.append({"type": "sport", "value": value})

        return sport_and_league_tags

    def get_person_tags(self, toke_dict: dict):
        """
        # Pass in token and if a full name adding this tag
        :param toke_dict: Token Dict
        :return: Tags that are for a specific person
        """

        # Getting list of names to see length
        person_tags = []
        name: str = toke_dict['text']
        name_length = len(name.split())
        if name_length > 1:
            # Greater than 1 suggesting its a full name
            person_tags.append({"type": "person", "value": name})

        return person_tags

    @debug
    def get_tags_using_sports_dict(self, key_word: Dict)-> List[Dict]:

        key_word_tags: list = []

        key_word_tags += self.get_person_tags(key_word)
        key_word_tags += self.get_team_tags(key_word)
        key_word_tags += self.get_player_or_coach_tags(key_word, self.helper.sports_player_dict)
        if len(key_word_tags) == 0:
            key_word_tags += self.get_individual_sports_tags(key_word, self.helper.individual_sports_dict)
        if len(key_word_tags) == 0:
            key_word_tags += self.get_nickname_tags(key_word, self.helper.sports_nickname_dict)
        # TODO Dont think sports terms is worth it
        if len(key_word_tags) == 0:
            key_word_tags += self.get_sports_terms_tag(key_word)

        return key_word_tags

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
        if token_dict["type"] == "PERSON":
            tmp_tag_dict_list += self.get_person_tags(token_dict)

        # Todo how to handle Tampa Bay Buccaneers being considered a person
        # TODO identify which sport they are actually talking about i.e. Auburn vs. Florida (Which sports basketball? football?)
        if token_dict["type"] in ["ORG", "PERSON", "GPE"]:
            tmp_tag_dict_list += self.get_team_tags(token_dict)
            tmp_tag_dict_list += self.get_player_or_coach_tags(token_dict, self.helper.sports_player_dict)

            if len(tmp_tag_dict_list) == 0:
                tmp_tag_dict_list += self.get_individual_sports_tags(token_dict, self.helper.individual_sports_dict)

            if len(tmp_tag_dict_list) == 0:
                tmp_tag_dict_list += self.get_player_or_coach_tags(token_dict, self.helper.sports_coach_dict)

        if len(tmp_tag_dict_list) == 0:
            tmp_tag_dict_list += self.get_nickname_tags(token_dict, self.helper.sports_nickname_dict)

        if len(tmp_tag_dict_list) == 0:
            tmp_tag_dict_list += self.get_sports_terms_tag(token_dict)

        logger.info(f"get_tags_using_dict response: {tmp_tag_dict_list}")
        return tmp_tag_dict_list

    def get_team_tags(self, token_dict: dict):

        org_tags = []
        team_name = token_dict["text"]
        # Sometime names have punctuation that will screw it up, checking if it without punctuation is contained
        # IN List
        team_name_no_punc = self.helper.remove_punctuation_from_text(team_name)
        logger.debug(f"Team Name: {team_name}, Team Name no Punc: {team_name_no_punc}")
        for league in self.helper.sports_team_dict.keys():
            # TODO Handle if there are multiple teams with the same name
            if team_name in self.helper.sports_team_dict[league]:
                logger.debug(f"Team Exists in {league}")
                org_tags.append({"type": "team", "value": self.helper.sports_team_dict[league][team_name]})
                org_tags.append({"type": "league", "value": league})
                break
            if team_name_no_punc in self.helper.sports_team_dict[league]:
                org_tags.append({"type": "team", "value": self.helper.sports_team_dict[league][team_name_no_punc]})
                org_tags.append({"type": "league", "value": league})
                break
        return org_tags

    def get_player_or_coach_tags(self, token_dict: dict, reference_dict: dict):
        """
        Used to check if person is either a player or coach
        :param token_dict:
        :param reference_dict:
        :return:
        """
        org_tags = []
        name = token_dict["text"]
        # Sometime names have punctuation that will screw it up, checking if it without punctuation is contained
        # IN List
        name_no_punc = self.helper.remove_punctuation_from_text(name)
        for league in reference_dict.keys():

            if name in reference_dict[league]:
                logger.debug(f"Coach Exists in {league}")
                org_tags.append({"type": "team", "value": reference_dict[league][name]})
                # Todo Delete Belo
                # Removing Name Appended because tags will be added if it is a full Name
                # org_tags.append({"type": "person", "value": name})
                org_tags.append({"type": "league", "value": league})
                break

            if name_no_punc in reference_dict[league]:
                logger.debug(f"Coach Exists in {league}")
                org_tags.append({"type": "team", "value": reference_dict[league][name_no_punc]})
                # Todo Delete Belo
                # Removing Name Appended because tags will be added if it is a full Name
                # org_tags.append({"type": "person", "value": name_no_punc})
                org_tags.append({"type": "league", "value": league})
                break

        return org_tags

    def get_nickname_tags(self, token_dict: dict, nickname_dict: dict):
        """
        :param token_dict:
        :param nickname_dict:
        :return:
        """
        org_tags = []
        name = token_dict["text"]
        # Sometime names have punctuation that will screw it up, checking if it without punctuation is contained
        # IN List
        name_no_punc = self.helper.remove_punctuation_from_text(name)
        for league in nickname_dict.keys():

            if name in nickname_dict[league]:
                logger.debug(f"Coach Exists in {league}")

                # Todo Delete Belo
                # Removing Name Appended because tags will be added if it is a full Name
                # org_tags.append({"type": "person", "value": name})

                org_tags.append({"type": "league", "value": league})
                if name in self.helper.sports_player_dict[league]:
                    org_tags.append({"type": "team", "value": self.helper.sports_player_dict[league][name]})
                break

            if name_no_punc in nickname_dict[league]:
                logger.debug(f"Coach Exists in {league}")
                # Todo Delete Belo
                # Removing Name Appended because tags will be added if it is a full Name
                # org_tags.append({"type": "person", "value": name_no_punc})
                org_tags.append({"type": "league", "value": league})
                if name in self.helper.sports_player_dict[league]:
                    org_tags.append({"type": "team", "value": self.helper.sports_player_dict[league][name]})
                break
        return org_tags

    def get_individual_sports_tags(self, token_dict: dict, individual_sports_dict: dict):

        individual_sports_tags = []
        person = token_dict['text']
        for sport in individual_sports_dict.keys():
            if person in self.helper.individual_sports_dict[sport]:
                individual_sports_tags.append({"type": "person", "value": person})
                individual_sports_tags.append({"type": "sport", "value": sport})

        return individual_sports_tags

    def get_sports_terms_tag(self, token_dict: dict):

        sports_terms_tags = []
        for sport in self.helper.sports_terms_dict.keys():
            # TODO Handle if there are multiple teams with the same name
            # Todo Handle Case Sensitive
            if token_dict["text"] in self.helper.sports_terms_dict[sport]:
                logger.debug(f"Term exists in {sport}")
                sports_terms_tags.append({"type": "sport", "value": sport})
                break
        return sports_terms_tags
