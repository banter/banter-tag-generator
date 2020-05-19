import logging.handlers
import os
from typing import *
from src.main.tagging_algos.tagging_base_handler import TaggingBaseHandler
from src.main.utils.decorators import debug
from src.main.tagging_algos.tagging_enums.sports_tag_types import SportsTagTypes as TagType
from src.main.tagging_algos.tagging_enums.confidence_levels import ConfidenceLevels
from src.main.models.tag_model import TagModel, NLPEntityModel

PARENT_DIR = os.getcwd()
logger = logging.getLogger(__name__)


class TaggingSportsHandler(TaggingBaseHandler):

    def get_sports_tags(self, description: str) -> List[Dict[str, str]]:
        sports_tags = self.generate_sports_tags(description)
        return self.util.remove_duplicates_from_dict_list_based_on_key(sports_tags, "value")

    @debug
    def generate_sports_tags(self, description: str) -> List[Dict[str, str]]:

        description_tags: List[TagModel] = []
        location_entities: List[NLPEntityModel] = []
        key_words = self.util.get_key_word_dict(description)
        description_tags += self.check_sport_and_league(description)

        for word in key_words:
            if word['text'].lower() in self.util.sports_leagues:
                # Handling sports leagues in other method skipping this
                continue
            word_tags = self.get_tags_using_sports_dict(word)
            if len(word_tags) == 0:
                word_tags += self.handle_untagged_key_word(word)

            if len(word_tags) == 0:
                # Checking if it is an untagged location, if it is will use later
                if self.util.is_token_specific_type(word, "GPE"):
                    location_entities.append(word)
            description_tags += word_tags

        # If there are untagged location tags, going to check if there is any
        # Reference to a sports league. This way we can use this as context for the discussion
        if len(location_entities) != 0:
            description_tags += self.get_tags_using_location(location_entities, description_tags)

        return description_tags

    @debug
    def check_sport_and_league(self, description: str) -> List[Dict]:
        """
        If League is mentioned in a tokenized word i.e ESPN NBA, this would tag for NBA
        Done before any words are tokenized for a quick check
        :param description: String/Text of Summary
        :return: List of tags
        """
        method_confidence = ConfidenceLevels.MEDIUM.value
        sport_and_league_tags: list = []
        matching_league = [league for league in self.util.sports_leagues if league in description.lower()]
        if matching_league:
            for index, value in enumerate(matching_league):
                sport_and_league_tags.append({"type": TagType.LEAGUE.value, "value": value, "confidence": method_confidence})

        matching_sport = [sport for sport in self.util.all_sports if sport in description.lower()]
        if matching_sport:
            for index, value in enumerate(matching_sport):
                sport_and_league_tags.append({"type": TagType.SPORT.value, "value": value, "confidence": method_confidence})

        return sport_and_league_tags

    @debug
    def get_tags_using_sports_dict(self, key_word: Dict) -> List[TagModel]:
        key_word_tags: list = []
        key_word_tags += self.get_team_and_league_tags_on_team(key_word)
        key_word_tags += self.get_team_player_league_tags_on_player_or_coach(key_word, self.util.sports_player_dict)
        if len(key_word_tags) == 0:
            key_word_tags += self.get_team_player_league_tags_on_player_or_coach(key_word, self.util.sports_coach_dict)
        if len(key_word_tags) == 0:
            key_word_tags += self.get_sport_and_person_tags_on_non_team_sport(key_word,
                                                                              self.util.individual_sports_dict)
        if len(key_word_tags) == 0:
            key_word_tags += self.get_nickname_tags(key_word, self.util.sports_nickname_dict)
        # TODO Dont think sports terms is worth it
        if len(key_word_tags) == 0:
            key_word_tags += self.get_sports_terms_tag(key_word)

        return key_word_tags

    def get_team_and_league_tags_on_team(self, token_dict: dict):
        method_confidence = ConfidenceLevels.HIGH.value
        org_tags = []
        team_name = token_dict["text"]
        # Sometime names have punctuation that will screw it up, checking if it without punctuation is contained
        # IN List
        team_name_no_punc = self.util.remove_punctuation_from_text(team_name)
        logger.debug(f"Team Name: {team_name}, Team Name no Punc: {team_name_no_punc}")
        for league in self.util.sports_team_dict.keys():
            # TODO Handle if there are multiple teams with the same name
            if team_name in self.util.sports_team_dict[league]:
                logger.debug(f"Team Exists in {league}")
                org_tags.append({"type": TagType.TEAM.value, "value": self.util.sports_team_dict[league][team_name], "confidence": method_confidence})
                org_tags.append({"type": TagType.LEAGUE.value, "value": league, "confidence": method_confidence})
                break
            if team_name_no_punc in self.util.sports_team_dict[league]:
                org_tags.append({"type": TagType.TEAM.value, "value": self.util.sports_team_dict[league][team_name_no_punc], "confidence": method_confidence})
                org_tags.append({"type": TagType.LEAGUE.value, "value": league, "confidence": method_confidence})
                break
        return org_tags

    def get_team_player_league_tags_on_player_or_coach(self, token_dict: dict, reference_dict: dict):
        """
        Used to check if person is either a player or coach
        :param token_dict:
        :param reference_dict:
        :return:
        """
        method_confidence = ConfidenceLevels.HIGH.value
        org_tags = []
        name = token_dict["text"]
        # Sometime names have punctuation that will screw it up, checking if it without punctuation is contained
        # IN List
        name_no_punc = self.util.remove_punctuation_from_text(name)
        for league in reference_dict.keys():

            if name in reference_dict[league]:
                logger.debug(f"Coach Exists in {league}")
                org_tags.append({"type": TagType.TEAM.value, "value": reference_dict[league][name], "confidence": method_confidence})
                org_tags.append({"type": TagType.PERSON.value, "value": name, "confidence": method_confidence})
                org_tags.append({"type": TagType.LEAGUE.value, "value": league, "confidence": method_confidence})
                break

            if name_no_punc in reference_dict[league]:
                logger.debug(f"Coach Exists in {league}")
                org_tags.append({"type": TagType.TEAM.value, "value": reference_dict[league][name_no_punc], "confidence": method_confidence})
                org_tags.append({"type": TagType.PERSON.value, "value": name_no_punc, "confidence": method_confidence})
                org_tags.append({"type": TagType.LEAGUE.value, "value": league, "confidence": method_confidence})
                break

        return org_tags

    def get_nickname_tags(self, token_dict: dict, nickname_dict: dict):
        """
        :param token_dict:
        :param nickname_dict:
        :return:
        """
        method_confidence = ConfidenceLevels.MEDIUM.value
        org_tags = []
        name = token_dict["text"]
        # Sometime names have punctuation that will screw it up, checking if it without punctuation is contained
        # IN List
        name_no_punc = self.util.remove_punctuation_from_text(name)
        for league in nickname_dict.keys():

            if name in nickname_dict[league]:
                org_tags.append({"type": TagType.LEAGUE.value, "value": league, "confidence": method_confidence})
                if name in self.util.sports_player_dict[league]:
                    org_tags.append({"type": TagType.TEAM.value, "value": self.util.sports_player_dict[league][name], "confidence": method_confidence})
                break

            if name_no_punc in nickname_dict[league]:
                logger.debug(f"Coach Exists in {league}")
                org_tags.append({"type": TagType.LEAGUE.value, "value": league, "confidence": method_confidence})
                if name in self.util.sports_player_dict[league]:
                    org_tags.append({"type": TagType.TEAM.value, "value": self.util.sports_player_dict[league][name], "confidence": method_confidence})
                break
        return org_tags

    # TODO Write Test
    def get_sport_and_person_tags_on_non_team_sport(self, token_dict: dict, individual_sports_dict: dict) -> List[TagModel]:
        method_confidence = ConfidenceLevels.HIGH.value
        individual_sports_tags: List[TagModel] = []
        person = token_dict['text']
        for sport in individual_sports_dict.keys():
            if person in self.util.individual_sports_dict[sport]:
                individual_sports_tags.append({"type": TagType.PERSON.value, "value": person, "confidence": method_confidence})
                individual_sports_tags.append({"type": TagType.SPORT.value, "value": sport, "confidence": method_confidence })

        return individual_sports_tags

    def get_sports_terms_tag(self, token_dict: dict):
        method_confidence = ConfidenceLevels.MEDIUM.value
        sports_terms_tags = []
        if token_dict["text"] in self.util.sports_terms_dict:
            sports_terms_tags.append({"type": TagType.SPORT.value, "value": self.util.sports_terms_dict[token_dict["text"]], "confidence": method_confidence})
        return sports_terms_tags

    @debug
    def handle_untagged_key_word(self, key_word: dict) -> List[Dict]:
        word_tags = []
        if self.check_if_game_matchup(key_word):
            word_tags += self.get_matchup_tags(key_word)
        if self.util.is_token_specific_type(key_word, "PERSON"):
            word_tags += self.get_person_tags(key_word)
        if self.util.is_token_specific_type(key_word, "ORG"):
            # TODO process if the key word is the same
            key_word_adjusted = self.util.remove_non_capitalized_words_from_key_word_text(key_word)
            word_tags += self.get_tags_using_sports_dict(key_word_adjusted)
        if len(word_tags) == 0:
            self.sports_ml_algo(key_word)

        return word_tags

    @staticmethod
    def check_if_game_matchup(key_word) -> bool:
        if '-' in key_word["text"] or '@' in key_word["text"]:
            return True
        return False

    def get_matchup_tags(self, key_word: Dict) -> List[Dict]:
        """
        Breaking up the matchup i.e MIN@DAL into a list w each team
        then altering the existing keyword dict to get matchup tags
        with the "text" = "DAL"
        :param key_word:key word dict
        :return: Return matchup_tags identifies
        """
        matchup_tags = []
        try:
            if '-' in key_word["text"]:
                matchup: List[str, str] = key_word["text"].split("-")
            else:
                matchup: List[str, str] = key_word["text"].split("@")
            key_word["text"] = matchup[0]
            matchup_tags += self.get_team_and_league_tags_on_team(key_word)
            key_word["text"] = matchup[1]
            matchup_tags += self.get_team_and_league_tags_on_team(key_word)
            return matchup_tags
        except:
            return []

    def get_tags_using_location(self, location_entities: List[NLPEntityModel], description_tags: List[TagModel]) -> List[TagModel]:
        league_discussed: str = self.util.get_value_of_specified_type(description_tags, TagType.LEAGUE.value)
        location_tags: List[TagModel] = []
        # checking Type Value Which is used for specif
        if league_discussed != '':
            location_tags += self.get_team_tags_from_city_ref_league(location_entities, league_discussed)
        return location_tags


    def get_team_tags_from_city_ref_league(self, location_entities: List[NLPEntityModel], league: str) -> List[TagModel]:
        method_confidence = ConfidenceLevels.LOW.value
        location_tags: List[TagModel] = []
        for location_entity in location_entities:
            if location_entity['text'] in self.util.city_team_dict[league]:
                location_tags.append({'type': TagType.TEAM.value, 'value': self.util.city_team_dict[league][location_entity['text']], "confidence": method_confidence})
        return location_tags

    def sports_ml_algo(self, key_word: Dict):
        # TODO Uncomment Below
        ml_dict = {}
        # google_results = self.google_util.get_google_search_results(word['text'])
        # google_key_words = self.util.get_key_word_dict(google_results)
        # for google_key_word in google_key_words:
        #     google_word_tags = self.get_tags_using_sports_dict(google_key_word)
        #     description_tags += google_word_tags
        #     # ml_dict = self.util.append_to_existing_dict(google_key_word, ml_dict, google_word_tags)
        #     # self.util.save_to_existing_dict_tags()
        # if self.store_ml_data:
        #
        #     self.util.save_to_existing_dict_tags(ml_dict,
        #                                            file_path=r"%s\data\tag_generation_pending_validation" % self.helper.root_dir,
        #                                            file_name="tags.json")
        pass
