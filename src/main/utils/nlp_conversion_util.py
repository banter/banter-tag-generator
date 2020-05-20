import string
from typing import *

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


class NLPConversionUtil(LanguageConfig):

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

    @staticmethod
    def remove_duplicates_from_dict_list_based_on_key(list_: List[Dict], analyzed_key: str = "value") -> List[Dict]:
        filterd_list: List[Dict] = []
        token_set: Set = set()
        for value in list_:
            if value[analyzed_key] in token_set:
                pass
            else:
                token_set.add(value[analyzed_key])
                filterd_list.append(value)
        return filterd_list

    @staticmethod
    def filter_tokens_get_unique_text(token_dict_list: List[Dict], token_types_analyzed: Set) -> [List[Dict], Set, str]:
        """
        :param token_dict_list: List of tokens
        :param token_types_analyzed: Token Types that we are inerested in i.e. "PEOPLE" and "ORGS"
        :return:
        filtered_token_list ---- List of only the important tokens
        token_set ----- A Set of all the tokens that are important, this will be used to ensure no duplicates
                        when looking at the UPOS of just the generic word tokens
        token_concat_str ----- a concatinated string which is used to see if the UPOS was mentioned is part of a set
                        i.e. Token St.Louis ---- NLP will breakdown St. , Louis into 2 different tokens, however we dont
                        want to look at either, this is what the concat_str is usefull for
        """
        filtered_token_list: List[Dict] = []
        token_set: Set = set()
        token_concat_str: str = ''
        for token in token_dict_list:
            if token['text'] in token_set:
                pass
            else:
                if token['type'] in token_types_analyzed:
                    token_set.add(token['text'])
                    token_concat_str += token['text']
                    filtered_token_list.append(token)

        return filtered_token_list, token_set, token_concat_str

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
    def remove_non_capitalized_words_from_key_word_text(key_word: Dict, ) -> Dict:
        """
        Usecase: if in description it says, the Cleveland Browns are going to the super bowl, this is identified
                as an ORG "the Cleveland Browns" which is not ideal
        :param key_word: keyword dict
        :return: keyword dict with non capitalized text removed
        """
        key_word["text"] = ' '.join(w for w in key_word["text"].split(' ') if not w.islower())
        return key_word

    @staticmethod
    def remove_non_capitalized_words(s: str) -> str:
        return ' '.join(w for w in s.split(' ') if not w.islower())

    # @staticmethod
    # def add_tag_to_tag_list(tag_list: List[TagModel], type: str, value: str, confidence: float) -> List[TagModel]:
    #     tag_list += {"type": type, "value": value, "confidence": confidence}
    #     return tag_list
