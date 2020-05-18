import logging

import requests
from bs4 import BeautifulSoup

from src.main.utils.decorators import debug

logger = logging.getLogger(__name__)


class GoogleSearchTagGenerator:

    @debug
    def get_google_search_results(self, google_search: str) -> str:
        # TODO Edge Cases to Consider
        # TODO 1. Zion
        # TODO 2. Jarvis
        """
        :param google_search: Search Term for Google
        :return: String of terms associated to the Person Block on the Google Search

        # TODO Remove punctuation from response simplify main class?
        """
        logger.info(f"Google Search Request: {google_search}")
        text_list = []
        google_search = google_search.replace(' ', '+')
        URL = f"https://google.com/search?q={google_search}"
        # desktop user-agent
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        # mobile user-agent
        MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
        headers = {"user-agent": USER_AGENT}
        resp = requests.get(URL, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
        results = []
        try:
            text_list += self.try_webpage_scrap_on_class(soup, 'kp-hc')

            if len(text_list) == 0:
                text_list += self.try_webpage_scrap_on_class(soup, 'kp-header')

        except Exception as e:
            logger.info(e)
            text_list = []
        logger.info(f"Google Search Results Scraped Final Text List: {str(text_list)}")
        return str(text_list)

    def try_webpage_scrap_on_class(self, soup, html_class: str):

        tmp_text: list = []
        for g in soup.find_all('div', class_=html_class):
            logger.debug(f"Find All divs of specfic html class = {html_class}: {g}")
            anchors = g.find_all('span')
            if anchors:
                logger.debug(f"SPAN ANCHORS: {anchors}")
                for index, value in enumerate(anchors):
                    tmp_text.append(anchors[index].text)

        logger.info(f"Google Search Result Scraped Text: {tmp_text}")
        return tmp_text
