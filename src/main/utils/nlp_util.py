from typing import *

import stanza
from nltk.tokenize import word_tokenize
from stanza import Document

from src.main.utils.decorators import debug
from src.main.utils.nlp_conversion_util import NLPConversionUtil
from src.main.utils.nlp_resource_util import NLPResourceUtil


# TODO Uncomment
stanza.download('en')  # download English model

class NLPUtil(NLPConversionUtil, NLPResourceUtil):
    nlp = stanza.Pipeline(lang='en', processors="TOKENIZE,POS,NER")
    # This sets up a default neural pipeline in English
    word_tokenize = word_tokenize

    def get_token_dict_from_nlp(self, nlp_response: Document) -> List[Dict[str, str]]:
        """
        Take a summary provided from a podcast and return a tokenized dictionary
        """
        token_span_list = nlp_response.entities
        token_dict_list: List[Dict[str, str]] = self.convert_span_list_to_dict_list(token_span_list)
        return token_dict_list

    def get_nlp_response(self, str_: str) -> Document:
        return self.nlp(str_)

    @staticmethod
    def is_description_below_max_words(str_: str, max_words: int) -> bool:
        return len(str_.split(' ')) < max_words

    # TODO Consider the Following TB12 is considered a noun, AB is considered a proper noun
    # TODO Allowing for nouns open ups a can of worms
    @staticmethod
    def check_if_token_is_relevant(token, language_types_analyzed: Set[str]) -> bool:
        # Checking if we care about the upos (NOUN, PRONOUN, Etc.) Also Checking for Duplicates
        if token['upos'] not in language_types_analyzed:
            return False
        return True

    @staticmethod
    def is_token_specific_type(token_dict: Dict, type: str) -> bool:
        return token_dict["type"] == type

    @staticmethod
    def check_if_token_is_new(token, token_set: Set, token_concat_str: str) -> bool:
        if token['text'] in token_set:
            # Above checks for an EXACT Match, however St.Louis Rams gets tokenized as St.Louis Rams
            # But each St. , Louis, Rams, are all technically different parts of speach.
            # As a result, a token_concat_str is created and it just looks to see if it contains a sub string
            return False
        # TODO this probably fucks some edge scenarios up
        if token['text'] in token_concat_str:
            return False
        return True

    def get_important_pos_tags_from_sentence(self, nlp_response_list: List[List[Dict[str, str]]], token_set: Set,
                                             token_concat_str: str) -> List[Dict]:
        """
        :param nlp_response_list: needs to be the nlp_response in dict format ---input nlp_response.to_dict()
                                where nlp response is type: Document
        :param token_set:
        :param token_concat_str:
        UPOS - Universal POS Tags
        :return: List of important nouns with the text and the type
        """
        noun_list = []
        for index, sentence in enumerate(nlp_response_list):
            for token in sentence:
                if self.check_if_token_is_relevant(token, self.language_types_analyzed) \
                        and self.check_if_token_is_new(token, token_set, token_concat_str):
                    # Creating noun dict to match with entities dict
                    noun = {"text": token['text'], "type": token['upos']}
                    noun_list.append(noun)
        return noun_list

    def get_token_dict_manual(self, _str: str):
        """
        This is used to determine the tokens without using standford nlp
        :return: dict
        """
        # Tokenizing Data, breaks up into words/ phrases
        token_dict_list = []
        token_list = self.word_tokenize(_str)
        # Removing Stop words and punctuation from data
        clean_data = self.remove_stop_words_and_punctuation(token_list)

        for word in clean_data:
            token_dict_list.append({"text": word, "type": "UNKNOWN"})

        return token_dict_list

    # TODO Write Test
    @debug
    def get_key_word_dict(self, str_: str) -> List[Dict]:
        is_descption_too_long: bool = self.is_description_below_max_words(str_, self.max_description)
        if is_descption_too_long:
            nlp_response = self.get_nlp_response(str_)
            token_dict_list = self.get_token_dict_from_nlp(nlp_response)
            all_tokens_as_string: str = ''
            token_dict_list, token_set, token_concat_str = self.filter_tokens_get_unique_text(token_dict_list,
                                                                                              self.token_types_analyzed)
            for token in token_dict_list:
                all_tokens_as_string += token['text']
            token_dict_list += self.get_important_pos_tags_from_sentence(nlp_response.to_dict(), token_set,
                                                                         token_concat_str)
            return token_dict_list
        else:
            print("Description is Too Long")
            return []

    # @staticmethod
    # # TODO Handle multiple leagues discussed
    # def get_value_of_specified_type(tokens: List[TagModel], type_: str) -> str:
    #     for token in tokens:
    #         if token['type'] == type_:
    #             return token['value']
    #     return ''
