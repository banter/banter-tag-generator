import json
import os
from os.path import dirname, realpath

import requests
from bs4 import BeautifulSoup

from src.main.utils.nlp_conversion_util import NLPConversionUtil

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(dirname(realpath(__file__)))))
SAVE_LOCATION = '%s/resources/reference_dict' % BASEDIR


# TODO some words are cut off, handling () in web scraping
def create_golfer_dict(male_url, female_url):
    """
    Creating Golfer Set male and female
    :param url:
    :return:
    """
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(male_url, headers=headers)
    golf_dict = {}
    if resp.status_code == 200:
        print(resp.content)
        soup = BeautifulSoup(resp.content, "html.parser")

    for index, value in enumerate(soup.find_all('tr')):
        if index == 0 or index == 1:
            print(value)
            continue
        try:
            golfer = value.text.split('\n')[1].lstrip()
            if ' *' in golfer:
                golfer = golfer.replace(' *', '')
            if 'HoF' in golfer:
                golfer = golfer.replace(' HoF', '')
            golf_dict[NLPConversionUtil().normalize_text(golfer)] = "MEN'S GOLF"
        except IndexError as err:
            print(err, value)

    resp = requests.get(female_url, headers=headers)
    if resp.status_code == 200:
        print(resp.content)
        soup = BeautifulSoup(resp.content, "html.parser")

    for index, value in enumerate(soup.find_all('tr')):
        if index == 0 or index == 1:
            print(value)
            continue
        try:
            golfer = value.text.split('\n')[1].lstrip()
            if ' *' in golfer:
                golfer = golfer.replace(' *', '')
            if 'HoF' in golfer:
                golfer = golfer.replace(' HoF', '')

            golf_dict[NLPConversionUtil().normalize_text(golfer)] = "WOMEN'S GOLF"
        except IndexError as err:
            print(err, value)

    return golf_dict


def save_dict(dictionary, file_name):
    tmp_json = json.dumps(dictionary)
    f = open(f"{SAVE_LOCATION}/{file_name}.json", "w")
    f.write(tmp_json)
    f.close()


def create_golf_player_dict():
    male_golfer_url = 'https://en.wikipedia.org/wiki/List_of_male_golfers'
    female_golfer_url = 'https://en.wikipedia.org/wiki/List_of_female_golfers'
    golfer_dict = create_golfer_dict(male_golfer_url, female_golfer_url)

    save_dict(golfer_dict, "GOLF_player_dict")
