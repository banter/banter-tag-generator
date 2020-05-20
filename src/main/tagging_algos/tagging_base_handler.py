from typing import *

from src.main.tagging_algos.tagging_enums.base_tag_types import BaseTagTypes as TagTypes
from src.main.tagging_algos.tagging_enums.confidence_levels import ConfidenceLevels
from src.main.utils.nlp_util import NLPUtil


class TaggingBaseHandler:
    # Class Variable instead of Instance variable, so on initilization,
    # Dont have to setup, makes init go from 20ms to 0.00ms
    util = NLPUtil()

    def get_person_tags(self, toke_dict: dict):
        """
        # Pass in token and if a full name adding this tag
        :param toke_dict: Token Dict
        :return: Tags that are for a specific person
        """
        # Getting list of names to see length
        method_confidence = ConfidenceLevels.HIGH.value
        person_tags = []
        name: str = toke_dict['text']
        name_length = len(name.split())
        if name_length > 1:
            # Greater than 1 suggesting its a full name
            person_tags.append({"type": TagTypes.PERSON.value, "value": name, "confidence": method_confidence})

        return person_tags

    def get_basic_tags(self, description: str) -> List[Dict[str, str]]:
        basic_tags = self.generate_basic_tags(description)
        return self.util.remove_duplicates_from_dict_list_based_on_key(basic_tags, "value")

    def generate_basic_tags(self, description: str) -> List[Dict]:
        description_tags: List[Dict] = []
        key_words = self.util.get_key_word_dict(description)
        for word in key_words:
            if self.util.is_token_specific_type(word, "PERSON"):
                description_tags += self.get_person_tags(word)
        return description_tags

    def handle_untagged_key_word(self, key_word: dict):
        pass
