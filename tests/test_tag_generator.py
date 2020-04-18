from basic_topic_identifier import GenerateTags
import unittest

test_list = ["Cowboys lose Browns bounce back",
"Bucs win",
"TB12 declining?",
"Burfict suspended"]

class TestGenerateTags(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        super(TestGenerateTags, self).setUpClass()
        self.generate_tags = GenerateTags()


    def test_get_token_dict_valid(self):

        sample = "Hello this is Austin Marchese and this is the Banter Podcast."
        response = self.generate_tags.get_token_dict(sample)
        print(response)
        # TODO fix test
        self.assertIsNotNone(response)


    def test_get_token_dict_empty(self):

        sample = "ajbfasd askdhasd sdkja"
        response = self.generate_tags.get_token_dict(sample)
        print(response)
        self.assertEqual(response, [])

    def test_get_token_dict_manual(self):

        sample = "TB12 declining?"
        response = self.generate_tags.get_token_dict_manual(sample)
        print(response)
        valid_response = [{"text": "TB12", "type": "UNKNOWN"},{"text": "declining", "type": "UNKNOWN"}]

        self.assertEqual(response, valid_response)

    def test_get_org_tags(self):
        sample = {'text': 'Browns', 'type': 'ORG', 'start_char': 13, 'end_char': 19}
        response = self.generate_tags.get_team_tags(sample)
        print(response)
        valid_response = [{'type': 'team', 'value': 'Cleveland Browns'},{'type': 'league', 'value': 'nfl'}]
        self.assertEqual(response, valid_response)

    def test_get_org_tags_mlb(self):
        sample = {'text': 'Yankees', 'type': 'ORG', 'start_char': 13, 'end_char': 19}
        response = self.generate_tags.get_team_tags(sample)
        print(response)
        valid_response = [{'type': 'team', 'value': 'New York Yankees'},{'type': 'league', 'value': 'mlb'}]
        self.assertEqual(response, valid_response)

    def test_get_player_tags_mlb(self):
        sample = {'text': 'Cam Bedrosian', 'type': 'PERSON', 'start_char': 13, 'end_char': 19}
        response = self.generate_tags.get_person_tags(sample)
        print(response)
        valid_response = [{'type': 'team', 'value': 'Los Angeles Angels'},{'type': 'league', 'value': 'mlb'}, {'type': 'person', 'value': 'Cam Bedrosian'}]
        self.assertCountEqual(response, valid_response)


    def test_get_sport_terms_tags_mlb(self):
        sample = {'text': 'caught nappin', 'type': 'UNKNOWN', 'start_char': 13, 'end_char': 19}
        response = self.generate_tags.get_sports_terms_tag(sample)
        print(response)
        valid_response = [{'type': 'sport', 'value': 'baseball'}]
        self.assertCountEqual(response, valid_response)

    def test_get_google_search_results(self):

        sample = "TB12"
        response = self.generate_tags.get_google_search_results(sample)
        print(response)
        valid_response = "['', '', 'The TB12 Method: How to Achieve a Lifetime of Sustained Peak Performance', 'Book by Tom Brady']"
        self.assertCountEqual(response, valid_response)


    def test_get_google_search_results_bucs(self):

        sample = "Bucs"
        response = self.generate_tags.get_google_search_results(sample)
        print(response)

        self.assertNotEqual(response, [])

    def test_tag_generator_punctuation(self):
        sample_input = {'text': "Tom Brady'", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        response = self.generate_tags.get_tags_using_dict(sample_input)
        print(response)
        valid_response = [{'type': 'team', 'value': 'New England Patriots'}, {'type': 'person', 'value': "Tom Brady'"}, {'type': 'league', 'value': 'nfl'}]
        self.assertCountEqual(response, valid_response)

    def test_tag_generator_no_punctuation(self):
        sample_input = {'text': "Tom Brady", 'type': 'PERSON', 'start_char': 94, 'end_char': 104}
        response = self.generate_tags.get_tags_using_dict(sample_input)
        print(response)
        valid_response = [{'type': 'team', 'value': 'New England Patriots'}, {'type': 'person', 'value': "Tom Brady'"},
                          {'type': 'league', 'value': 'nfl'}]
        self.assertCountEqual(response, valid_response)