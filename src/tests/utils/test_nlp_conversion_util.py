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

    def test_remove_prefix_from_word(self):
        nlp_entity = {"type": "ORG", "text": "THE CLEVELAND BROWNS"}
        self.assertEqual({"type": "ORG", "text": "CLEVELAND BROWNS"},
                         NLPConversionUtil().remove_prefix_from_word(nlp_entity))

    def test_remove_duplicates_from_dict_list(self):
        sample_dict = [{"type": "name", "value": "Austin"}, {"type": "name", "value": "Jesse"},
                       {"type": "name", "value": "Jesse"}]
        self.assertEqual(2, len(NLPConversionUtil.remove_duplicates_from_dict_list_based_on_key(sample_dict)))

    def test_filter_tokens_get_unique_text(self):
        sample_dict = [{"type": "PERSON", "text": "AUSTIN"}, {"type": "PERSON", "text": "LEBRON JAMES STARS"},
                       {"type": "ORG", "text": "JESSE"},
                       {"type": "ORG", "text": "JESSE"}, {"type": "NOT_IMPORTANT", "text": "JESSE"}]
        response, token_set, token_concat_str = NLPConversionUtil().filter_nlp_entities_and_create_unique_entity_reference(
            sample_dict,
            {"PERSON"})
        self.assertEqual(response,
                         [{'type': 'PERSON', 'text': 'AUSTIN'}, {'type': 'PERSON', 'text': 'LEBRON JAMES STARS'},
                          {'type': 'PERSON', 'text': 'LEBRON JAMES'}])
        self.assertTrue('AUSTIN' in token_set)
        self.assertTrue('LEBRON JAMES STARS' in token_set)
        self.assertEqual(token_concat_str, 'AUSTINLEBRON JAMES STARS')

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

    def test_normalize_name(self):
        self.assertEqual("AJ GREEN", NLPConversionUtil().normalize_text("A.J. GreEn Jr. Sr. III ii, iii '!?"))
        self.assertEqual("LEBRON JAMES", NLPConversionUtil().normalize_text(" Lebron JAmes "))
        self.assertEqual("LAURIE AYTON", NLPConversionUtil().normalize_text("Laurie Ayton Jnr Snr jnr. snr."))
        self.assertEqual("NYG@MIN", NLPConversionUtil().normalize_text("NYG@MIN"))
        self.assertEqual("AJ GREEN", NLPConversionUtil().normalize_text("A.J. Green's"))

    def test_normalize_names_in_entity_list(self):
        sample_dict = [{"type": "PERSON", "text": "Austin"}, {"type": "PERSON", "text": "Lebron James Stars"},
                       {"type": "PERSON", "text": "Lebron James Jr. Sr. iii, III"},
                       {"type": "ORG", "text": "Jesse"},
                       {"type": "ORG", "text": "Jesse"}, {"type": "NOT_IMPORTANT", "text": "Jesse"}]
        response = NLPConversionUtil().normalize_entity_list(sample_dict)
        expected = [{'type': 'PERSON', 'text': 'AUSTIN'}, {'type': 'PERSON', 'text': 'LEBRON JAMES STARS'},
                    {'type': 'PERSON', 'text': 'LEBRON JAMES'}, {"type": "ORG", "text": "JESSE"},
                    {"type": "ORG", "text": "JESSE"}, {"type": "NOT_IMPORTANT", "text": "JESSE"}]
        self.assertEqual(response, expected)

    def test_convert_tags_to_capital_case(self):
        tag = [{"type": "person", "value": "LEBRON JAMES"}]
        expected = [{"type": "person", "value": "Lebron James"}]
        response = NLPConversionUtil().conver_non_league_tags_to_Title_Case_and_format_names(tag)
        self.assertEqual(expected, response)
        tag = [{"type": "league", "value": "NFL"}]
        expected = [{"type": "league", "value": "NFL"}]
        response = NLPConversionUtil().conver_non_league_tags_to_Title_Case_and_format_names(tag)
        self.assertEqual(expected, response)

    def test_format_names(self):
        response = NLPConversionUtil().format_name("AJ GREEN")
        expected = "AJ Green"
        self.assertEqual(expected, response)
        response = NLPConversionUtil().format_name("LEBRON JAMES")
        expected = "Lebron James"
        self.assertEqual(expected, response)
        response = NLPConversionUtil().format_name("AJ GREEN JAMES")
        expected = "AJ Green James"
        self.assertEqual(expected, response)

    def test_alter_tags_to_proper_response_format(self):
        tag = [{"type": "person", "value": "LEBRON JAMES"}, {"type": "person", "value": "LEBRON JAMES"},
               {"type": "team", "value": "LOS ANGELES LAKERS"}]
        expected = [{"type": "person", "value": "Lebron James"}, {"type": "team", "value": "Los Angeles Lakers"}]
        response = NLPConversionUtil().alter_tags_to_proper_response_format(tag)
        self.assertEqual(expected, response)


if __name__ == '__main__':
    unittest.main()
