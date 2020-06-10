import unittest

from src.main.utils.nlp_util import NLPUtil


class TestNLPUtil(unittest.TestCase):
    starting_dict = {"ab": "cd"}
    span_list = []
    sample_token = {'id': '1', 'text': 'Tom', 'upos': 'PROPN', 'xpos': 'NNP', 'feats': 'Number=Sing',
                    'misc': 'start_char=0|end_char=3'}
    sample_nlp_response_list = [[{'id': '1', 'text': 'Tom', 'upos': 'PROPN', 'xpos': 'NNP', 'feats': 'Number=Sing',
                                  'misc': 'start_char=0|end_char=3'},
                                 {'id': '2', 'text': 'Brady', 'upos': 'PROPN', 'xpos': 'NNP', 'feats': 'Number=Sing',
                                  'misc': 'start_char=4|end_char=9'}], [
                                    {'id': '1', 'text': 'Is', 'upos': 'AUX', 'xpos': 'VBZ',
                                     'feats': 'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin',
                                     'misc': 'start_char=10|end_char=12'},
                                    {'id': '2', 'text': 'the', 'upos': 'DET', 'xpos': 'DT',
                                     'feats': 'Definite=Def|PronType=Art', 'misc': 'start_char=13|end_char=16'},
                                    {'id': '3', 'text': 'greates', 'upos': 'NOUN', 'xpos': 'NNS',
                                     'feats': 'Number=Plur', 'misc': 'start_char=17|end_char=24'},
                                    {'id': '4', 'text': 'of', 'upos': 'ADP', 'xpos': 'IN',
                                     'misc': 'start_char=25|end_char=27'},
                                    {'id': '5', 'text': 'all', 'upos': 'DET', 'xpos': 'DT',
                                     'misc': 'start_char=28|end_char=31'},
                                    {'id': '6', 'text': 'time', 'upos': 'NOUN', 'xpos': 'NN', 'feats': 'Number=Sing',
                                     'misc': 'start_char=32|end_char=36'},
                                    {'id': '7', 'text': '.', 'upos': 'PUNCT', 'xpos': '.',
                                     'misc': 'start_char=36|end_char=37'}], [
                                    {'id': '1', 'text': 'Jared', 'upos': 'PROPN', 'xpos': 'NNP', 'feats': 'Number=Sing',
                                     'misc': 'start_char=38|end_char=43'},
                                    {'id': '2', 'text': 'is', 'upos': 'AUX', 'xpos': 'VBZ',
                                     'feats': 'Mood=Ind|Number=Sing|Person=3|Tense=Pres|VerbForm=Fin',
                                     'misc': 'start_char=44|end_char=46'},
                                    {'id': '3', 'text': 'the', 'upos': 'DET', 'xpos': 'DT',
                                     'feats': 'Definite=Def|PronType=Art', 'misc': 'start_char=47|end_char=50'},
                                    {'id': '4', 'text': 'quarterback', 'upos': 'NOUN', 'xpos': 'NN',
                                     'feats': 'Number=Sing', 'misc': 'start_char=51|end_char=62'},
                                    {'id': '5', 'text': 'for', 'upos': 'ADP', 'xpos': 'IN',
                                     'misc': 'start_char=63|end_char=66'},
                                    {'id': '6', 'text': 'the', 'upos': 'DET', 'xpos': 'DT',
                                     'feats': 'Definite=Def|PronType=Art', 'misc': 'start_char=67|end_char=70'},
                                    {'id': '7', 'text': 'Rams', 'upos': 'PROPN', 'xpos': 'NNPS', 'feats': 'Number=Plur',
                                     'misc': 'start_char=71|end_char=75'}]]

    @classmethod
    def setUpClass(cls):
        cls.nlp_util = NLPUtil()

    def test_convert_span_to_dict(self):
        response = self.nlp_util.get_nlp_response("Austin Marchese is the man")
        self.assertIsNotNone(response.entities, "Asserting response for specified text string")

    def test_is_description_too_long_above(self):
        response = self.nlp_util.is_description_too_long_or_empty("ABC DEF GED", 2)
        self.assertEqual(True, response)

    def test_is_description_too_long_empty(self):
        response = self.nlp_util.is_description_too_long_or_empty("", 2)
        self.assertEqual(True, response)

    def test_is_description_too_long_below(self):
        response = self.nlp_util.is_description_too_long_or_empty("ABC", 4)
        self.assertEqual(False, response)

    def test_check_if_token_is_relevant_not_relevent(self):
        self.assertFalse(NLPUtil.is_nlp_entity_important_language_type(self.sample_token, {"NOUN"}))

    def test_check_if_token_is_relevant_relevent(self):
        self.assertTrue(NLPUtil.is_nlp_entity_important_language_type(self.sample_token, {"PROPN"}))

    def test_has_nlp_entity_already_been_analyzed_new(self):
        token_set = set()
        token_set.add("Brian")
        self.assertFalse(self.nlp_util.has_nlp_entity_already_been_analyzed(self.sample_token, token_set, "AbcdEfghi"))

    def test_has_nlp_entity_already_been_analyzed_not_new(self):
        token_set = set()
        token_set.add("Tom")
        self.assertTrue(self.nlp_util.has_nlp_entity_already_been_analyzed(self.sample_token, token_set, "AbcdEfghi"))

    def test_check_if_token_is_new_not_new_in_token_concat_str(self):
        token_set = set()
        token_set.add("Brian")
        self.assertTrue(
            self.nlp_util.has_nlp_entity_already_been_analyzed(self.sample_token, token_set, "TomBrianSteve"))

    def test_should_nlp_entity_be_analyzed_true(self):
        token_set = set()
        token_set.add("Brian")
        self.assertTrue(
            self.nlp_util.should_nlp_entity_be_analyzed(self.sample_token, {"PROPN"}, token_set, "AbcdEfghi"))

    def test_should_nlp_entity_be_analyzed_false(self):
        token_set = set()
        token_set.add("Brian")
        self.assertFalse(
            self.nlp_util.should_nlp_entity_be_analyzed(self.sample_token, {"NOUN"}, token_set, "AbcdEfghi"))

    # TODO mock nested method response
    def test_get_nouns_from_sentence(self):
        token_set = set()
        response = self.nlp_util.get_important_pos_tags_from_sentence(self.sample_nlp_response_list, token_set,
                                                                      "ABCDEFG")
        self.assertEqual(4, len(response))

    def test_get_nouns_from_sentence_token_in_set(self):
        token_set = set()
        token_set.add("Brady")
        response = self.nlp_util.get_important_pos_tags_from_sentence(self.sample_nlp_response_list, token_set,
                                                                      "ABCDEFG")
        self.assertEqual(3, len(response))

    def test_get_nouns_from_sentence_token_not_in_set(self):
        token_set = set()
        token_set.add("Jared Goff")
        response = self.nlp_util.get_important_pos_tags_from_sentence(self.sample_nlp_response_list, token_set,
                                                                      "ABCDEFG")
        self.assertEqual(4, len(response))

    def test_get_normalized_and_filtered_nlp_entities(self):
        # IMPROVE
        response = self.nlp_util.get_normalized_and_filtered_nlp_entities(
            'On This Weeks Episode we are going to discuss the Cleveland Browns')
        print(response)
        expected = [{'end_char': 66,
                     'start_char': 46,
                     'text': 'THE CLEVELAND BROWNS',
                     'type': 'ORG'}]
        self.assertEqual(response, expected)

    def test_get_nouns_from_sentence_token_in_concat_str(self):
        token_set = set()
        token_set.add("Jared Goff")
        response = self.nlp_util.get_important_pos_tags_from_sentence(self.sample_nlp_response_list, token_set,
                                                                      "JaredGoff")
        self.assertEqual(3, len(response))

    def test_is_token_specific_type(self):
        token = {"type": "PERSON"}
        self.assertTrue(self.nlp_util.is_nlp_entity_specific_type(token, "PERSON"))
