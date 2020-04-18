from bs4 import BeautifulSoup
import requests
import pickle


# TODO some words are cut off, handling () in web scraping


def scrape_wiki(url):
    sports_set = set()
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
            sports_set.add(bracket_text)
        # Removing unnecessary Characters
        if "\xa0" in tmp_text:
            tmp_text = tmp_text.split('\xa0')[0]

        sports_set.add(tmp_text)
    return sports_set


def scrape_wiki_baseball(url):
    sports_set = set()
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
            sports_set.add(bracket_text)
        # Removing unnecessary Characters
        if "\xa0" in tmp_text:
            tmp_text = tmp_text.split('\xa0')[0]

        sports_set.add(tmp_text)
    return sports_set


def save_list(word_set, file_name):
    word_list = list(word_set)
    with open(f"../assets/reference_dict/{file_name}.data", 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(word_list, filehandle)


#
# hockey_url="https://en.wikipedia.org/wiki/Glossary_of_ice_hockey_terms"
# hockey_set = scrape_wiki(hockey_url)
# save_list(hockey_set, "hockey_terms")
#
#
# basketball_url = "https://en.wikipedia.org/wiki/Glossary_of_basketball_terms"
# basketball_set = scrape_wiki(basketball_url)
# save_list(basketball_set, "basketball_terms")
#
# american_football_url = 'https://en.wikipedia.org/wiki/Glossary_of_American_football'
# american_football_set = scrape_wiki(american_football_url)
# save_list(american_football_set, "american_football_terms")
#
#
# # TODO fix football terms
# football_url = 'https://en.wikipedia.org/wiki/Glossary_of_association_football_terms'
# football_set = scrape_wiki(football_url)
# save_list(football_set, "football_terms")


baseball_url = 'https://en.wikipedia.org/wiki/Glossary_of_baseball'
baseball_set = scrape_wiki_baseball(baseball_url)
save_list(baseball_set, "baseball_terms")
