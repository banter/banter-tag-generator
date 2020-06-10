import re
import string
from typing import *

from src.main.models.tag_model import TagModel, NLPEntityModel
from src.main.utils.config_util import LanguageConfig

ENGLISH_STOP_WORDS = frozenset([
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves", "like"])

# Editing punctuation so normalization doesnt remove matchup text punctuation
punctuation = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
for char in LanguageConfig().punctuation_to_keep_in_normalized_text:
    punctuation = punctuation.replace(char, '')


class NLPConversionUtil(LanguageConfig):
    altered_punctuation = punctuation
    capitalized_tag_types = ['league', 'position']

    @staticmethod
    def remove_stop_words_and_punctuation(list_: list) -> list:
        clean_data = [word for word in list_ if
                      not word in ENGLISH_STOP_WORDS and not word in string.punctuation]
        return clean_data

    @staticmethod
    def remove_duplicates_from_list(list_: list) -> list:
        return list(dict.fromkeys(list_))

    @staticmethod
    def filter_token_list_by_type(token_list: List[Dict], type: str) -> List[Dict]:
        filtered_list = [token for token in token_list if token['type'] == type]
        return filtered_list

    @staticmethod
    def remove_punctuation_from_text(text: str) -> str:
        translator = str.maketrans('', '', string.punctuation)
        return text.translate(translator)

    def alter_tags_to_proper_response_format(self, tags: List[TagModel], analyed_key: str = "value") -> List[TagModel]:
        return self.conver_non_league_tags_to_Title_Case_and_format_names(
            self.remove_duplicates_from_dict_list_based_on_key(tags, analyed_key))

    def conver_non_league_tags_to_Title_Case_and_format_names(self, tags: List[TagModel]):
        for tag in tags:
            tag_type = tag["type"]
            if tag_type not in self.capitalized_tag_types:
                if tag_type == "person":
                    tag["value"] = self.format_name(tag["value"])
                else:
                    tag["value"] = tag["value"].title()
        return tags

    @staticmethod
    def format_name(name: str):
        name_list = name.split(' ')
        if len(name_list[0]) == 2:
            formatted_name = name_list[0] + ' ' + ' '.join(name_list[1:]).title()
            return formatted_name
        else:
            return name.title()

    @staticmethod
    def sort_tags_primary_at_top(tags: List[TagModel]) -> List[TagModel]:
        return sorted(tags, key=lambda i: i['isPrimary'], reverse=True)

    def remove_duplicates_from_dict_list_based_on_key(self, list_: List[Dict], analyzed_key: str = "value") -> List[
        Dict]:
        sorted_list = self.sort_tags_primary_at_top(list_)
        filterd_list: List[Dict] = []
        token_set: Set = set()
        for value in sorted_list:
            if value[analyzed_key] in token_set:
                pass
            else:
                token_set.add(value[analyzed_key])
                filterd_list.append(value)
        return filterd_list

    def remove_extra_word_from_name(self, entity: NLPEntityModel) -> NLPEntityModel:
        """
        :param entity:
        :return: altered name if need be --- Lebron James Starts ---- Lebron James
        """
        if entity['type'] == "PERSON":
            text: List = entity['text'].split()
            if len(text) == 3:
                altered_name = " ".join(text[0:2])
                adjusted_name_tag: NLPEntityModel = {"type": "PERSON", "text": altered_name}
                return adjusted_name_tag
        return None

    def filter_nlp_entities_and_create_unique_entity_reference(self, nlp_entity_list: List[NLPEntityModel],
                                                               entities_analyzed: Set) -> [List[Dict], Set,
                                                                                           str]:
        """
        :param nlp_entity_list: List of tokens
        :param entities_analyzed: Token Types that we are inerested in i.e. "PEOPLE" and "ORGS"
        :return:
        filtered_token_list ---- List of only the important tokens
        token_set ----- A Set of all the tokens that are important, this will be used to ensure no duplicates
                        when looking at the UPOS of just the generic word tokens
        token_concat_str ----- a concatinated string which is used to see if the UPOS was mentioned is part of a set
                        i.e. Token St.Louis ---- NLP will breakdown St. , Louis into 2 different tokens, however we dont
                        want to look at either, this is what the concat_str is usefull for
        """
        filtered_token_list: List[Dict] = []
        existing_entity_set: Set = set()
        existing_entity_str: str = ''
        for nlp_entity in nlp_entity_list:
            if nlp_entity['text'] in existing_entity_set:
                pass
            else:
                if nlp_entity['type'] in entities_analyzed:
                    existing_entity_set.add(nlp_entity['text'])
                    existing_entity_str += nlp_entity['text']
                    filtered_token_list.append(nlp_entity)
                    adjusted_name_tag = self.remove_extra_word_from_name(nlp_entity)
                    if adjusted_name_tag:
                        filtered_token_list.append(adjusted_name_tag)

        return filtered_token_list, existing_entity_set, existing_entity_str

    @staticmethod
    # TODO write test
    def convert_span_list_to_dict_list(span_list: list) -> List[Dict[str, str]]:
        """
        :param span_list: Span list created from Standford NLP
        :return: dict_list
        """
        for index, value in enumerate(span_list):
            span_list[index] = span_list[index].to_dict()

        return span_list

    @staticmethod
    def append_to_existing_dict(new_key: str, new_value: str, existing_dict: Dict) -> Dict:
        existing_dict[new_key] = new_value
        return existing_dict

    @staticmethod
    def remove_non_capitalized_words_from_nlp_entity_text(nlp_entity: NLPEntityModel) -> NLPEntityModel:
        """
        Usecase: if in description it says, the Cleveland Browns are going to the super bowl, this is identified
                as an ORG "the Cleveland Browns" which is not ideal
        :param nlp_entity: keyword dict
        :return: keyword dict with non capitalized text removed
        """
        nlp_entity["text"] = ' '.join(w for w in nlp_entity["text"].split(' ') if not w.islower())
        return nlp_entity

    def remove_prefix_from_word(self, nlp_entity: NLPEntityModel):
        nlp_entity["text"] = ' '.join(w for w in nlp_entity["text"].split(' ') if not w in self.entity_prefix_list)
        return nlp_entity

    @staticmethod
    def remove_non_capitalized_words(s: str) -> str:
        return ' '.join(w for w in s.split(' ') if not w.islower())

    def normalize_text(self, text: str):
        """
        Performance --- 1000000 runs takes 3.8s locally
        Return a normalized name, removing jr, sr, III, II, also removing all punctuation, leading and trailing whitespace and making it uppercase
        :param text: name -- A.J. Green Sr. Jr. jr III
        :return: AJ GREEN
        """
        # removing 's from text
        clean_text = re.sub(r"(\'s\b)+\ *", " ", text)
        return re.sub('(\\s((?i)jr|sr|III|II|jnr|snr)[.]?)', '',
                      clean_text.translate(str.maketrans('', '', self.altered_punctuation)).upper()).strip()

    def normalize_nlp_entity(self, nlp_entity: NLPEntityModel):
        nlp_entity["text"] = self.normalize_text(nlp_entity["text"])
        return nlp_entity

    def normalize_entity_list(self, nlp_entities: List[NLPEntityModel]) -> List[NLPEntityModel]:
        return [self.normalize_nlp_entity(nlp_entity) for nlp_entity in nlp_entities]

    def is_adjusted_entity_different(self, nlp_entity: NLPEntityModel, adjusted_nlp_entity: NLPEntityModel):
        return nlp_entity == adjusted_nlp_entity
