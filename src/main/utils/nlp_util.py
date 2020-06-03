import os
from typing import *

import stanza
from nltk.tokenize import word_tokenize
from stanza import Document

from src.main.models.tag_model import NLPEntityModel
from src.main.utils.decorators import debug
from src.main.utils.nlp_conversion_util import NLPConversionUtil
from src.main.utils.nlp_resource_util import NLPResourceUtil

a = os.popen('hostname').read()

if 'Austin' not in a:
    stanza.download('en')  # download English model


class NLPUtil(NLPConversionUtil, NLPResourceUtil):
    nlp = stanza.Pipeline(lang='en', processors="TOKENIZE,POS,NER")
    # This sets up a default neural pipeline in English
    word_tokenize = word_tokenize

    def get_nlp_entities_from_nlp_response(self, nlp_response: Document) -> List[NLPEntityModel]:
        """
        Take a summary provided from a podcast and return a tokenized dictionary
        """
        nlp_entity_list_span = nlp_response.entities
        nlp_entity_list: List[NLPEntityModel] = self.convert_span_list_to_dict_list(nlp_entity_list_span)
        return nlp_entity_list

    def get_nlp_response(self, str_: str) -> Document:
        return self.nlp(str_)

    @staticmethod
    def is_description_too_long_or_empty(str_: str, max_words: int) -> bool:
        if len(str_) == 0:
            return True
        return len(str_.split(' ')) > max_words

    @staticmethod
    def is_nlp_entity_specific_type(nlp_entity: NLPEntityModel, type: str) -> bool:
        return nlp_entity["type"] == type

    # TODO Consider the Following TB12 is considered a noun, AB is considered a proper noun
    # TODO Allowing for nouns open ups a can of worms
    @staticmethod
    def is_nlp_entity_important_language_type(nlp_entity: NLPEntityModel, language_types_analyzed: Set[str]) -> bool:
        # Checking if we care about the upos (NOUN, PRONOUN, Etc.) Also Checking for Duplicates
        return nlp_entity['upos'] in language_types_analyzed

    def should_nlp_entity_be_analyzed(self, nlp_entity: NLPEntityModel, language_types_analyzed: Set[str],
                                      analyzed_entities_set: Set, analyzed_entities_str: str) -> bool:
        if self.is_nlp_entity_important_language_type(nlp_entity, language_types_analyzed) is False:
            return False
        if self.has_nlp_entity_already_been_analyzed(nlp_entity, analyzed_entities_set, analyzed_entities_str):
            return False
        return True

    @staticmethod
    def has_nlp_entity_already_been_analyzed(nlp_entity: NLPEntityModel, analyzed_entities_set: Set,
                                             analyzed_entities_str: str) -> bool:
        # Above checks for an EXACT Match, however St.Louis Rams gets tokenized as St.Louis Rams
        # But each St. , Louis, Rams, are all technically different parts of speach.
        # As a result, a token_concat_str is created and it just looks to see if it contains a sub string
        # return nlp_entity["text"] not in analyzed_entities_set or nlp_entity["text"] not in analyzed_entities_str
        nlp_entity_text = nlp_entity['text']
        if nlp_entity_text in analyzed_entities_set:
            return True
        # TODO this probably fucks some edge scenarios up
        if nlp_entity_text in analyzed_entities_str:
            return True
        return False

    def get_important_pos_tags_from_sentence(self, nlp_response_list: List[List[NLPEntityModel]],
                                             analyzed_entities_set: Set,
                                             analyzed_entities_str: str) -> List[NLPEntityModel]:
        """
        :param nlp_response_list: needs to be the nlp_response in dict format ---input nlp_response.to_dict()
                                where nlp response is type: Document
        :param analyzed_entities_set:
        :param analyzed_entities_str:
        UPOS - Universal POS Tags
        :return: List of important nouns with the text and the type
        """
        important_nlp_entity_list = []
        for index, sentence in enumerate(nlp_response_list):
            for entity in sentence:
                if self.should_nlp_entity_be_analyzed(entity, self.language_types_analyzed,
                                                      analyzed_entities_set, analyzed_entities_str):
                    # Creating noun dict to match with entities dict
                    nlp_entity = {"text": entity['text'], "type": entity['upos']}
                    important_nlp_entity_list.append(nlp_entity)
        return important_nlp_entity_list

    def get_entity_list_manually(self, _str: str):
        """
        This is used to determine the tokens without using standford nlp
        :return: dict
        """
        # Tokenizing Data, breaks up into words/ phrases
        entity_list = []
        token_list = self.word_tokenize(_str)
        # Removing Stop words and punctuation from data
        clean_token_list = self.remove_stop_words_and_punctuation(token_list)

        for word in clean_token_list:
            entity_list.append({"text": word, "type": "UNKNOWN"})
        return entity_list

    # TODO Write Test
    @debug
    def get_normalized_and_filtered_nlp_entities(self, str_: str) -> List[NLPEntityModel]:
        """
        :param str_: description
        :return: Normalized Filtered Tokens
        """
        if self.is_description_too_long_or_empty(str_, self.max_description):
            print("Description is Too Long")
            return []
        else:
            nlp_response = self.get_nlp_response(str_)
            nlp_entities = self.get_nlp_entities_from_nlp_response(nlp_response)

            nlp_entities, existing_entity_set, existing_entity_str = self.filter_nlp_entities_and_create_unique_entity_reference(
                nlp_entities,
                self.token_types_analyzed)
            nlp_entities += self.get_important_pos_tags_from_sentence(nlp_response.to_dict(), existing_entity_set,
                                                                      existing_entity_str)

            nlp_entities = self.normalize_entity_list(nlp_entities)
            print(nlp_entities)
            return nlp_entities

    # @staticmethod
    # # TODO Handle multiple leagues discussed
    # def get_value_of_specified_type(tokens: List[TagModel], type_: str) -> str:
    #     for token in tokens:
    #         if token['type'] == type_:
    #             return token['value']
    #     return ''
