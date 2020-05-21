import unittest
from typing import *

from src.main.models.tag_model import TagModel
from src.main.tagging_algos.utils.tagging_sports_util import TaggingSportsUtil


class TestTaggingSportsUtil(unittest.TestCase):

    def setUp(self) -> None:
        self.sport_util = TaggingSportsUtil()

    def adj(self, response: List[TagModel]):
        """
        This is used so the confidence levels in test fixtures dont have to be constantly changed/maintained
        :param response: Response from method being tested
        :return: response without confidence level
        """
        for tag in response:
            del tag['confidence']
        return response

    def remove_confidence_for_test_verification(self, response: List[TagModel]):
        """
        This is used so the confidence levels in test fixtures dont have to be constantly changed/maintained
        :param response: Response from method being tested
        :return: response without confidence level
        """
        for tag in response:
            del tag['confidence']
        return response

    def test_get_org_tags(self):
        sample = {'text': 'Browns', 'type': 'ORG', 'start_char': 13, 'end_char': 19}
        response = self.sport_util.get_team_and_league_tags_on_team(sample)
        print(response)
        valid_response = [{'type': 'team', 'value': 'Cleveland Browns'}, {'type': 'league', 'value': 'nfl'}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertEqual(response, valid_response)

    def test_get_org_tags_mlb(self):
        sample = {'text': 'Yankees', 'type': 'ORG', 'start_char': 13, 'end_char': 19}
        response = self.sport_util.get_team_and_league_tags_on_team(sample)
        print(response)
        valid_response = [{'type': 'team', 'value': 'New York Yankees'}, {'type': 'league', 'value': 'mlb'}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertEqual(response, valid_response)

    def test_get_team_and_league_tags_on_player_or_coach_player(self):
        sample = {'text': 'Cam Bedrosian', 'type': 'PERSON', 'start_char': 13, 'end_char': 19}
        response = self.sport_util.get_team_player_league_tags_on_player_or_coach(sample,
                                                                                  self.sport_util.util.sports_player_dict)
        valid_response = [{'type': 'team', 'value': 'Los Angeles Angels'}, {'type': 'league', 'value': 'mlb'},
                          {'type': 'person', 'value': 'Cam Bedrosian'}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_get_team_and_league_tags_on_player_or_coach_player_name_with_jr(self):
        # This test is on a person whose name NORMALLY has a Jr. But in the event it is not included
        # We want to pickup on it. Altered ref. dict for people w Jr. to have an additional entry without Jr.
        # TODO do with Sr. and III
        sample = {'text': 'Maurice Hurst', 'type': 'PERSON', 'start_char': 13, 'end_char': 19}
        response = self.sport_util.get_team_player_league_tags_on_player_or_coach(sample,
                                                                                  self.sport_util.util.sports_player_dict)
        valid_response = [{'type': 'team', 'value': 'Oakland Raiders'}, {'type': 'league', 'value': 'nfl'},
                          {'type': 'person', 'value': 'Maurice Hurst'}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_get_team_and_league_tags_on_player_or_coach_coach(self):
        sample = {'text': 'Mike Tomlin', 'type': 'PERSON', 'start_char': 13, 'end_char': 19}
        response = self.sport_util.get_team_player_league_tags_on_player_or_coach(sample,
                                                                                  self.sport_util.util.sports_coach_dict)
        valid_response = [{'type': 'team', 'value': 'Pittsburgh Steelers'}, {'type': 'league', 'value': 'nfl'},
                          {'type': 'person', 'value': 'Mike Tomlin'}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_get_sport_terms_tags_baseball(self):
        sample = {'text': 'caught napping', 'type': 'UNKNOWN', 'start_char': 13, 'end_char': 19}
        response = self.sport_util.get_sport_tag_on_sports_terms(sample)
        print(response)
        valid_response = [{'type': 'sport', 'value': 'baseball'}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_get_sport_and_person_tags_on_non_team_sport(self):
        sample_input = {'text': "Jordan Spieth", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        valid_output = [{'type': 'person', 'value': 'Jordan Spieth'}, {'type': 'sport', 'value': 'golf'}]
        response = self.sport_util.get_sport_and_person_tags_on_non_team_sport(sample_input,
                                                                               self.sport_util.util.individual_sports_dict)
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_output)

    def test_get_sport_and_person_tags_on_non_team_sport_foreign_name(self):
        sample_input = {'text': "Benjamín Alvarado", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        valid_output = [{'type': 'person', 'value': 'Benjamín Alvarado'}, {'type': 'sport', 'value': 'golf'}]
        response = self.sport_util.get_sport_and_person_tags_on_non_team_sport(sample_input,
                                                                               self.sport_util.util.individual_sports_dict)
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_output)

    def test_get_team_tag_from_city_ref_league(self):
        location_entity = [{'text': 'Dallas', 'type': 'GPE', 'start_char': 61, 'end_char': 67}]
        response = self.sport_util.get_team_and_league_tags_from_city(location_entity, 'nfl')
        expected = [{"type": "team", "value": "Dallas Cowboys"}, {"type": "league", "value": "nfl"},]
        response = self.remove_confidence_for_test_verification(response)
        self.assertEqual(response, expected)

    def test_get_nickname_tags_non_active_player(self):
        entity = {"text": "Black Jesus", "type": "PERSON", "start_char": 1, "end_char": 12}
        response = self.adj(self.sport_util.get_team_player_league_tags_on_nickname(entity,
                                                                                    self.sport_util.util.sports_nickname_dict))
        expected = [{'type': 'person', 'value': 'Earl Monroe'}, {'type': 'league', 'value': 'nba'}]
        self.assertCountEqual(response, expected)

    def test_get_nickname_tags_active_player(self):
        entity = {"text": "King James", "type": "PERSON", "start_char": 1, "end_char": 12}
        response = self.adj(self.sport_util.get_team_player_league_tags_on_nickname(entity,
                                                                                    self.sport_util.util.sports_nickname_dict))
        expected = [{'type': 'person', 'value': 'LeBron James'},
                    {'type': 'league', 'value': 'nba'},
                    {'type': 'team', 'value': 'Los Angeles Lakers'}]
        self.assertCountEqual(response, expected)

    def test_set_sub_genre_mapping(self):
        self.sport_util.set_optimization_tool('nba')
        self.assertEqual('BASKETBALL', self.sport_util.optimization_tool.name)

    def test_set_sub_genre_no_mapping(self):
        self.sport_util.set_optimization_tool('Billy')
        self.assertEqual('NONE', self.sport_util.optimization_tool.name)


if __name__ == '__main__':
    unittest.main()
