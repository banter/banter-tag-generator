import json

import requests
from bs4 import BeautifulSoup

from src.main.utils.nlp_conversion_util import NLPConversionUtil
import os
from os.path import dirname, realpath

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(dirname(realpath(__file__)))))
SAVE_LOCATION = '%s/resources/reference_dict' % BASEDIR

def create_nfl_coach_dict():
    """
    Source: https://en.wikipedia.org/wiki/List_of_nicknames_used_in_basketball
    :return: Nickname dict format:
    {
    nickname: Player Name
    The King: Lebron James
    }
    """
    url = "https://en.wikipedia.org/wiki/List_of_current_National_Football_League_head_coaches"
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(url, headers=headers)
    coach_dict = {}
    if resp.status_code == 200:
        print(resp.content)
        soup = BeautifulSoup(resp.content, "html.parser")

    for index, value in enumerate(soup.findAll('tr')):
        try:
            if index > 1 and index < 34:
                team, name = value.text.split('\n')[1::2][0:2]
                coach_dict[NLPConversionUtil().normalize_text(name)] = team


        except Exception as e:
            print(e)
    return coach_dict


def create_nba_coach_dict():
    """
    Source: https://en.wikipedia.org/wiki/List_of_nicknames_used_in_basketball
    :return: Nickname dict format:
    {
    nickname: Player Name
    The King: Lebron James
    }
    """
    url = "https://en.wikipedia.org/wiki/List_of_National_Basketball_Association_head_coaches"
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(url, headers=headers)
    coach_dict = {}
    if resp.status_code == 200:
        print(resp.content)
        soup = BeautifulSoup(resp.content, "html.parser")

    for index, value in enumerate(soup.findAll('tr')):
        try:
            if 7 < index < 38:
                name, team = value.text.split('\n')[1::2][0:2]
                if '*' in name:
                    name = name.replace('*', '')

                coach_dict[NLPConversionUtil().normalize_text(name)] = team


        except Exception as e:
            print(e)
    return coach_dict


def create_mlb_coach_dict():
    # TODO Issues with Same Manager Multiple Teams
    """
    Source: https://en.wikipedia.org/wiki/List_of_nicknames_used_in_basketball
    :return: Nickname dict format:
    {
    nickname: Player Name
    The King: Lebron James
    }
    """
    url = "https://en.wikipedia.org/wiki/List_of_Major_League_Baseball_managers"
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(url, headers=headers)
    coach_dict = {}
    if resp.status_code == 200:
        print(resp.content)
        soup = BeautifulSoup(resp.content, "html.parser")

    for index, value in enumerate(soup.findAll('tr')):
        try:
            if 0 < index < 16 or 16 < index < 32:
                team = value.text.split('\n')[1]
                try:
                    name = value.text.split('\n')[6]
                    old_name = value.text.split('\n')[11]
                except IndexError as e:
                    print(e)
                    name = value.text.split('\n')[5]
                    old_name = value.text.split('\n')[9]

                coach_dict[NLPConversionUtil().normalize_text(name)] = team
                # coach_dict[old_name] = team


        except Exception as e:
            print(e)
    return coach_dict

def save_dict(dictionary, file_name):
    tmp_json = json.dumps(dictionary)
    f = open(f"{SAVE_LOCATION}/{file_name}.json", "w")
    f.write(tmp_json)
    f.close()

def create_headcoach_dict(is_team_upper_case=False):
    if is_team_upper_case:
        coach_dict = create_nfl_coach_dict()
        coach_dict_upper = dict((NLPConversionUtil().normalize_text(k), v.upper()) for k, v in coach_dict.items())
        save_dict(coach_dict_upper, "NFL_coach_dict")
        coach_dict = create_nba_coach_dict()
        coach_dict_upper = dict((NLPConversionUtil().normalize_text(k), v.upper()) for k, v in coach_dict.items())
        save_dict(coach_dict_upper, "NBA_coach_dict")
        coach_dict = create_mlb_coach_dict()
        coach_dict_upper = dict((NLPConversionUtil().normalize_text(k), v.upper()) for k, v in coach_dict.items())
        save_dict(coach_dict_upper, "MLB_coach_dict")
    else:
        coach_dict = create_nfl_coach_dict()
        coach_dict_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in coach_dict.items())
        save_dict(coach_dict_upper, "NFL_coach_dict")
        coach_dict = create_nba_coach_dict()
        coach_dict_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in coach_dict.items())
        save_dict(coach_dict_upper, "NBA_coach_dict")
        coach_dict = create_mlb_coach_dict()
        coach_dict_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in coach_dict.items())
        save_dict(coach_dict_upper, "MLB_coach_dict")
