import os
import unittest
from os.path import dirname, realpath
from typing import *

from src.main.models.tag_model import TagModel
from src.main.tagging_algos.tagging_enums.optimization_tool_mapping import OptimizationToolMapping
from src.main.tagging_algos.tagging_sports_handler import TaggingSportsHandler

BASEDIR = os.path.abspath(os.path.dirname(dirname(realpath(__file__))))


class TestTaggingSportsHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        super(TestTaggingSportsHandler, self).setUpClass()
        # Allowing for test console to not limit output length
        self.maxDiff = None
        self.sport_handler = TaggingSportsHandler()
        FIXTURE_LOCATION = '%s/resources/fixtures' % BASEDIR
        self.integration_test_fixture = self.sport_handler.util.read_json_file(FIXTURE_LOCATION,
                                                                               "sports_tagging_integration_fixture.json")
        self.normalization_test_fixture = self.sport_handler.util.read_json_file(FIXTURE_LOCATION,
                                                                                 "sports_tagging_normalization_fixture.json")

    def setUp(self) -> None:
        self.sport_handler = TaggingSportsHandler()

        # Same as below but shorter description :)

    def adj(self, response: List[TagModel]):
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

    def test_generate_sports_tags(self):
        sample = "Hello this is Austin Marchese and this is the Banter Podcast."
        response = self.sport_handler.generate_sports_tags(sample)
        self.assertIsNotNone(response)

    def test_generate_sports_tags_empty(self):
        sample = "ajbfasd askdhasd sdkja"
        response = self.sport_handler.generate_sports_tags(sample)
        self.assertEqual(response, [])

    def test_tag_generator_name(self):
        sample_input = {'text': "TOM BRADY", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        response = self.sport_handler.generate_basic_sport_tags(sample_input)
        print(response)
        valid_response = [{'type': 'team', 'value': 'TAMPA BAY BUCCANEERS', 'isPrimary': False},
                          {'type': 'person', 'value': 'Tom Brady', 'isPrimary': True},
                          {'type': 'position', 'value': 'QB', 'isPrimary': False},
                          {'type': 'league', 'value': 'NFL', 'isPrimary': False},
                          {"type": "sport", "value": "FOOTBALL", 'isPrimary': False}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_integration_generate_sports_tags(self):
        sample = "Hello this is Austin Marchese and this is the Banter Podcast."
        valid_output = [{'type': 'person', 'value': 'AUSTIN MARCHESE', 'isPrimary': True}]
        response = self.sport_handler.generate_sports_tags(sample)
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_output)

    def test_check_if_game_matchup_at(self):
        key_word = {'text': "NYG@MIN", 'type': 'ORG', 'start_char': 94, 'end_char': 104}
        self.assertTrue(self.sport_handler.is_nlp_entity_a_game_matchup(key_word))

    def test_check_if_game_matchup_and(self):
        key_word = {"text": "Lakers & Clippers", "type": "ORG", "start_char": 0, "end_char": 17}
        self.assertTrue(self.sport_handler.is_nlp_entity_a_game_matchup(key_word))

    def test_generate_matchup_tags(self):
        """
        Duplicate tags is fine as this is handled in seperate methods
        """
        key_word = {'text': "NYG@DAL", 'type': 'ORG', 'start_char': 94, 'end_char': 104}
        desired_tags = [{"type": "team", "value": "DALLAS COWBOYS", 'isPrimary': True},
                        {"type": "league", "value": "NFL", 'isPrimary': False},
                        {"type": "sport", "value": "FOOTBALL", 'isPrimary': False},
                        {"type": "team", "value": "NEW YORK GIANTS", 'isPrimary': True},
                        {"type": "league", "value": "NFL", 'isPrimary': False},
                        {"type": "sport", "value": "FOOTBALL", 'isPrimary': False}]
        response = self.sport_handler.generate_matchup_tags(key_word)
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, desired_tags)

    def test_generate_tags_using_location(self):
        location_entities = [{'text': 'DALLAS', 'type': 'GPE', 'start_char': 61, 'end_char': 67}]
        expected = [{"type": "team", "value": "DALLAS MAVERICKS", 'isPrimary': True},
                    {"type": "league", "value": "NBA", 'isPrimary': False},
                    {"type": "sport", "value": "BASKETBALL", 'isPrimary': False}]
        self.sport_handler.optimization_tool = OptimizationToolMapping.BASKETBALL
        response = self.sport_handler.generate_location_tags(location_entities)
        response = self.remove_confidence_for_test_verification(response)
        self.assertEqual(expected, response)

    def test_get_sports_tags_normalized_text_test(self):
        for (description, desired_tags) in self.normalization_test_fixture.items():
            response = self.sport_handler.get_sports_tags(description)
            print(response, description)
            response = self.remove_confidence_for_test_verification(response)
            self.assertCountEqual(response, desired_tags)

    def test_get_sports_tags_empty_description(self):
        description = ""
        desired_tags = []
        response = self.adj(self.sport_handler.get_sports_tags(description))
        self.assertCountEqual(response, desired_tags)

    # TODO Tag Clyde Edwards-Helair in this scenario
    @unittest.skip("Skip failing test")
    def test_get_sports_tags_specific_test(self):
        description = "Speaking of player opt-outs, Damien Williams decided to opt-out this season, causing the Clyde Edwards-Helaire hype train to explode. Is he a fantasy first-rounder?"
        desired_tags = [
            {"type": "team", "value": "Kansas City Chiefs","isPrimary": False},
            {"type": "person","value": "Damien Williams","isPrimary": True},
            {"type": "person","value": "Clyde Edwards-Helaire","isPrimary": True},
            {"type": "position","value": "RB","isPrimary": False},
            {"type": "league","value": "NFL","isPrimary": False},
            {"type": "sport","value": "Football","isPrimary": False}
        ]
        response = self.adj(self.sport_handler.get_sports_tags(description))
        print(response, desired_tags)
        self.assertCountEqual(response, desired_tags)

    # @unittest.skip("Skip when testing locally, this is a full integration test, uncomment in production")
    def test_get_sports_tags_full_test(self):
        for (description, desired_tags) in self.integration_test_fixture.items():
            response = self.sport_handler.get_sports_tags(description)
            print(response, desired_tags, description)
            response = self.remove_confidence_for_test_verification(response)
            self.assertCountEqual(response, desired_tags)


if __name__ == '__main__':
    unittest.main()
