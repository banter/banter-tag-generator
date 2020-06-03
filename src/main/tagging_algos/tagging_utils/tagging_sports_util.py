import logging.handlers
import os
from typing import *

from src.main.models.tag_model import TagModel, NLPEntityModel
from src.main.tagging_algos.tagging_base_handler import TaggingBaseHandler
from src.main.tagging_algos.tagging_enums.confidence_levels import ConfidenceLevels
from src.main.tagging_algos.tagging_enums.optimization_tool_mapping import OptimizationToolMapping
from src.main.tagging_algos.tagging_enums.sports_tag_types import SportsTagTypes as TagType
from src.main.utils.decorators import debug

class TaggingSportsUtil(TaggingBaseHandler):

    def __init__(self, optimization_tool: OptimizationToolMapping = OptimizationToolMapping.NONE):
        self.optimization_tool = optimization_tool

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
                           league in description.upper()]
        if matching_league:
            for index, league in enumerate(matching_league):
                sport_and_league_tags.append(
                    {"type": TagType.LEAGUE.value, "value": league, "confidence": method_confidence})
                sport_and_league_tags.append(
                    {"type": TagType.SPORT.value, "value": self.util.league_sport_mapping[league],
                     "confidence": method_confidence})
                self.set_optimization_tool(TagType.LEAGUE.value)

        # TODO Make General Based on sub category
        matching_sport = [sport for sport in self.util.all_sports if sport in description.upper()]
        if matching_sport:
            for index, sport in enumerate(matching_sport):
                sport_and_league_tags.append(
                    {"type": TagType.SPORT.value, "value": sport, "confidence": method_confidence})
                self.set_optimization_tool(TagType.SPORT.value)

        return sport_and_league_tags

    def get_team_and_league_tags_on_team(self, entity: NLPEntityModel) -> List[TagModel]:
        method_confidence = ConfidenceLevels.HIGH.value
        tags = []
        team_name = entity["text"]
        # Sometime names have punctuation that will screw it up, checking if it without punctuation is contained
        # IN List
        team_name_no_punc = self.util.remove_punctuation_from_text(team_name)
        logging.debug(f"Team Name: {team_name}, Team Name no Punc: {team_name_no_punc}")
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
                logging.debug(f"Team Exists in {league}")
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
            tags.append({"type": TagType.SPORT.value, "value": self.util.league_sport_mapping[matching_league],
                         "confidence": method_confidence})
            self.set_optimization_tool(matching_league)

        return tags

    def get_team_player_league_tags_on_player(self, nlp_entity: NLPEntityModel, reference_dict: dict) -> List[TagModel]:
        return self.get_team_player_league_tags_on_player_or_coach(nlp_entity, reference_dict)

    def get_team_player_league_tags_on_coach(self, nlp_entity: NLPEntityModel, reference_dict: dict) -> List[TagModel]:
        return self.get_team_player_league_tags_on_player_or_coach(nlp_entity, reference_dict)

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
                logging.debug(f"Coach Exists in {league}")
                tags.append({"type": TagType.TEAM.value, "value": reference_dict[league][name],
                             "confidence": method_confidence})
                tags.append({"type": TagType.PERSON.value, "value": name, "confidence": method_confidence})
                tags.append({"type": TagType.LEAGUE.value, "value": league, "confidence": method_confidence})
                tags.append({"type": TagType.SPORT.value, "value": self.util.league_sport_mapping[league],
                             "confidence": method_confidence})
                self.set_optimization_tool(TagType.LEAGUE.value)
                break

            if name_no_punc in reference_dict[league]:
                logging.debug(f"Coach Exists in {league}")
                tags.append({"type": TagType.TEAM.value, "value": reference_dict[league][name_no_punc],
                             "confidence": method_confidence})
                tags.append({"type": TagType.PERSON.value, "value": name_no_punc, "confidence": method_confidence})
                tags.append({"type": TagType.LEAGUE.value, "value": league, "confidence": method_confidence})
                tags.append({"type": TagType.SPORT.value, "value": self.util.league_sport_mapping[league],
                             "confidence": method_confidence})
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
                tags.append({"type": TagType.SPORT.value, "value": self.util.league_sport_mapping[league],
                             "confidence": method_confidence})
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
                tags.append({"type": TagType.SPORT.value, "value": self.util.league_sport_mapping[league],
                             "confidence": method_confidence})
                self.set_optimization_tool(TagType.LEAGUE.value)
                if real_name in self.util.sports_player_dict[league]:
                    tags.append({"type": TagType.TEAM.value, "value": self.util.sports_player_dict[league][real_name],
                                 "confidence": method_confidence})
                break
        return tags

    # TODO Write Test
    def get_sport_and_person_tags_on_non_team_sport(self, nlp_entity: NLPEntityModel, individual_sports_dict: dict) -> \
    List[
        TagModel]:
        method_confidence = ConfidenceLevels.HIGH.value
        individual_sports_tags: List[TagModel] = []
        person = nlp_entity['text']
        for sport in individual_sports_dict.keys():
            if person in self.util.individual_sports_dict[sport]:
                individual_sports_tags.append(
                    {"type": TagType.PERSON.value, "value": person, "confidence": method_confidence})
                individual_sports_tags.append(
                    {"type": TagType.SPORT.value, "value": sport, "confidence": method_confidence})

        return individual_sports_tags

    def get_sport_tag_on_sports_terms(self, nlp_entity: NLPEntityModel) -> List[TagModel]:
        method_confidence = ConfidenceLevels.MEDIUM.value
        sports_terms_tags = []
        if nlp_entity["text"] in self.util.sports_terms_dict:
            sports_terms_tags.append(
                {"type": TagType.SPORT.value, "value": self.util.sports_terms_dict[nlp_entity["text"]],
                 "confidence": method_confidence})
            self.set_optimization_tool(TagType.SPORT.value)
        return sports_terms_tags

    def get_team_and_league_tags_from_city(self, location_nlp_entities: List[NLPEntityModel], league: str) -> List[
        TagModel]:
        method_confidence = ConfidenceLevels.LOW.value
        location_tags: List[TagModel] = []
        for location_entity in location_nlp_entities:
            if location_entity['text'] in self.util.city_team_dict[league]:
                location_tags.append(
                    {'type': TagType.TEAM.value, 'value': self.util.city_team_dict[league][location_entity['text']],
                     "confidence": method_confidence})
                location_tags.append(
                    {'type': TagType.LEAGUE.value, 'value': league,
                     "confidence": method_confidence})
                location_tags.append({"type": TagType.SPORT.value, "value": self.util.league_sport_mapping[league],
                                      "confidence": method_confidence})

        return location_tags

    def set_optimization_tool(self, identifier: str):
        if self.optimization_tool.name != 'NONE':
            return
        elif identifier == 'NBA' or identifier == 'BASKETBALL':
            self.optimization_tool = OptimizationToolMapping.BASKETBALL
        elif identifier == 'NFL' or identifier == 'FOOTBALL':
            self.optimization_tool = OptimizationToolMapping.FOOTBALL
        elif identifier == 'MLB' or identifier == 'BASEBALL':
            self.optimization_tool = OptimizationToolMapping.BASEBALL
        elif identifier == 'NHL' or identifier == 'HOCKEY':
            self.optimization_tool = OptimizationToolMapping.HOCKEY

        return
