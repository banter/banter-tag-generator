from src.main.tag_identifier import TagIdentifier
import unittest
test_list = ["Cowboys lose Browns bounce back",
"Bucs win",
"TB12 declining?",
"Burfict suspended"]

class TestTagIdentifier(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        super(TestTagIdentifier, self).setUpClass()
        self.tag_identifier = TagIdentifier()

    def test_generate_sports_tags(self):

        sample = "Hello this is Austin Marchese and this is the Banter Podcast."
        response = self.tag_identifier.generate_sports_tags(sample)
        print(response)
        # TODO fix test
        self.assertIsNotNone(response)


    def test_generate_sports_tags_empty(self):

        sample = "ajbfasd askdhasd sdkja"
        response = self.tag_identifier.generate_sports_tags(sample)
        print(response)
        self.assertEqual(response, [])

    def test_generate_tags_non_specific(self):
        sample = "Hello this is Austin Marchese and this is the Banter Podcast."
        response = self.tag_identifier.generate_tags_non_specific(sample)
        print(response)
        self.assertEqual(response, [])

    def test_get_org_tags(self):
        sample = {'text': 'Browns', 'type': 'ORG', 'start_char': 13, 'end_char': 19}
        response = self.tag_identifier.get_team_and_league_tags_on_team(sample)
        print(response)
        valid_response = [{'type': 'team', 'value': 'Cleveland Browns'},{'type': 'league', 'value': 'nfl'}]
        self.assertEqual(response, valid_response)

    def test_get_org_tags_mlb(self):
        sample = {'text': 'Yankees', 'type': 'ORG', 'start_char': 13, 'end_char': 19}
        response = self.tag_identifier.get_team_and_league_tags_on_team(sample)
        print(response)
        valid_response = [{'type': 'team', 'value': 'New York Yankees'},{'type': 'league', 'value': 'mlb'}]
        self.assertEqual(response, valid_response)

    def test_get_team_and_league_tags_on_player_or_coach(self):
        sample = {'text': 'Cam Bedrosian', 'type': 'PERSON', 'start_char': 13, 'end_char': 19}
        response = self.tag_identifier.get_team_player_league_tags_on_player_or_coach(sample, self.tag_identifier.util.sports_player_dict)
        print("AYOO", response)
        valid_response = [{'type': 'team', 'value': 'Los Angeles Angels'},{'type': 'league', 'value': 'mlb'}, {'type': 'person', 'value' :'Cam Bedrosian'}]
        self.assertCountEqual(response, valid_response)

    def test_get_person_tags(self):
        sample = {'text': 'Cam Bedrosian', 'type': 'PERSON', 'start_char': 13, 'end_char': 19}
        response = self.tag_identifier.get_person_tags(sample)
        print("AYOO", response)
        valid_response = [{'type': 'person', 'value' :'Cam Bedrosian'}]
        self.assertCountEqual(response, valid_response)

    def test_get_sport_terms_tags_mlb(self):
        sample = {'text': 'caught nappin', 'type': 'UNKNOWN', 'start_char': 13, 'end_char': 19}
        response = self.tag_identifier.get_sports_terms_tag(sample)
        print(response)
        valid_response = [{'type': 'sport', 'value': 'baseball'}]
        self.assertCountEqual(response, valid_response)

    def test_tag_generator_punctuation(self):
        sample_input = {'text': "Tom Brady'", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        response = self.tag_identifier.get_tags_using_sports_dict(sample_input)
        print(response)
        valid_response = [{'type': 'team', 'value': 'New England Patriots'}, {'type': 'person', 'value': "Tom Brady"}, {'type': 'league', 'value': 'nfl'}]
        self.assertCountEqual(response, valid_response)

    def test_tag_generator_no_punctuation(self):
        sample_input = {'text': "Tom Brady", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        response = self.tag_identifier.get_tags_using_sports_dict(sample_input)
        print(response)
        valid_response = [{'type': 'team', 'value': 'New England Patriots'}, {'type': 'person', 'value': "Tom Brady"},
                          {'type': 'league', 'value': 'nfl'}]
        self.assertCountEqual(response, valid_response)


    def test_integration_generate_sports_tags(self):
        sample = "Hello this is Austin Marchese and this is the Banter Podcast."
        valid_output = [{'type': 'person', 'value': 'Austin Marchese'}]
        response = self.tag_identifier.generate_sports_tags(sample)
        self.assertCountEqual(response, valid_output)


