import unittest

from src.main.tagging_algos.tagging_sports import TaggingSportsHandler


class TestTaggingSportsHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        super(TestTaggingSportsHandler, self).setUpClass()
        self.sport_handler = TaggingSportsHandler()
        self.integration_test_fixture = self.sport_handler.util.read_json_file(f"../resources/fixtures",
                                                                               "sports_tagging_integration_fixture.json")

    def test_generate_sports_tags(self):
        sample = "Hello this is Austin Marchese and this is the Banter Podcast."
        response = self.sport_handler.generate_sports_tags(sample)
        print(response)
        # TODO fix test
        self.assertIsNotNone(response)

    def test_generate_sports_tags_empty(self):
        sample = "ajbfasd askdhasd sdkja"
        response = self.sport_handler.generate_sports_tags(sample)
        print(response)
        self.assertEqual(response, [])

    def test_get_org_tags(self):
        sample = {'text': 'Browns', 'type': 'ORG', 'start_char': 13, 'end_char': 19}
        response = self.sport_handler.get_team_and_league_tags_on_team(sample)
        print(response)
        valid_response = [{'type': 'team', 'value': 'Cleveland Browns'}, {'type': 'league', 'value': 'nfl'}]
        self.assertEqual(response, valid_response)

    def test_get_org_tags_mlb(self):
        sample = {'text': 'Yankees', 'type': 'ORG', 'start_char': 13, 'end_char': 19}
        response = self.sport_handler.get_team_and_league_tags_on_team(sample)
        print(response)
        valid_response = [{'type': 'team', 'value': 'New York Yankees'}, {'type': 'league', 'value': 'mlb'}]
        self.assertEqual(response, valid_response)

    def test_get_team_and_league_tags_on_player_or_coach(self):
        sample = {'text': 'Cam Bedrosian', 'type': 'PERSON', 'start_char': 13, 'end_char': 19}
        response = self.sport_handler.get_team_player_league_tags_on_player_or_coach(sample,
                                                                                     self.sport_handler.util.sports_player_dict)
        print("AYOO", response)
        valid_response = [{'type': 'team', 'value': 'Los Angeles Angels'}, {'type': 'league', 'value': 'mlb'},
                          {'type': 'person', 'value': 'Cam Bedrosian'}]
        self.assertCountEqual(response, valid_response)

    def test_get_sport_terms_tags_baseball(self):
        sample = {'text': 'caught napping', 'type': 'UNKNOWN', 'start_char': 13, 'end_char': 19}
        response = self.sport_handler.get_sports_terms_tag(sample)
        print(response)
        valid_response = [{'type': 'sport', 'value': 'baseball'}]
        self.assertCountEqual(response, valid_response)

    def test_tag_generator_punctuation(self):
        sample_input = {'text': "Tom Brady'", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        response = self.sport_handler.get_tags_using_sports_dict(sample_input)
        print(response)
        valid_response = [{'type': 'team', 'value': 'New England Patriots'}, {'type': 'person', 'value': "Tom Brady"},
                          {'type': 'league', 'value': 'nfl'}]
        self.assertCountEqual(response, valid_response)

    def test_tag_generator_no_punctuation(self):
        sample_input = {'text': "Tom Brady", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        response = self.sport_handler.get_tags_using_sports_dict(sample_input)
        print(response)
        valid_response = [{'type': 'team', 'value': 'New England Patriots'}, {'type': 'person', 'value': "Tom Brady"},
                          {'type': 'league', 'value': 'nfl'}]
        self.assertCountEqual(response, valid_response)

    def test_integration_generate_sports_tags(self):
        sample = "Hello this is Austin Marchese and this is the Banter Podcast."
        valid_output = [{'type': 'person', 'value': 'Austin Marchese'}]
        response = self.sport_handler.generate_sports_tags(sample)
        self.assertCountEqual(response, valid_output)

    def test_get_sport_and_person_tags_on_non_team_sport(self):
        sample_input = {'text': "Jordan Spieth", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        valid_output = [{'type': 'person', 'value': 'Jordan Spieth'}, {'type': 'sport', 'value': 'golf'}]
        response = self.sport_handler.get_sport_and_person_tags_on_non_team_sport(sample_input,
                                                                                  self.sport_handler.util.individual_sports_dict)
        self.assertCountEqual(response, valid_output)

    def test_get_sport_and_person_tags_on_non_team_sport_foreign_name(self):
        sample_input = {'text': "Benjamín Alvarado", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        valid_output = [{'type': 'person', 'value': 'Benjamín Alvarado'}, {'type': 'sport', 'value': 'golf'}]
        response = self.sport_handler.get_sport_and_person_tags_on_non_team_sport(sample_input,
                                                                                  self.sport_handler.util.individual_sports_dict)
        self.assertCountEqual(response, valid_output)

    def test_get_sports_tags_specific_test(self):
        description = "NYG-DAL"
        desired_tags = [{"type": "team", "value": "Dallas Cowboys"}, {"type": "league", "value": "nfl"}, {"type": "team", "value": "New York Giants"}]
        response = self.sport_handler.get_sports_tags(description)
        self.assertCountEqual(response, desired_tags)

    def test_check_if_game_matchup(self):
        key_word = {'text': "NYG@MIN", 'type': 'ORG', 'start_char': 94, 'end_char': 104}
        self.assertTrue(self.sport_handler.check_if_game_matchup(key_word))

    def test_get_matchup_tags(self):
        """
        Duplicate tags is fine as this is handled in seperate methods
        """
        key_word = {'text': "NYG@DAL", 'type': 'ORG', 'start_char': 94, 'end_char': 104}
        desired_tags = [{"type": "team", "value": "Dallas Cowboys"}, {"type": "league", "value": "nfl"}, {"type": "team", "value": "New York Giants"},{"type": "league", "value": "nfl"}]
        response = self.sport_handler.get_matchup_tags(key_word)
        self.assertCountEqual(response, desired_tags)

    # @unittest.skip("Skip when testing locally, this is a full integration test, uncomment in production")
    def test_get_sports_tags_full_test(self):
        for (description, desired_tags) in self.integration_test_fixture.items():
            response = self.sport_handler.get_sports_tags(description)
            print(response, description)
            self.assertCountEqual(response, desired_tags)



if __name__ == '__main__':
    unittest.main()
