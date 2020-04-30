import string
import json
import pickle
import stanza
from pathlib import Path
from nltk.tokenize import word_tokenize
import os
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


class HelperClass:

    def __init__(self):
        self.eng_stop_words = ENGLISH_STOP_WORDS
        self.nlp = stanza.Pipeline('en')  # This sets up a default neural pipeline in English
        self.sports_leagues = ["nfl", "nhl", "nba", "football", "mlb", "ncaab", "ncaafb"]
        self.sports_with_references = ["american_football", "basketball", "football", "hockey", "baseball"]
        self.sports_with_nickname_coaches = ['nfl', 'nba', 'mlb']
        # Todo add more indv. sports dicts
        self.individual_sports = ['golf']
        # TODO handle football/soccer vs american football
        self.all_sports = ["american_football", "basketball", "football", "hockey", "baseball", "tennis",
                           "swimming", "track", "olympics", "lacrosse", "rugby", "soccer"]
        # When running from runner this references root dict
        # C:\Users\runni_000\PycharmProjects
        # Useful for local Coding depending where import helper_class
        try:
            self.root_dir = str(Path(os.getcwd()).parents[0])
            self.reference_dir = r"%s\assets\reference_dict" % self.root_dir
            self.sports_team_dict = self.set_team_dict(self.reference_dir)
            self.sports_player_dict = self.set_player_dict(self.reference_dir)
            self.sports_terms_dict = self.set_sports_terms_dict(self.reference_dir)
            self.individual_sports_dict = self.set_individual_sport_dict(self.reference_dir)
            self.sports_coach_dict = self.set_coach_dict(self.reference_dir)
            self.sports_nickname_dict = self.set_nickname_dict(self.reference_dir)
        except FileNotFoundError as error:
            print(error)
            self.root_dir = str(Path(os.getcwd()))
            self.reference_dir= r"%s\assets\reference_dict" % self.root_dir
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
        for league in self.sports_leagues:
            # Dont have football team info (soccer)
            if league == "football":
                pass
            else:
                tmp_dict[league] = self.read_json_file(file_path=file_path,
                                                              file_name=f"{league}_team_dict.json")
        return tmp_dict


    def set_player_dict(self, file_path):
        tmp_dict = {}
        for league in self.sports_leagues:
            # Dont have football (soccer) , ncaab, ncaafb player info
            if league in ["football", "ncaab", "ncaafb"]:
                pass
            else:
                tmp_dict[league] = self.read_json_file(file_path=file_path,
                                                              file_name=f"{league}_player_dict.json")
        return tmp_dict

    def set_sports_terms_dict(self, file_path):
        tmp_dict = {}
        for sport in self.sports_with_references:
            tmp_dict[sport] = self.read_pickled_file(file_path=file_path,
                                                            file_name=f"{sport}_terms.data")
        return tmp_dict

    def set_nickname_dict(self, file_path):
        tmp_dict = {}
        for sport in self.sports_with_nickname_coaches:
            tmp_dict[sport] = self.read_json_file(file_path=file_path,
                                                            file_name=f"{sport}_nickname_dict.json")
        return tmp_dict

    def set_coach_dict(self, file_path):
        tmp_dict = {}
        for sport in self.sports_with_nickname_coaches:
            tmp_dict[sport] = self.read_json_file(file_path=file_path,
                                                            file_name=f"{sport}_coach_dict.json")
        return tmp_dict

    def set_individual_sport_dict(self, file_path):
        tmp_dict = {}
        for sport in self.individual_sports:
            tmp_dict[sport] = self.read_pickled_file(file_path=file_path, file_name=f"{sport}_athlete_set.data")
        return tmp_dict


    def remove_punctuation_from_text(self, text: str):
        translator = str.maketrans('', '', string.punctuation)
        text = text.translate(translator)
        return text

    def convert_span_list_to_dict_list(self, span_list: list):
        """
        :param span_list: Span list created from Standford NLP
        :return: dict_list
        """
        for index, value in enumerate(span_list):
            span_list[index] = span_list[index].to_dict()

        return span_list

    def read_json_file(self, file_path, file_name):
        # C:\Users\runni_000\PycharmProjects\podcastProject\assets\reference_dict\nba_team_dict.json
        with open(f'{file_path}\{file_name}') as json_file:
            return json.load(json_file)

    def read_pickled_file(self, file_path, file_name):
        with open(f'{file_path}\{file_name}', 'rb') as filehandle:
            # read the data as binary data stream
            return pickle.load(filehandle)

    def save_dict(self, dictionary, file_path, file_name):
        tmp_json = json.dumps(dictionary)
        with open(f'{file_path}\{file_name}', "w") as json_file:
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


    def get_token_dict_from_nlp(self, _str: str):
        """
        Take a summary provided from a podcast and return a tokenized dictionary
        :param summary: A list of words in string format
        :return: tokenized dictionary
        """
        token_span_list = self.nlp(_str).entities
        token_dict_list: dict = self.convert_span_list_to_dict_list(token_span_list)
        return token_dict_list

    def remove_duplicates_from_list(self, list_: list):
        return list(dict.fromkeys(list_))

    def get_token_dict_manual(self, _str: str):
        """
        This is used to determine the tokens without using standford nlp
        :param summary: Summary
        :return: dict
        """
        # Tokenizing Data, breaks up into words/ phrases
        token_dict_list = []
        token_list = word_tokenize(_str)
        # Removing Stop words and punctuation from data
        clean_data = [word for word in token_list if
                      not word in self.eng_stop_words and not word in string.punctuation]

        for word in clean_data:
            token_dict_list.append({"text": word, "type": "UNKNOWN"})

        return token_dict_list