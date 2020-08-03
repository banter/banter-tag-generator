import os
from os.path import dirname, realpath

import requests
from bs4 import BeautifulSoup

BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(dirname(realpath(__file__)))))
FANTASY_FOOTBALL_POSITIONS = ['QB', 'RB', 'WR', 'TE', 'K']
MLB_OUTFIELD_POSITIONS = ['LF', 'RF', 'OF', 'CF']
NBA_POSITIONS = ['PG', 'SG', 'SF', 'PF', 'C']


class SportsReferencePlayerScraper:

    def __init__(self, league: str):
        self.league = league.upper()
        if league == 'MLB':
            self.sports_reference_url = "https://www.baseball-reference.com/players/"
            self.url_ending = 'shtml'
        elif league == 'NFL':
            self.sports_reference_url = "https://www.pro-football-reference.com/players/"
            self.url_ending = 'htm'
        elif league == 'NBA':
            self.sports_reference_url = "https://www.basketball-reference.com/players/"
            self.url_ending = 'html'
        # TODO implement nhl
        elif league == 'NHL':
            self.sports_reference_url = ""

    def get_position(self, player):
        if self.league == 'MLB':
            return self.get_position_mlb(player)
        elif self.league == 'NFL':
            return self.get_position_nfl(player)
        elif self.league == 'NBA':
            return self.get_position_nba(player)
        else:
            return ''

    def is_position_attribute_corect(self, position) -> bool:
        if position == '' or position is None:
            return False
        else:
            return True

    def get_position_mlb(self, player):
        try:
            if self.is_position_attribute_corect(player.position):
                if player.position in MLB_OUTFIELD_POSITIONS:
                    return 'OF'
                else:
                    return player.position
            else:
                position = self.get_baseball_position_from_protected_attribute(player)
                return position
        except:
            position = self.get_baseball_position_from_protected_attribute(player)
            return position

    def get_baseball_position_from_protected_attribute(self, player):
        try:
            positions = player._position
            if type(positions) == list:
                if positions[0] not in MLB_OUTFIELD_POSITIONS:
                    return positions[0]
                else:
                    return 'OF'
            else:
                if positions != '':
                    if '/' in positions:
                        # CB/LB/RB
                        return positions.split('/')[0]
                    else:
                        return positions
                else:
                    return positions
        except:
            return ''

    def get_position_nfl(self, player):
        is_every_position_empty = True
        try:
            positions = player._position
            if positions is None:
                return self._scrape_sports_reference_for_nfl_players_position(player.player_id)
            elif type(positions) == list:
                for index, position in enumerate(positions):
                    if position.upper() in FANTASY_FOOTBALL_POSITIONS:
                        return position.upper()
                    else:
                        if position != '':
                            is_every_position_empty = False
                if is_every_position_empty:
                    return self._scrape_sports_reference_for_nfl_players_position(player.player_id)
                else:
                    return ''
            else:
                if positions != '':
                    if '/' in positions:
                        # CB/LB/RB
                        position = positions.split('/')[0]
                        if position in FANTASY_FOOTBALL_POSITIONS:
                            return position
                    else:
                        if positions in FANTASY_FOOTBALL_POSITIONS:
                            return positions
                    return ''
                else:
                    return ''
        except:
            return ''

    def get_position_nba(self, player):
        if self.is_position_attribute_corect(player.position):
            return player.position
        else:
            try:
                positions = player._position
                if type(positions) == list:
                    if positions[0].upper() in NBA_POSITIONS:
                        return positions[0].upper()
                    else:
                        return ''
                else:
                    if positions != '' and positions.upper() in NBA_POSITIONS:
                        return positions.upper()
                    else:
                        return ''
            except:
                return ''

    def _create_player_url(self, player_id):
        first_letter_of_id = player_id[0]
        return f"{self.sports_reference_url}{first_letter_of_id}/{player_id}.{self.url_ending}"

    def _scrape_sports_reference_for_nfl_players_position(self, player_id):
        url = self._create_player_url(player_id)
        soup = self._return_soup_object(url)
        position = self.get_position_from_html(soup)
        if position in FANTASY_FOOTBALL_POSITIONS:
            return position
        else:
            return ''

    def _scrape_sports_reference_for_players_team(self, player_id):
        url = self._create_player_url(player_id)
        soup = self._return_soup_object(url)
        team = self.get_team_from_html(soup)
        return team

    def get_position_from_html(self, soup: BeautifulSoup):
        for g in soup.find_all('p'):
            try:
                if g.findChild().text == 'Position':
                    position = g.text.split()[1]
                    return position
            except:
                return ''

    def get_team_from_html(self, soup: BeautifulSoup):
        for g in soup.find_all('p'):
            try:
                # print(g.findChild().text)
                if g.findChild().text == 'Team:':
                    team = g.find('a').text
                    return team
                elif g.findChild().text == 'Team':
                    team = g.find('a').text
                    return team
            except:
                return ''

    def _manually_fix_nba_positions(self, player_dict):
        # There are scenarios where a player is labeled as SF-SG or PF-SG ... etc, NBAs going small ball
        if "JIMMY BUTLER" in player_dict:
            player_dict["JIMMY BUTLER"]["position"] = "SF"
        if "THON MAKER" in player_dict:
            player_dict["THON MAKER"]["position"] = "C"
        if "WESLEY MATTHEWS" in player_dict:
            player_dict["WESLEY MATTHEWS"]["position"] = "SG"
        if "KYLE KORVER" in player_dict:
            player_dict["KYLE KORVER"]["position"] = "SG"
        if "PAUL WATSON" in player_dict:
            player_dict["PAUL WATSON"]["position"] = "SG"
        if "HARRISON BARNES" in player_dict:
            player_dict["HARRISON BARNES"]["position"] = "SF"
        if "WILSON CHANDLER" in player_dict:
            player_dict["WILSON CHANDLER"]["position"] = "SF"
        return player_dict

    @staticmethod
    def _return_soup_object(url):
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        headers = {"user-agent": USER_AGENT}
        resp = requests.get(url, headers=headers)
        # Full roster on Profootball reference is in the comments portion of html, very weird
        # Removing for now
        # removed_comments = str(resp.content).replace("<!--", "").replace("-->", "")
        return BeautifulSoup(resp.content, "html.parser")
