import unittest

from src.main.utils.nlp_conversion_util import NLPConversionUtil


class TestNLPConversionUtil(unittest.TestCase):
    starting_dict = {"ab": "cd"}

    def test_filter_stop_words_and_punctuation(self):
        word_list = ['abcd', "a", "'", "austin"]
        self.assertEqual(2, len(NLPConversionUtil.remove_stop_words_and_punctuation(word_list)))

    def test_filter_duplicates_from_list(self):
        word_list = ['abcd', "a", "'", "austin", "austin"]
        self.assertEqual(4, len(NLPConversionUtil.remove_duplicates_from_list(word_list)))
        word_list = ['abcd', "a", "'", "austin"]
        self.assertEqual(4, len(NLPConversionUtil.remove_duplicates_from_list(word_list)))

    def test_filter_token_list_by_type(self):
        word_list = [{"type": 'PERSON'}, {"type": 'ORG'}, {"type": 'ORG'}]
        self.assertEqual(1, len(NLPConversionUtil.filter_token_list_by_type(word_list, "PERSON")))

    def test_remove_punctuation_from_text(self):
        sample_str = "My name's austin"
        self.assertEqual("My names austin", NLPConversionUtil.remove_punctuation_from_text(sample_str))

    def test_remove_duplicates_from_dict_list(self):
        sample_dict = [{"type": "name", "value": "Austin"}, {"type": "name", "value": "Jesse"},
                       {"type": "name", "value": "Jesse"}]
        self.assertEqual(2, len(NLPConversionUtil.remove_duplicates_from_dict_list_based_on_key(sample_dict)))

    def test_filter_tokens_get_unique_text(self):
        sample_dict = [{"type": "PERSON", "text": "Austin"}, {"type": "PERSON", "text": "Lebron James Stars"},
                       {"type": "ORG", "text": "Jesse"},
                       {"type": "ORG", "text": "Jesse"}, {"type": "NOT_IMPORTANT", "text": "Jesse"}]
        response, token_set, token_concat_str = NLPConversionUtil().filter_nlp_entities_and_create_unique_entity_reference(
            sample_dict,
            {"PERSON"})
        self.assertEqual(response,
                         [{'type': 'PERSON', 'text': 'Austin'}, {'type': 'PERSON', 'text': 'Lebron James Stars'},
                          {'type': 'PERSON', 'text': 'Lebron James'}])
        self.assertTrue('Austin' in token_set)
        self.assertTrue('Lebron James Stars' in token_set)
        self.assertEqual(token_concat_str, 'AustinLebron James Stars')

    def test_remove_extra_word_from_name(self):
        sample_dict = {"type": "PERSON", "text": "Lebron James Stars"}
        expected_response = {"type": "PERSON", "text": "Lebron James"}
        response = NLPConversionUtil().remove_extra_word_from_name(sample_dict)
        self.assertCountEqual(response, expected_response)

    def test_append_to_existing_dict(self):
        expected = {"ab": "ce"}
        response = NLPConversionUtil.append_to_existing_dict("ab", "ce", self.starting_dict)
        self.assertEqual(expected, response)

    def test_remove_word_from_key_word_text(self):
        sample_dict = {'text': 'the Cleveland Browns', 'type': 'ORG', 'start_char': 46, 'end_char': 66}
        expected = {'text': 'Cleveland Browns', 'type': 'ORG', 'start_char': 46, 'end_char': 66}
        response = NLPConversionUtil.remove_non_capitalized_words_from_nlp_entity_text(sample_dict)
        self.assertEqual(expected, response)

    def test_remove_non_capitalized_words(self):
        self.assertEqual("Abc Def", NLPConversionUtil.remove_non_capitalized_words("Abc Def abd"))

    # def test_add_tag_to_tag_list(self):
    #     tag_list = [{'type': 'team', 'value': 'New York Knicks', 'confidence':1.0}, {'type': 'person', 'value': 'Dennis Smith Jr.', 'confidence':1.0}, {'type': 'league', 'value': 'nba', 'confidence':1.0}, {'type': 'team', 'value': 'Los Angeles Lakers', 'confidence':1.0}, {'type': 'league', 'value': 'nba', 'confidence':1.0}, {'type': 'team', 'value': 'Oklahoma City Thunder', 'confidence':1.0}, {'type': 'league', 'value': 'nba', 'confidence': 1.0}, {'type': 'team', 'value': 'Oklahoma City Thunder', 'confidence':1.0}, {'type': 'person', 'value': 'Terrance Ferguson', 'confidence':1.0}, {'type': 'league', 'value': 'nba', 'confidence':1.0}]
    #     new_tag_list = NLPConversionUtil.add_tag_to_tag_list(tag_list, type="ab",value="value", confidence=1.0)


if __name__ == '__main__':
    unittest.main()
