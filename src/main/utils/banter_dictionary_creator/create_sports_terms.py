import requests
from bs4 import BeautifulSoup

import json

import os
from os.path import dirname, realpath

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(dirname(realpath(__file__)))))
SAVE_LOCATION = '%s/resources/reference_dict' % BASEDIR
# TODO some words are cut off, handling () in web scraping


def scrape_wiki(url, sport):
    sport_dict = {}
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        print(resp.content)
        soup = BeautifulSoup(resp.content, "html.parser")
    for i in soup.find_all('dt'):

        tmp_text = i.get_text()
        print(tmp_text)
        print(i)

        # Accounting for if terms are in ( ) ex: National Basketball Association (NBA)
        bracket_text = tmp_text[tmp_text.find("(") + 1:tmp_text.find(")")]
        if tmp_text != bracket_text:
            # Removing below addition for time being
            # sport_dict[bracket_text] = sport
            pass
        # Removing unnecessary Characters
        if "\xa0" in tmp_text:
            tmp_text = tmp_text.split('\xa0')[0]

        sport_dict[tmp_text] = sport
    return sport_dict


def scrape_wiki_baseball(url):
    sport_dict = {}
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        print(resp.content)
        soup = BeautifulSoup(resp.content, "html.parser")

    for i in soup.find_all('span', class_='mw-headline'):

        tmp_text = i.get_text()
        print(tmp_text)
        print(i)

        # Accounting for if terms are in ( ) ex: National Basketball Association (NBA)
        bracket_text = tmp_text[tmp_text.find("(") + 1:tmp_text.find(")")]
        if tmp_text != bracket_text:
            # Removing below addition for time being
            # sport_dict[bracket_text] = "baseball"
            pass
        # Removing unnecessary Characters
        if "\xa0" in tmp_text:
            tmp_text = tmp_text.split('\xa0')[0]

        sport_dict[tmp_text] = "BASEBALL"
    return sport_dict

def save_dict(dictionary, file_name):
    tmp_json = json.dumps(dictionary)
    with open(f"{SAVE_LOCATION}/{file_name}.json", "w") as json_file:
        json_file.write(tmp_json)
        json_file.close()

def create_sports_terms():
    final_dict = {}
    basketball_url = "https://en.wikipedia.org/wiki/Glossary_of_basketball_terms"
    basketball_dict = scrape_wiki(basketball_url, "BASKETBALL")
    final_dict.update(basketball_dict)
    hockey_url = "https://en.wikipedia.org/wiki/Glossary_of_ice_hockey_terms"
    hockey_dict = scrape_wiki(hockey_url, "HOCKEY")
    final_dict.update(hockey_dict)
    # TODO Football/Soccer Terms
    american_football_url = 'https://en.wikipedia.org/wiki/Glossary_of_American_football'
    american_football_dict = scrape_wiki(american_football_url, "FOOTBALL")
    final_dict.update(american_football_dict)
    football_url = 'https://en.wikipedia.org/wiki/Glossary_of_association_football_terms'
    football_dict = scrape_wiki(football_url, "SOCCER")
    final_dict.update(football_dict)
    baseball_url = 'https://en.wikipedia.org/wiki/Glossary_of_baseball'
    baseball_dict = scrape_wiki_baseball(baseball_url)
    final_dict.update(baseball_dict)

    save_dict(final_dict, "sports_terms_dict")


if __name__ == '__main__':
    create_sports_terms()
