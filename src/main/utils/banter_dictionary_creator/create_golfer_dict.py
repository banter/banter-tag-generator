from bs4 import BeautifulSoup
import requests
import pickle


# TODO some words are cut off, handling () in web scraping




def create_golfer_set(male_url, female_url):
    """
    Creating Golfer Set male and female
    :param url:
    :return:
    """
    sports_set = set()
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    headers = {"user-agent": USER_AGENT}
    resp = requests.get(male_url, headers=headers)
    if resp.status_code == 200:
        print(resp.content)
        soup = BeautifulSoup(resp.content, "html.parser")

    for index, value in enumerate(soup.find_all('tr')):
        try:
            golfer = value.text.split('\n')[1].lstrip()
            if ' *' in golfer:
                golfer = golfer.replace(' *', '')
            if 'HoF' in golfer:
                golfer = golfer.replace(' HoF', '')
            sports_set.add(golfer)
        except IndexError as err:
            print(err, value)

    resp = requests.get(female_url, headers=headers)
    if resp.status_code == 200:
        print(resp.content)
        soup = BeautifulSoup(resp.content, "html.parser")

    for index, value in enumerate(soup.find_all('tr')):
        try:
            golfer = value.text.split('\n')[1].lstrip()
            if ' *' in golfer:
                golfer = golfer.replace(' *', '')
            if 'HoF' in golfer:
                golfer = golfer.replace(' HoF', '')
            sports_set.add(golfer)
        except IndexError as err:
            print(err, value)

    return sports_set




def save_list(word_set, file_name):
    word_list = list(word_set)
    with open(f"../resources/reference_dict/{file_name}.data", 'wb') as filehandle:
        # store the data as binary data stream
        pickle.dump(word_list, filehandle)

# TODO this is just male golfers
male_golfer_url = 'https://en.wikipedia.org/wiki/List_of_male_golfers'
female_golfer_url = 'https://en.wikipedia.org/wiki/List_of_female_golfers'
golfer_set = create_golfer_set(male_golfer_url, female_golfer_url)

save_list(golfer_set, "golfer_set")
