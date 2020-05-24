import unittest
from typing import *

from src.main.models.tag_model import TagModel
from src.main.tagging_algos.tagging_enums.optimization_tool_mapping import OptimizationToolMapping
from src.main.tagging_algos.tagging_sports_handler import TaggingSportsHandler


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

    def test_tag_generator_punctuation(self):
        sample_input = {'text': "Tom Brady'", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        response = self.sport_handler.generate_basic_sport_tags(sample_input)
        print(response)
        valid_response = [{'type': 'team', 'value': 'New England Patriots'}, {'type': 'person', 'value': "Tom Brady"},
                          {'type': 'league', 'value': 'NFL'}, {"type": "sport", "value": "football"}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_tag_generator_no_punctuation(self):
        sample_input = {'text': "Tom Brady", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        response = self.sport_handler.generate_basic_sport_tags(sample_input)
        print(response)
        valid_response = [{'type': 'team', 'value': 'New England Patriots'}, {'type': 'person', 'value': 'Tom Brady'},
                          {'type': 'league', 'value': 'NFL'}, {"type": "sport", "value": "football"}]
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_response)

    def test_integration_generate_sports_tags(self):
        sample = "Hello this is Austin Marchese and this is the Banter Podcast."
        valid_output = [{'type': 'person', 'value': 'Austin Marchese'}]
        response = self.sport_handler.generate_sports_tags(sample)
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, valid_output)

    def test_check_if_game_matchup_at(self):
        key_word = {'text': "NYG@MIN", 'type': 'ORG', 'start_char': 94, 'end_char': 104}
        self.assertTrue(self.sport_handler.check_if_game_matchup(key_word))

    def test_check_if_game_matchup_and(self):
        key_word = {"text": "Lakers & Clippers", "type": "ORG", "start_char": 0, "end_char": 17}
        self.assertTrue(self.sport_handler.check_if_game_matchup(key_word))

    def test_generate_matchup_tags(self):
        """
        Duplicate tags is fine as this is handled in seperate methods
        """
        key_word = {'text': "NYG@DAL", 'type': 'ORG', 'start_char': 94, 'end_char': 104}
        desired_tags = [{"type": "team", "value": "Dallas Cowboys"}, {"type": "league", "value": "NFL"},
                        {"type": "sport", "value": "football"},
                        {"type": "team", "value": "New York Giants"}, {"type": "league", "value": "NFL"},
                        {"type": "sport", "value": "football"}]
        response = self.sport_handler.generate_matchup_tags(key_word)
        response = self.remove_confidence_for_test_verification(response)
        self.assertCountEqual(response, desired_tags)

    def test_generate_tags_using_location(self):
        location_entities = [{'text': 'Dallas', 'type': 'GPE', 'start_char': 61, 'end_char': 67}]
        expected = [{"type": "team", "value": "Dallas Mavericks"}, {"type": "league", "value": "NBA"}, {
            "type": "sport",
            "value": "basketball"
        }]
        self.sport_handler.optimization_tool = OptimizationToolMapping.BASKETBALL
        response = self.sport_handler.generate_location_tags(location_entities)
        response = self.remove_confidence_for_test_verification(response)
        self.assertEqual(expected, response)

    # @unittest.skip("Skip when testing locally, this is a full integration test, uncomment in production")
    def test_get_sports_tags_full_test(self):
        for (description, desired_tags) in self.integration_test_fixture.items():
            response = self.sport_handler.get_sports_tags(description)
            print(response, description)
            response = self.remove_confidence_for_test_verification(response)
            self.assertCountEqual(response, desired_tags)

    def test_get_sports_tags_specific_test(self):
        description = "Lakers & Clippers"
        desired_tags = [
            {
                "type": "team",
                "value": "Los Angeles Lakers"
            },
            {
                "type": "league",
                "value": "NBA"
            },
            {
                "type": "team",
                "value": "Los Angeles Clippers"
            },
            {
                "type": "sport",
                "value": "basketball"
            }]
        response = self.adj(self.sport_handler.get_sports_tags(description))
        print(response)
        self.assertCountEqual(response, desired_tags)


if __name__ == '__main__':
    unittest.main()
