import unittest
from typing import *

from src.main.models.tag_model import TagModel
from src.main.tagging_algos.tagging_enums.optimization_tool_mapping import OptimizationToolMapping
from src.main.tagging_algos.tagging_utils.tagging_sports_util import TaggingSportsUtil


class TestTaggingSportsUtil(unittest.TestCase):

    def setUp(self) -> None:
        self.sport_util = TaggingSportsUtil()

    def ignore_confidence(self, response: List[TagModel]):
        """
        This is used so the confidence levels in test fixtures dont have to be constantly changed/maintained
        :param response: Response from method being tested
        :return: response without confidence level
        """
        return self.remove_confidence_for_test_verification(response)

    def remove_confidence_for_test_verification(self, response: List[TagModel]):
        """
        This is used so the confidence levels in test fixtures dont have to be constantly changed/maintained
        :param response: Response from method being tested
        :return: response without confidence level
        """
        for tag in response:
            del tag['confidence']
        return response

    def convert_to_upper_case(self, list_: list):
        for i in list_:
            try:
                i['text'] = i['text'].upper()
            except:
                i['value'] = i['value'].upper()
        return list_

    def test_get_org_tags(self):
        sample = {'text': 'BROWNS', 'type': 'ORG', 'start_char': 13, 'end_char': 19}
        response = self.sport_util.get_team_and_league_tags_on_team(sample)
        print(response)
        valid_response = [{'type': 'team', 'value': 'CLEVELAND BROWNS', 'isPrimary': True},
                          {'type': 'league', 'value': 'NFL', 'isPrimary': False},
                          {'type': 'sport', 'value': 'FOOTBALL', 'isPrimary': False}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertEqual(response, valid_response)

    def test_get_sport_and_league_tags_on_description(self):
        description = 'Marty talks with Niall Horan at Augusta about his love for golf'
        valid_response = [{'type': 'sport', 'value': 'GOLF', 'isPrimary': True}]
        response = self.sport_util.get_sport_and_league_tags_on_description(description)
        self.assertEqual(self.remove_confidence_for_test_verification(response), valid_response)

        description = 'Marty talks with Niall Horan at Augusta about his love for nfl NBA'
        valid_response = [{'type': 'league', 'value': 'NFL', 'isPrimary': True},
                          {'type': 'sport', 'value': 'FOOTBALL', 'isPrimary': False},
                          {'type': 'league', 'value': 'NBA', 'isPrimary': True},
                          {'type': 'sport', 'value': 'BASKETBALL', 'isPrimary': False}, ]
        response = self.sport_util.get_sport_and_league_tags_on_description(description)
        self.assertEqual(self.remove_confidence_for_test_verification(response), valid_response)

    def test_get_org_tags_MLB(self):
        sample = {'text': 'YANKEES', 'type': 'ORG', 'start_char': 13, 'end_char': 19}
        response = self.sport_util.get_team_and_league_tags_on_team(sample)
        print(response)
        valid_response = [{'type': 'team', 'value': 'NEW YORK YANKEES', 'isPrimary': True},
                          {'type': 'league', 'value': 'MLB', 'isPrimary': False},
                          {'type': 'sport', 'value': 'BASEBALL', 'isPrimary': False}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertEqual(response, valid_response)

    def test_get_team_and_league_tags_on_player_or_coach_player_single_position(self):
        sample = {'text': 'CAM BEDROSIAN', 'type': 'PERSON', 'start_char': 13, 'end_char': 19}
        response = self.sport_util.get_team_player_league_tags_on_player_or_coach(sample,
                                                                                  self.sport_util.util.sports_player_dict,
                                                                                  is_tag_for_player=True)
        valid_response = [{'type': 'team', 'value': 'LOS ANGELES ANGELS', 'isPrimary': False},
                          {'type': 'league', 'value': 'MLB', 'isPrimary': False},
                          {'type': 'position', 'value': 'P', 'isPrimary': False},
                          {'type': 'person', 'value': 'CAM BEDROSIAN', 'isPrimary': True},
                          {'type': 'sport', 'value': 'BASEBALL', 'isPrimary': False}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_get_team_and_league_tags_on_player_or_coach_player_multi_position(self):
        sample = {'text': 'GIO URSHELA', 'type': 'PERSON', 'start_char': 13, 'end_char': 19}
        response = self.sport_util.get_team_player_league_tags_on_player_or_coach(sample,
                                                                                  self.sport_util.util.sports_player_dict,
                                                                                  is_tag_for_player=True)
        valid_response = [{'type': 'team', 'value': 'NEW YORK YANKEES', 'isPrimary': False},
                          {'type': 'league', 'value': 'MLB', 'isPrimary': False},
                          {'type': 'position', 'value': '3B', 'isPrimary': False},
                          {'type': 'person', 'value': 'GIO URSHELA', 'isPrimary': True},
                          {'type': 'sport', 'value': 'BASEBALL', 'isPrimary': False}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_get_team_and_league_tags_on_player_or_coach_player_multi_position_outfield(self):
        sample = {'text': 'JAKE MARISNICK', 'type': 'PERSON', 'start_char': 13, 'end_char': 19}
        response = self.sport_util.get_team_player_league_tags_on_player_or_coach(sample,
                                                                                  self.sport_util.util.sports_player_dict,
                                                                                  is_tag_for_player=True)
        valid_response = [{'type': 'team', 'value': 'HOUSTON ASTROS', 'isPrimary': False},
                          {'type': 'league', 'value': 'MLB', 'isPrimary': False},
                          {'type': 'position', 'value': 'OF', 'isPrimary': False},
                          {'type': 'person', 'value': 'JAKE MARISNICK', 'isPrimary': True},
                          {'type': 'sport', 'value': 'BASEBALL', 'isPrimary': False}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_get_team_and_league_tags_on_player_or_coach_player_name_with_jr(self):
        # This test is on a person whose name NORMALLY has a Jr. But in the event it is not included
        # We want to pickup on it. Altered ref. dict for people w Jr. to have an additional entry without Jr.
        # TODO do with Sr. and III
        sample = {'text': 'MAURICE HURST', 'type': 'PERSON', 'start_char': 13, 'end_char': 19}
        response = self.sport_util.get_team_player_league_tags_on_player_or_coach(sample,
                                                                                  self.sport_util.util.sports_player_dict,
                                                                                  is_tag_for_player=True)
        valid_response = [{'type': 'team', 'value': 'OAKLAND RAIDERS', 'isPrimary': False},
                          {'type': 'league', 'value': 'NFL', 'isPrimary': False},
                          {'type': 'person', 'value': 'MAURICE HURST', 'isPrimary': True},
                          {'type': 'sport', 'value': 'FOOTBALL', 'isPrimary': False}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_get_team_and_league_tags_on_player_or_coach_coach(self):
        sample = {'text': 'MIKE TOMLIN', 'type': 'PERSON', 'start_char': 13, 'end_char': 19}
        response = self.sport_util.get_team_player_league_tags_on_player_or_coach(sample,
                                                                                  self.sport_util.util.sports_coach_dict,
                                                                                  is_tag_for_player=False)
        valid_response = [{'type': 'team', 'value': 'PITTSBURGH STEELERS', 'isPrimary': False},
                          {'type': 'league', 'value': 'NFL', 'isPrimary': False},
                          {'type': 'person', 'value': 'MIKE TOMLIN', 'isPrimary': True},
                          {'type': 'sport', 'value': 'FOOTBALL', 'isPrimary': False}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_get_sport_terms_tags_baseball(self):
        sample = {'text': 'caught napping', 'type': 'UNKNOWN', 'start_char': 13, 'end_char': 19}
        response = self.sport_util.get_sport_tag_on_sports_terms(sample)
        print(response)
        valid_response = [{'type': 'sport', 'value': 'BASEBALL', 'isPrimary': True}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_get_sport_and_person_tags_on_non_team_sport(self):
        sample_input = {'text': "JORDAN SPIETH", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        valid_output = [{'type': 'person', 'value': 'JORDAN SPIETH', 'isPrimary': True},
                        {'type': 'sport', 'value': 'GOLF', 'isPrimary': False}]
        response = self.sport_util.get_sport_and_person_tags_on_non_team_sport(sample_input,
                                                                               self.sport_util.util.individual_sports_dict)
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_output)

    def test_get_sport_and_person_tags_on_non_team_sport_foreign_name(self):
        sample_input = {'text': "BENJAMÍN ALVARADO", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        valid_output = [{'type': 'person', 'value': 'BENJAMÍN ALVARADO', 'isPrimary': True},
                        {'type': 'sport', 'value': 'GOLF', 'isPrimary': False}]
        response = self.sport_util.get_sport_and_person_tags_on_non_team_sport(sample_input,
                                                                               self.sport_util.util.individual_sports_dict)
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_output)

    def test_get_team_tag_from_city_ref_league(self):
        location_entity = [{'text': 'DALLAS', 'type': 'GPE', 'start_char': 61, 'end_char': 67}]
        response = self.sport_util.get_team_and_league_tags_from_city(location_entity, 'NFL')
        expected = [{"type": "team", "value": "DALLAS COWBOYS", 'isPrimary': True},
                    {"type": "league", "value": "NFL", 'isPrimary': False},
                    {'type': 'sport', 'value': 'FOOTBALL', 'isPrimary': False}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertEqual(response, expected)

    def test_get_team_player_league_tags_on_player_or_coach(self):
        entity = {'text': 'DEVILS', 'type': 'PROPN'}
        self.sport_util.optimization_tool = OptimizationToolMapping.HOCKEY
        response = self.sport_util.get_team_and_league_tags_on_team(entity)
        expected = [{"type": "team", "value": "NEW JERSEY DEVILS", 'isPrimary': True},
                    {"type": "league", "value": "NHL", 'isPrimary': False},
                    {'type': 'sport', 'value': 'HOCKEY', 'isPrimary': False}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertEqual(response, expected)
        return

    def test_get_nickname_tags_non_active_player(self):
        entity = {"text": "MELO", "type": "PERSON", "start_char": 1, "end_char": 12}
        response = self.ignore_confidence(self.sport_util.get_team_player_league_tags_on_nickname(entity,
                                                                                                  self.sport_util.util.sports_nickname_dict))
        expected = [{'type': 'person', 'value': 'CARMELO ANTHONY', 'isPrimary': True},
                    {'type': 'league', 'value': 'NBA', 'isPrimary': False},
                    {'type': 'sport', 'value': 'BASKETBALL', 'isPrimary': False},
                    {'type': 'team', 'value': 'PORTLAND TRAIL BLAZERS', 'isPrimary': False},
                    {'type': 'position', 'value': 'PF', 'isPrimary': False}]
        self.assertCountEqual(response, expected)

    def test_get_nickname_tags_active_player(self):
        entity = {"text": "KING JAMES", "type": "PERSON", "start_char": 1, "end_char": 12}
        response = self.ignore_confidence(self.sport_util.get_team_player_league_tags_on_nickname(entity,
                                                                                                  self.sport_util.util.sports_nickname_dict))
        expected = [{'type': 'person', 'value': 'LEBRON JAMES', 'isPrimary': True},
                    {'type': 'league', 'value': 'NBA', 'isPrimary': False},
                    {'type': 'position', 'value': 'SF', 'isPrimary': False},
                    {'type': 'team', 'value': 'LOS ANGELES LAKERS', 'isPrimary': False},
                    {'type': 'sport', 'value': 'BASKETBALL', 'isPrimary': False}]
        self.assertCountEqual(response, expected)

    def test_set_sub_genre_mapping(self):
        self.sport_util.set_optimization_tool('NBA')
        self.assertEqual('BASKETBALL', self.sport_util.optimization_tool.name)

    def test_set_sub_genre_no_mapping(self):
        self.sport_util.set_optimization_tool('Billy')
        self.assertEqual('NONE', self.sport_util.optimization_tool.name)


if __name__ == '__main__':
    unittest.main()
