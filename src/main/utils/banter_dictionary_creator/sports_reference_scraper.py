import requests
from bs4 import BeautifulSoup

FANTASY_FOOTBALL_POSITIONS = ['QB', 'RB', 'WR', 'TE', 'K']


class SportsReferenceScraper:
    nfl_base_url = "https://www.pro-football-reference.com/players/"
    nba_base_url = "https://www.basketball-reference.com/players/"
    mlb_base_url = "https://www.baseball-reference.com/players/"

    def scrape_nfl(self, player_id):

        first_letter_of_id = player_id[0]

        URL = f"{self.nfl_base_url}{first_letter_of_id}/{player_id}.htm"
        # desktop user-agent
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        headers = {"user-agent": USER_AGENT}
        resp = requests.get(URL, headers=headers)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            position = self.get_position_from_html(soup)
            if position in FANTASY_FOOTBALL_POSITIONS:
                return position
            else:
                return ''
        else:
            return ''

    def get_position_from_html(self, soup: BeautifulSoup):
        for g in soup.find_all('p'):
            try:
                if g.findChild().text == 'Position':
                    position = g.text.split()[1]
                    return position
            except:
                return ''
