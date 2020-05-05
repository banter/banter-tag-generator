import string
# https://medium.com/@ageitgey/learn-how-to-use-static-type-checking-in-python-3-6-in-10-minutes-12c86d72677b
from typing import *
import json
import pickle
import stanza
from stanza import Document
from pathlib import Path
import os
from os.path import dirname, realpath
from nltk.tokenize import word_tokenize
import configparser
from src.main.utils.decorators import debug
from src.main.utils.google_search_scraper import GoogleSearchTagGenerator

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


stanza.download('en')  # download English model

class HelperClass(GoogleSearchTagGenerator):

    # Current File Base Dir
    BASEDIR = os.path.abspath(os.path.dirname(dirname(realpath(__file__))))
    CONFIG_LOCATION = '%s/config/banter_tag_gen.config' % BASEDIR
    print(CONFIG_LOCATION)
    CONFIG = configparser.ConfigParser()
    CONFIG.read(CONFIG_LOCATION)
    SECTION = "DEFAULT"
    SPORTS_LEAGUES: List[str] = json.loads(CONFIG.get(SECTION, "SPORTS_LEAGUES"))
    SPORTS_LEAGUES_NO_PLAYER_REF: List[str] = json.loads(CONFIG.get(SECTION, "SPORTS_LEAGUES_NO_PLAYER_REF"))
    SPORTS_LEAGUES_NO_TEAM_REF: List[str] = json.loads(CONFIG.get(SECTION, "SPORTS_LEAGUES_NO_TEAM_REF"))

    SPORTS_WITH_REFERENCES: List[str] = json.loads(CONFIG.get(SECTION, "SPORTS_WITH_REF"))
    SPORTS_LEAGUES_WITH_NICKNAME_AND_COACHES: List[str] = json.loads(CONFIG.get(SECTION, "SPORTS_LEAGUES_WITH_NICKNAME_AND_COACHES"))

    # Todo add more indv. sports dicts
    INDIVIDUAL_SPORTS: List[str] = json.loads(CONFIG.get(SECTION, "INDIVIDUAL_SPORTS"))

    # TODO handle football/soccer vs american football
    ALL_SPORTS: List[str] = json.loads(CONFIG.get(SECTION, "ALL_SPORTS"))

    # TODO Consider EVENTS
    TOKEN_TYPES_ANALYZED = set(json.loads(CONFIG.get(SECTION, "TOKEN_TYPES_ANALYZED")))
    # TODO Consider NOUNS?
    LANGUAGE_TYPES_ANALYZED: Dict[str, str] = set(json.loads(CONFIG.get(SECTION, "LANGUAGE_TYPES_ANALYZED")))
    IGNORE_TAGS: set = set(json.loads(CONFIG.get(SECTION, "IGNORE_TAGS")))

    # TODO Consider max descrition size to consider
    MAX_DESCRIPTION: int = int(CONFIG.get(SECTION, "MAX_DESCRIPTION_LENGTH"))

    def __init__(self):

        self.ENG_STOP_WORDS = ENGLISH_STOP_WORDS
        self.nlp = stanza.Pipeline('en')  # This sets up a default neural pipeline in English
        self.word_tokenize = word_tokenize
        # When running from runner this references root dict
        # C:\Users\runni_000\PycharmProjects
        # Useful for local Coding depending where import helper_class
        try:
            # Current File
            self.reference_dir = r"%s/resources/reference_dict" % self.BASEDIR
            self.sports_team_dict = self.set_team_dict(self.reference_dir)
            self.sports_player_dict = self.set_player_dict(self.reference_dir)
            self.individual_sports_dict = self.set_individual_sport_dict(self.reference_dir)
            self.sports_terms_dict = self.set_sports_terms_dict(self.reference_dir)
            self.sports_coach_dict = self.set_coach_dict(self.reference_dir)
            self.sports_nickname_dict = self.set_nickname_dict(self.reference_dir)
        except FileNotFoundError as error:
            print(error)
            # self.root_dir = str(Path(os.getcwd()))
            self.reference_dir= r"%s/main/resources/reference_dict" % self.BASEDIR
            self.sports_team_dict = self.set_team_dict(self.reference_dir)
            self.sports_player_dict = self.set_player_dict(self.reference_dir)
            self.individual_sports_dict = self.set_individual_sport_dict(self.reference_dir)
            self.sports_terms_dict = self.set_sports_terms_dict(self.reference_dir)
            self.sports_coach_dict = self.set_coach_dict(self.reference_dir)
            self.sports_nickname_dict = self.set_nickname_dict(self.reference_dir)

        pass

    def set_team_dict(self, file_path):
        """
        Set team dictionary for class
        """
        tmp_dict = {}
        for league in self.SPORTS_LEAGUES:
            # Dont have football team info (soccer)
            if league in self.SPORTS_LEAGUES_NO_TEAM_REF:
                pass
            else:
                tmp_dict[league] = self.read_json_file(file_path=file_path,
                                                              file_name=f"{league}_team_dict.json")
        return tmp_dict


    def set_player_dict(self, file_path):
        tmp_dict = {}
        for league in self.SPORTS_LEAGUES:
            # Dont have football (soccer) , ncaab, ncaafb player info
            if league in self.SPORTS_LEAGUES_NO_PLAYER_REF:
                pass
            else:
                tmp_dict[league] = self.read_json_file(file_path=file_path,
                                                              file_name=f"{league}_player_dict.json")
        return tmp_dict

    def set_sports_terms_dict(self, file_path):
        tmp_dict = {}
        for sport in self.SPORTS_WITH_REFERENCES:
            tmp_dict[sport] = self.read_pickled_file(file_path=file_path,
                                                            file_name=f"{sport}_terms.data")
        return tmp_dict

    def set_nickname_dict(self, file_path):
        tmp_dict = {}
        for sport in self.SPORTS_LEAGUES_WITH_NICKNAME_AND_COACHES:
            tmp_dict[sport] = self.read_json_file(file_path=file_path,
                                                            file_name=f"{sport}_nickname_dict.json")
        return tmp_dict

    def set_coach_dict(self, file_path):
        tmp_dict = {}
        for sport in self.SPORTS_LEAGUES_WITH_NICKNAME_AND_COACHES:
            tmp_dict[sport] = self.read_json_file(file_path=file_path,
                                                            file_name=f"{sport}_coach_dict.json")
        return tmp_dict

    def set_individual_sport_dict(self, file_path):
        tmp_dict = {}
        for sport in self.INDIVIDUAL_SPORTS:
            tmp_dict[sport] = self.read_pickled_file(file_path=file_path, file_name=f"{sport}_athlete_set.data")
        return tmp_dict


    def remove_punctuation_from_text(self, text: str):
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)
        return text

    def convert_span_list_to_dict_list(self, span_list: list) -> List[Dict[str,str]]:
        """
        :param span_list: Span list created from Standford NLP
        :return: dict_list
        """
        for index, value in enumerate(span_list):
            span_list[index] = span_list[index].to_dict()

        return span_list

    def convert_tuple_list_to_str_list(self, tuple_list: list):
        str_list: list = [".".join(map(str, r)) for r in tuple_list]
        return str_list


    def read_json_file(self, file_path, file_name):
        # C:\Users\runni_000\PycharmProjects\podcastProject\resources\reference_dict\nba_team_dict.json
        with open(f'{file_path}/{file_name}') as json_file:
        # with open(f'../{file_name}') as json_file:
            return json.load(json_file)

    def read_pickled_file(self, file_path, file_name):
        with open(f'{file_path}/{file_name}', 'rb') as filehandle:
            # read the data as binary data stream
            return pickle.load(filehandle)

    def save_dict(self, dictionary, file_path, file_name):
        tmp_json = json.dumps(dictionary)
        with open(f'{file_path}/{file_name}', "w") as json_file:
            json_file.write(tmp_json)
            json_file.close()

    def save_to_existing_dict_tags(self, appended_dict: dict, file_path: str , file_name: str):
        """
        :param appended_dict:
        :param file_path: r"%s\data\tag_generation_pending_validation" % self.parent_dir,
        :param file_name: "tags.json"
        :return:
        """
        existing_dict: dict = self.read_json_file(file_path=file_path, file_name=file_name)
        existing_dict.update(appended_dict)
        self.save_dict(existing_dict, file_path, file_name)

        return

    def save_to_existing_dict_summary(self, summary_list: list, file_path: str, file_name: str):
        """

        :param summary_list:
        :param file_path: r"%s\data\tag_generation_pending_validation" % self.parent_dir,
        :param file_name: "summary_tag__pending_validation.json"
        :return:
        """

        existing_dict: dict = self.read_json_file(file_path=file_path, file_name=file_name)


        for index, summary in enumerate(summary_list):
            existing_dict["SummaryList"].append(summary)
        self.save_dict(existing_dict, file_path, file_name)
        # print("Summary List", existing_dict)
        return

    def append_to_existing_dict(self, key, dict_, value):

        if key in dict_:
            # TODO Switch Back, writing whole key for testing purposes
            # _dict[key].append(value)
            dict_[key] = value
        else:
            dict_[key] = value
        return dict_


    def get_token_dict_from_nlp(self, nlp_response: Document) -> List[Dict[str,str]] :
        """
        Take a summary provided from a podcast and return a tokenized dictionary
        :param summary: A list of words in string format
        :return: tokenized dictionary
        """
        token_span_list = nlp_response.entities
        token_dict_list: List[Dict[str,str]] = self.convert_span_list_to_dict_list(token_span_list)
        return token_dict_list

    def remove_duplicates_from_list(self, list_: list):
        return list(dict.fromkeys(list_))

    def remove_stop_words_and_punctuation(self, list_: list):
        clean_data = [word for word in list_ if
                      not word in self.ENG_STOP_WORDS and not word in string.punctuation]
        return clean_data

    def filter_token_list_by_type(self, token_list: list, type:str):
        filtered_list = [token for token in token_list if token['type'] == type]
        return filtered_list

    def get_nlp_response(self, str_:str) -> Document:
        return self.nlp(str_)

    def is_description_below_max_length(self, str_:str, max_description: int) -> bool:
        return len(str_.split(' ')) < max_description

    @debug
    def get_key_word_dict(self, str_:str) -> List[Dict]:
        is_descption_too_long: bool = self.is_description_below_max_length(str_, self.MAX_DESCRIPTION)
        if is_descption_too_long:
            nlp_response = self.get_nlp_response(str_)

            token_dict_list = self.get_token_dict_from_nlp(nlp_response)
            all_tokens_as_string: str = ''
            token_dict_list, token_set, token_concat_str = self.filter_tokens_get_unique_text(token_dict_list)

            for token in token_dict_list:
                all_tokens_as_string += token['text']

            token_dict_list += self.get_nouns_from_sentence(nlp_response, token_set, token_concat_str)

            return token_dict_list

        else:
            print("Description is Too Long")
            return []

    def filter_duplicates_from_dict_list(self, list_: List[Dict], filtered_key: str = "value") -> [List[Dict], Set, str]:

        filterd_list: List[Dict] = []
        token_set: Set = set()
        for value in list_:
            if value[filtered_key] in token_set:
                pass
            else:
                token_set.add(value[filtered_key])
                filterd_list.append(value)
        return filterd_list


    def filter_tokens_get_unique_text(self, token_dict_list: List[Dict]) -> [List[Dict], Set, str]:

        filtered_token_list: List[Dict] = []
        token_set: Set = set()
        token_concat_str: str = ''
        for token in token_dict_list:
            if token['text'] in token_set:
                pass
            else:
                token_set.add(token['text'])
                token_concat_str += token['text']
                if token['type'] in self.TOKEN_TYPES_ANALYZED:
                    filtered_token_list.append(token)

        return filtered_token_list, token_set, token_concat_str

    def get_nouns_from_sentence(self, nlp_response: Document, token_set: Set, token_concat_str: str) -> List[Dict]:
        nlp_list = nlp_response.to_dict()

        noun_list = []

        for index, sentence in enumerate(nlp_list):

            # TODO Consider the Following TB12 is considered a noun, AB is considered a proper noun
            # TODO Allowing for nouns open ups a can of worms
            for token in sentence:
                # Checking if we care about the upos (NOUN, PRONOUN, Etc.) Also Checking for Duplicates
                if token['upos'] in self.LANGUAGE_TYPES_ANALYZED and token['text'] not in token_set:
                    # Above checks for an EXACT Match, however St.Louis Rams gets tokenized as St.Louis Rams
                    # But each St. , Louis, Rams, are all technically different parts of speach.
                    # As a result, a token_concat_str is created and it just looks to see if it contains a sub string
                    # TODO this probably fucks some edge scenarios up
                    if token['text'] not in token_concat_str:
                        # Creating noun dict to match with entities dict, arbitrary start_char and end_char
                        noun = {"text": token['text'], "type": token['upos'], "start_char": 1, "end_char":1}
                        noun_list.append(noun)

        return noun_list


    def get_token_dict_manual(self, _str: str):
        """
        This is used to determine the tokens without using standford nlp
        :param summary: Summary
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