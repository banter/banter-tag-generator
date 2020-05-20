import logging.handlers
import os
from typing import *

from src.main.models.tag_model import TagModel, NLPEntityModel
from src.main.tagging_algos.tagging_base_handler import TaggingBaseHandler
from src.main.tagging_algos.tagging_enums.confidence_levels import ConfidenceLevels
from src.main.tagging_algos.tagging_enums.optimization_tool_mapping import OptimizationToolMapping
from src.main.tagging_algos.tagging_enums.sports_tag_types import SportsTagTypes as TagType
from src.main.utils.decorators import debug
from src.main.tagging_algos.utils.sports_tag_util import SportsUtil

PARENT_DIR = os.getcwd()
logger = logging.getLogger(__name__)


class TaggingSportsHandler(TaggingBaseHandler, SportsUtil):

    def get_sports_tags(self, description: str,
                        optimization_tool: OptimizationToolMapping = OptimizationToolMapping.NONE) -> List[TagModel]:
        self.optimization_tool = optimization_tool
        sports_tags = self.generate_sports_tags(description)
        return self.util.remove_duplicates_from_dict_list_based_on_key(sports_tags, "value")

    @debug
    def generate_sports_tags(self, description: str) -> List[TagModel]:

        description_tags: List[TagModel] = []
        location_entities: List[NLPEntityModel] = []
        key_words = self.util.get_key_word_dict(description)
        description_tags += self.get_sport_and_league_tags_on_description(description)

        for word in key_words:
            if word['text'].lower() in self.util.sports_leagues:
                # Handling sports leagues in other method skipping this
                continue
            word_tags = self.generate_basic_sport_tags(word)
            if len(word_tags) == 0:
                word_tags += self.handle_untagged_key_word(word)

            if len(word_tags) == 0:
                # Checking if it is an untagged location, if it is will use later
                if self.util.is_token_specific_type(word, "GPE"):
                    location_entities.append(word)
            description_tags += word_tags

        # league_discussed: str = self.util.get_value_of_specified_type(description_tags, TagType.LEAGUE.value)
        # If there are untagged location tags, going to check if there is any
        # Reference to a sports league. This way we can use this as context for the discussion
        if len(location_entities) != 0:
            description_tags += self.generate_location_tags(location_entities)

        return description_tags

    @debug
    def generate_basic_sport_tags(self, key_word: Dict) -> List[TagModel]:
        key_word_tags: list = []
        key_word_tags += self.get_team_and_league_tags_on_team(key_word)
        key_word_tags += self.get_team_player_league_tags_on_player_or_coach(key_word, self.util.sports_player_dict)
        if len(key_word_tags) == 0:
            key_word_tags += self.get_team_player_league_tags_on_player_or_coach(key_word, self.util.sports_coach_dict)
        if len(key_word_tags) == 0:
            key_word_tags += self.get_sport_and_person_tags_on_non_team_sport(key_word,
                                                                              self.util.individual_sports_dict)
        if len(key_word_tags) == 0:
            key_word_tags += self.get_team_player_league_tags_on_nickname(key_word, self.util.sports_nickname_dict)
        # TODO Dont think sports terms is worth it
        if len(key_word_tags) == 0:
            key_word_tags += self.get_sport_tag_on_sports_terms(key_word)

        return key_word_tags

    def generate_matchup_tags(self, key_word: Dict) -> List[Dict]:
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

    def generate_location_tags(self, location_entities: List[NLPEntityModel]) -> \
            List[TagModel]:
        location_tags: List[TagModel] = []
        # checking Type Value Which is used for specif
        if self.optimization_tool.name != 'NONE':
            location_tags += self.get_team_tags_from_city_ref_league(location_entities,
                                                                     self.optimization_tool.value["leagues"][0])
        return location_tags

    @debug
    def get_sport_and_league_tags_on_description(self, description: str) -> List[TagModel]:
        """
        If League is mentioned in a tokenized word i.e ESPN NBA, this would tag for NBA
        Done before any words are tokenized for a quick check
        :param description: String/Text of Summary
        :return: List of tags
        """
        method_confidence = ConfidenceLevels.MEDIUM.value
        sport_and_league_tags: list = []
        matching_league = [league for league in self.optimization_tool.value["leagues"] if
                           league in description.lower()]
        if matching_league:
            for index, value in enumerate(matching_league):
                sport_and_league_tags.append(
                    {"type": TagType.LEAGUE.value, "value": value, "confidence": method_confidence})
                self.set_optimization_tool(TagType.LEAGUE.value)

        # TODO Make General Based on sub category
        matching_sport = [sport for sport in self.util.all_sports if sport in description.lower()]
        if matching_sport:
            for index, value in enumerate(matching_sport):
                sport_and_league_tags.append(
                    {"type": TagType.SPORT.value, "value": value, "confidence": method_confidence})
                self.set_optimization_tool(TagType.SPORT.value)

        return sport_and_league_tags

    def get_team_and_league_tags_on_team(self, entity: NLPEntityModel) -> List[TagModel]:
        method_confidence = ConfidenceLevels.HIGH.value
        tags = []
        team_name = entity["text"]
        # Sometime names have punctuation that will screw it up, checking if it without punctuation is contained
        # IN List
        team_name_no_punc = self.util.remove_punctuation_from_text(team_name)
        logger.debug(f"Team Name: {team_name}, Team Name no Punc: {team_name_no_punc}")
        matching_value: str = ''
        matching_league: str = ''
        for league in self.optimization_tool.value["leagues"]:
            # TODO Handle if there are multiple teams with the same name
            if team_name in self.util.sports_team_dict[league]:
                matching_value = self.util.sports_team_dict[league][team_name]
                matching_league = league
                break
            if team_name_no_punc in self.util.sports_team_dict[league]:
                matching_value = self.util.sports_team_dict[league][team_name_no_punc]
                matching_league = league
                break
            if team_name in self.util.abbreviation_team_dict[league]:
                logger.debug(f"Team Exists in {league}")
                matching_value = self.util.abbreviation_team_dict[league][team_name]
                matching_league = league
                break
            if team_name_no_punc in self.util.abbreviation_team_dict[league]:
                matching_value = self.util.abbreviation_team_dict[league][team_name_no_punc]
                matching_league = league
                break
        if matching_league != '':
            tags.append({"type": TagType.TEAM.value, "value": matching_value,
                         "confidence": method_confidence})
            tags.append({"type": TagType.LEAGUE.value, "value": matching_league, "confidence": method_confidence})
            self.set_optimization_tool(matching_league)

        return tags

    def get_team_player_league_tags_on_player_or_coach(self, token_dict: dict, reference_dict: dict) -> List[TagModel]:
        """
        Used to check if person is either a player or coach
        :param token_dict:
        :param reference_dict:
        :return:
        """
        method_confidence = ConfidenceLevels.HIGH.value
        tags = []
        name = token_dict["text"]
        # Sometime names have punctuation that will screw it up, checking if it without punctuation is contained
        # IN List
        name_no_punc = self.util.remove_punctuation_from_text(name)
        for league in self.optimization_tool.value['leagues']:

            if name in reference_dict[league]:
                logger.debug(f"Coach Exists in {league}")
                tags.append({"type": TagType.TEAM.value, "value": reference_dict[league][name],
                             "confidence": method_confidence})
                tags.append({"type": TagType.PERSON.value, "value": name, "confidence": method_confidence})
                tags.append({"type": TagType.LEAGUE.value, "value": league, "confidence": method_confidence})
                self.set_optimization_tool(TagType.LEAGUE.value)
                break

            if name_no_punc in reference_dict[league]:
                logger.debug(f"Coach Exists in {league}")
                tags.append({"type": TagType.TEAM.value, "value": reference_dict[league][name_no_punc],
                             "confidence": method_confidence})
                tags.append({"type": TagType.PERSON.value, "value": name_no_punc, "confidence": method_confidence})
                tags.append({"type": TagType.LEAGUE.value, "value": league, "confidence": method_confidence})
                self.set_optimization_tool(TagType.LEAGUE.value)
                break

        return tags

    def get_team_player_league_tags_on_nickname(self, entity: NLPEntityModel, nickname_dict: Dict) -> List[TagModel]:
        """
        :param entity:
        :param nickname_dict:
        :return:
        """
        method_confidence = ConfidenceLevels.MEDIUM.value
        tags = []
        nickname = entity["text"]
        # Sometime names have punctuation that will screw it up, checking if it without punctuation is contained
        # IN List
        nickname_no_punc = self.util.remove_punctuation_from_text(nickname)
        for league in self.optimization_tool.value["leagues"]:

            if nickname in nickname_dict[league]:
                real_name = nickname_dict[league][nickname]
                tags.append({"type": TagType.PERSON.value, "value": nickname_dict[league][nickname],
                             "confidence": method_confidence})
                tags.append({"type": TagType.LEAGUE.value, "value": league, "confidence": method_confidence})
                self.set_optimization_tool(TagType.LEAGUE.value)
                if real_name in self.util.sports_player_dict[league]:
                    tags.append({"type": TagType.TEAM.value, "value": self.util.sports_player_dict[league][real_name],
                                 "confidence": method_confidence})
                break
            if nickname_no_punc in nickname_dict[league]:
                real_name = nickname_dict[league][nickname_no_punc]
                tags.append({"type": TagType.PERSON.value, "value": nickname_dict[league][nickname_no_punc],
                             "confidence": method_confidence})
                tags.append({"type": TagType.LEAGUE.value, "value": league, "confidence": method_confidence})
                self.set_optimization_tool(TagType.LEAGUE.value)
                if real_name in self.util.sports_player_dict[league]:
                    tags.append({"type": TagType.TEAM.value, "value": self.util.sports_player_dict[league][real_name],
                                 "confidence": method_confidence})
                break
        return tags

    # TODO Write Test
    def get_sport_and_person_tags_on_non_team_sport(self, token_dict: dict, individual_sports_dict: dict) -> List[
        TagModel]:
        method_confidence = ConfidenceLevels.HIGH.value
        individual_sports_tags: List[TagModel] = []
        person = token_dict['text']
        for sport in individual_sports_dict.keys():
            if person in self.util.individual_sports_dict[sport]:
                individual_sports_tags.append(
                    {"type": TagType.PERSON.value, "value": person, "confidence": method_confidence})
                individual_sports_tags.append(
                    {"type": TagType.SPORT.value, "value": sport, "confidence": method_confidence})

        return individual_sports_tags

    def get_sport_tag_on_sports_terms(self, token_dict: dict) -> List[TagModel]:
        method_confidence = ConfidenceLevels.MEDIUM.value
        sports_terms_tags = []
        if token_dict["text"] in self.util.sports_terms_dict:
            sports_terms_tags.append(
                {"type": TagType.SPORT.value, "value": self.util.sports_terms_dict[token_dict["text"]],
                 "confidence": method_confidence})
            self.set_optimization_tool(TagType.SPORT.value)
        return sports_terms_tags

    def get_team_tags_from_city_ref_league(self, location_entities: List[NLPEntityModel], league: str) -> List[
        TagModel]:
        method_confidence = ConfidenceLevels.LOW.value
        location_tags: List[TagModel] = []
        for location_entity in location_entities:
            if location_entity['text'] in self.util.city_team_dict[league]:
                location_tags.append(
                    {'type': TagType.TEAM.value, 'value': self.util.city_team_dict[league][location_entity['text']],
                     "confidence": method_confidence})
        return location_tags

    @debug
    def handle_untagged_key_word(self, key_word: dict) -> List[Dict]:
        word_tags = []
        if self.check_if_game_matchup(key_word):
            word_tags += self.generate_matchup_tags(key_word)
        if self.util.is_token_specific_type(key_word, "PERSON"):
            word_tags += self.get_person_tags(key_word)
        if self.util.is_token_specific_type(key_word, "ORG"):
            # TODO process if the key word is the same
            key_word_adjusted = self.util.remove_non_capitalized_words_from_key_word_text(key_word)
            word_tags += self.generate_basic_sport_tags(key_word_adjusted)
        if len(word_tags) == 0:
            self.sports_ml_algo(key_word)

        return word_tags

    @staticmethod
    def check_if_game_matchup(key_word) -> bool:
        if '-' in key_word["text"] or '@' in key_word["text"]:
            return True
        return False

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

    def set_optimization_tool(self, identifier: str):
        if self.optimization_tool.name != 'NONE':
            return
        elif identifier == 'nba' or identifier == 'basketball':
            self.optimization_tool = OptimizationToolMapping.BASKETBALL
        elif identifier == 'nfl' or identifier == 'american football':
            self.optimization_tool = OptimizationToolMapping.FOOTBALL
        elif identifier == 'mlb' or identifier == 'baseball':
            self.optimization_tool = OptimizationToolMapping.BASEBALL
        elif identifier == 'nhl' or identifier == 'hockey':
            self.optimization_tool = OptimizationToolMapping.HOCKEY

        return
