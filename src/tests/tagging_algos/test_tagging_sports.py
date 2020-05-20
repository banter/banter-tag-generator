import unittest
from typing import *

from src.main.models.tag_model import TagModel
from src.main.tagging_algos.tagging_enums.optimization_tool_mapping import OptimizationToolMapping
from src.main.tagging_algos.tagging_sports import TaggingSportsHandler


class TestTaggingSportsHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        super(TestTaggingSportsHandler, self).setUpClass()
        self.sport_handler = TaggingSportsHandler()
        self.integration_test_fixture = self.sport_handler.util.read_json_file(f"../resources/fixtures",
                                                                               "sports_tagging_integration_fixture.json")

    def setUp(self) -> None:
        self.sport_handler = TaggingSportsHandler()

        # Same as below but shorter description :)

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

    def test_generate_sports_tags(self):
        sample = "Hello this is Austin Marchese and this is the Banter Podcast."
        response = self.sport_handler.generate_sports_tags(sample)
        self.assertIsNotNone(response)

    def test_generate_sports_tags_empty(self):
        sample = "ajbfasd askdhasd sdkja"
        response = self.sport_handler.generate_sports_tags(sample)
        self.assertEqual(response, [])

    def test_get_org_tags(self):
        sample = {'text': 'Browns', 'type': 'ORG', 'start_char': 13, 'end_char': 19}
        response = self.sport_handler.get_team_and_league_tags_on_team(sample)
        print(response)
        valid_response = [{'type': 'team', 'value': 'Cleveland Browns'}, {'type': 'league', 'value': 'nfl'}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertEqual(response, valid_response)

    def test_get_org_tags_mlb(self):
        sample = {'text': 'Yankees', 'type': 'ORG', 'start_char': 13, 'end_char': 19}
        response = self.sport_handler.get_team_and_league_tags_on_team(sample)
        print(response)
        valid_response = [{'type': 'team', 'value': 'New York Yankees'}, {'type': 'league', 'value': 'mlb'}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertEqual(response, valid_response)

    def test_get_team_and_league_tags_on_player_or_coach_player(self):
        sample = {'text': 'Cam Bedrosian', 'type': 'PERSON', 'start_char': 13, 'end_char': 19}
        response = self.sport_handler.get_team_player_league_tags_on_player_or_coach(sample,
                                                                                     self.sport_handler.util.sports_player_dict)
        valid_response = [{'type': 'team', 'value': 'Los Angeles Angels'}, {'type': 'league', 'value': 'mlb'},
                          {'type': 'person', 'value': 'Cam Bedrosian'}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_get_team_and_league_tags_on_player_or_coach_coach(self):
        sample = {'text': 'Mike Tomlin', 'type': 'PERSON', 'start_char': 13, 'end_char': 19}
        response = self.sport_handler.get_team_player_league_tags_on_player_or_coach(sample,
                                                                                     self.sport_handler.util.sports_coach_dict)
        valid_response = [{'type': 'team', 'value': 'Pittsburgh Steelers'}, {'type': 'league', 'value': 'nfl'},
                          {'type': 'person', 'value': 'Mike Tomlin'}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_get_sport_terms_tags_baseball(self):
        sample = {'text': 'caught napping', 'type': 'UNKNOWN', 'start_char': 13, 'end_char': 19}
        response = self.sport_handler.get_sport_tag_on_sports_terms(sample)
        print(response)
        valid_response = [{'type': 'sport', 'value': 'baseball'}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_tag_generator_punctuation(self):
        sample_input = {'text': "Tom Brady'", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        response = self.sport_handler.generate_basic_sport_tags(sample_input)
        print(response)
        valid_response = [{'type': 'team', 'value': 'New England Patriots'}, {'type': 'person', 'value': "Tom Brady"},
                          {'type': 'league', 'value': 'nfl'}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_tag_generator_no_punctuation(self):
        sample_input = {'text': "Tom Brady", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        response = self.sport_handler.generate_basic_sport_tags(sample_input)
        print(response)
        valid_response = [{'type': 'team', 'value': 'New England Patriots'}, {'type': 'person', 'value': 'Tom Brady'},
                          {'type': 'league', 'value': 'nfl'}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_integration_generate_sports_tags(self):
        sample = "Hello this is Austin Marchese and this is the Banter Podcast."
        valid_output = [{'type': 'person', 'value': 'Austin Marchese'}]
        response = self.sport_handler.generate_sports_tags(sample)
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_output)

    def test_get_sport_and_person_tags_on_non_team_sport(self):
        sample_input = {'text': "Jordan Spieth", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        valid_output = [{'type': 'person', 'value': 'Jordan Spieth'}, {'type': 'sport', 'value': 'golf'}]
        response = self.sport_handler.get_sport_and_person_tags_on_non_team_sport(sample_input,
                                                                                  self.sport_handler.util.individual_sports_dict)
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_output)

    def test_get_sport_and_person_tags_on_non_team_sport_foreign_name(self):
        sample_input = {'text': "Benjamín Alvarado", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        valid_output = [{'type': 'person', 'value': 'Benjamín Alvarado'}, {'type': 'sport', 'value': 'golf'}]
        response = self.sport_handler.get_sport_and_person_tags_on_non_team_sport(sample_input,
                                                                                  self.sport_handler.util.individual_sports_dict)
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_output)

    def test_get_sports_tags_specific_test(self):
        description = "We look at the 15 teams in the Western Conference, including Dallas' trade options for Dennis Smith Jr., the Lakers' recent struggles, OKC's Terrance Ferguson, and more."
        desired_tags = [{'type': 'team', 'value': 'New York Knicks'}, {'type': 'team', 'value': 'Dallas Mavericks'},
                        {'type': 'person', 'value': 'Dennis Smith Jr.'},
                        {'type': 'league', 'value': 'nba'}, {'type': 'team', 'value': 'Los Angeles Lakers'},
                        {'type': 'team', 'value': 'Oklahoma City Thunder'},
                        {'type': 'person', 'value': 'Terrance Ferguson'}]
        response = self.sport_handler.get_sports_tags(description)
        print(response)
        response = self.sport_handler.get_sports_tags(description)
        print(response)
        # self.assertCountEqual(response, desired_tags)

    def test_check_if_game_matchup(self):
        key_word = {'text': "NYG@MIN", 'type': 'ORG', 'start_char': 94, 'end_char': 104}
        self.assertTrue(self.sport_handler.check_if_game_matchup(key_word))

    def test_get_matchup_tags(self):
        """
        Duplicate tags is fine as this is handled in seperate methods
        """
        key_word = {'text': "NYG@DAL", 'type': 'ORG', 'start_char': 94, 'end_char': 104}
        desired_tags = [{"type": "team", "value": "Dallas Cowboys"}, {"type": "league", "value": "nfl"},
                        {"type": "team", "value": "New York Giants"}, {"type": "league", "value": "nfl"}]
        response = self.sport_handler.generate_matchup_tags(key_word)
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, desired_tags)

    def test_get_team_tag_from_city_ref_league(self):
        location_entity = [{'text': 'Dallas', 'type': 'GPE', 'start_char': 61, 'end_char': 67}]
        response = self.sport_handler.get_team_tags_from_city_ref_league(location_entity, 'nfl')
        expected = [{"type": "team", "value": "Dallas Cowboys"}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertEqual(response, expected)

    def test_get_tags_using_location(self):
        location_entities = [{'text': 'Dallas', 'type': 'GPE', 'start_char': 61, 'end_char': 67}]
        expected = [{"type": "team", "value": "Dallas Mavericks"}]
        self.sport_handler.optimization_tool = OptimizationToolMapping.BASKETBALL
        response = self.sport_handler.generate_location_tags(location_entities)
        response = self.remove_confidence_for_test_verification(response)
        self.assertEqual(expected, response)

    def test_get_nickname_tags_non_active_player(self):
        entity = {"text": "Black Jesus", "type": "PERSON", "start_char": 1, "end_char": 12}
        response = self.adj(self.sport_handler.get_team_player_league_tags_on_nickname(entity,
                                                                                       self.sport_handler.util.sports_nickname_dict))
        expected = [{'type': 'person', 'value': 'Earl Monroe'}, {'type': 'league', 'value': 'nba'}]
        self.assertCountEqual(response, expected)

    def test_get_nickname_tags_active_player(self):
        entity = {"text": "King James", "type": "PERSON", "start_char": 1, "end_char": 12}
        response = self.adj(self.sport_handler.get_team_player_league_tags_on_nickname(entity,
                                                                                       self.sport_handler.util.sports_nickname_dict))
        expected = [{'type': 'person', 'value': 'LeBron James'},
                    {'type': 'league', 'value': 'nba'},
                    {'type': 'team', 'value': 'Los Angeles Lakers'}]
        self.assertCountEqual(response, expected)

    def test_set_sub_genre_mapping(self):
        self.sport_handler.set_optimization_tool('nba')
        self.assertEqual('BASKETBALL', self.sport_handler.optimization_tool.name)

    def test_set_sub_genre_no_mapping(self):
        self.sport_handler.set_optimization_tool('Billy')
        self.assertEqual('NONE', self.sport_handler.optimization_tool.name)

    # @unittest.skip("Skip when testing locally, this is a full integration test, uncomment in production")
    def test_get_sports_tags_full_test(self):
        for (description, desired_tags) in self.integration_test_fixture.items():
            response = self.sport_handler.get_sports_tags(description)
            print(response, description)
            response = self.remove_confidence_for_test_verification(response)
            self.assertCountEqual(response, desired_tags)


if __name__ == '__main__':
    unittest.main()
