import json
import os
from os.path import dirname, realpath

from sportsreference.mlb.roster import Roster as MLBRoster
from sportsreference.mlb.teams import Teams as MLBTeams
from sportsreference.nba.roster import Roster as NBARoster
from sportsreference.nba.teams import Teams as NBATeams
from sportsreference.nfl.roster import Roster as NFLRoster
from sportsreference.nfl.teams import Teams as NFLTeams
from sportsreference.nhl.roster import Roster as NHLRoster
from sportsreference.nhl.teams import Teams as NHLTeams

from src.main.utils.banter_dictionary_creator.sports_reference_player_scraper import \
    SportsReferencePlayerScraper
from src.main.utils.nlp_conversion_util import NLPConversionUtil
from src.main.utils.nlp_resource_util import NLPResourceUtil

# TODO Handle Soccer Teams/Players
nlp_resource_util = NLPResourceUtil()
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(dirname(realpath(__file__)))))
MLB_OUTFIELD_POSITIONS = ['LF', 'RF', 'OF', 'CF']
FANTASY_FOOTBALL_POSITIONS = ['QB', 'RB', 'WR', 'TE', 'K']
NBA_POSITIONS = ['PG', 'SG', 'SF', 'PF', 'C']
SAVE_LOCATION = '%s/resources/reference_dict' % BASEDIR


class Player:
    def __init__(self, display: str, team: str, position: str, player_id: str):
        """
        Example
        :param display: LeBron James
        :param team: LOS ANGELES LAKERS
        :param position: SF
        :param player_id: jamesle01 *really wanted to make this lebron69420 but decided to put his actual playerid :(
        """
        self.display = display
        self.team = team
        self.position = position
        self.player_id = player_id


class SportsReferenceRosterScraper(SportsReferencePlayerScraper):

    def __init__(self, league: str, get_rosters: bool = False):
        super().__init__(league)
        self.league = league.upper()
        self.valid_team_names = set()
        if league == 'MLB':
            self.league_teams = MLBTeams("2019")
            self.Roster_Package = MLBRoster
        elif league == 'NFL':
            self.league_teams = NFLTeams("2019")
            self.Roster_Package = NFLRoster
        elif league == 'NBA':
            self.league_teams = NBATeams("2019")
            self.Roster_Package = NBARoster
        elif league == 'NHL':
            self.league_teams = NHLTeams("2019")
            self.Roster_Package = NHLRoster
        self.league_roster_dict: dict = {}
        self.duplicate_names: list = []
        if get_rosters:
            self.create_league_player_dict()
            self.league_roster_dict = self.manually_fix_roster_dict(self.league, self.league_roster_dict)

    def _get_valid_team_names(self) -> set:
        """
        if first time through, will create set, otherwise it will know already has the set
        this is used because you do not want to have to loop through each team whenever using this class, this
        slows it down
        :return: valid_team_names
        """
        if len(self.valid_team_names) == 0:
            for team in self.league_teams:
                self.valid_team_names.add(team.name)
            return self.valid_team_names
        else:
            return self.valid_team_names

    def _get_list_of_team_details(self) -> list:
        team_details = []
        for team in self.league_teams:
            team_details.append({"team_abbreviation": team.abbreviation, "team_name": team.name})
        return team_details

    def get_team_name(self, team_details: dict) -> str:
        return NLPConversionUtil().normalize_text(team_details["team_name"])

    def get_team_roster(self, team_abbreviation):
        try:
            team_roster = self.Roster_Package(team_abbreviation, '2020', slim=False)
            if len(team_roster.players) == 0:
                print(f"No Roster available for 2020 for:{team_abbreviation}")
                team_roster = self.Roster_Package(team_abbreviation, '2019', slim=False)
        except:
            team_roster = self.Roster_Package(team_abbreviation, '2019', slim=False)
            if len(team_roster.players) == 0:
                team_roster = self.Roster_Package(team_abbreviation, '2018', slim=False)
        return team_roster

    def create_league_player_dict(self):
        print("Start of Create League Player")
        for team_details in self._get_list_of_team_details():
            print("Starting:", team_details)
            team_roster = self.get_team_roster(team_abbreviation=team_details["team_abbreviation"])
            team_name = self.get_team_name(team_details)
            team_player_dict = self.create_team_player_dict(team_roster, team_name, self.league)
            # Combining Dictionaries
            print("Finishing:", team_details, "Amount of Players on Roster:", len(team_player_dict))
            self.league_roster_dict = {**self.league_roster_dict, **team_player_dict}
        return

    def create_team_player_dict(self, team_roster, team_name, league):
        """
        :param team_roster: Roster Object from sportsreference package
        :param team_name: UPPER CASE TEAM NAME i.e. YANKEES
        :param league: NFL/MLB/NHL/NBA
        :return: dictionary of specific players for a team
        """
        team_player_dict: dict = {}
        for player in team_roster.players:
            try:
                # If the player doesn't have a name
                # TODO add ability to scrape for name
                if player.name == None:
                    continue
                position = self.get_position(player)
                player_instance = Player(display=player.name, team=team_name, position=position,
                                         player_id=player.player_id)
                # Checking Duplicate Names
                if NLPConversionUtil().normalize_text(player_instance.display) in self.league_roster_dict:
                    self.handle_duplicate_names(player_instance)
                else:
                    team_player_dict[NLPConversionUtil().normalize_text(player_instance.display)] = vars(
                        player_instance)
            except AttributeError as err:
                # Some players have a name as None in sportsreference dict
                print(team_name, err)
        return team_player_dict

    def handle_duplicate_names(self, player_instance: Player):
        existing_player: dict = self.league_roster_dict[NLPConversionUtil().normalize_text(player_instance.display)]
        if existing_player["player_id"] == player_instance.player_id:
            # Getting the current team from sports reference, this issue happens when a player is on different
            # teams in the same season ex: MLB moralke01, so we are pulling from web page directly if this happens
            print("This is the Same person!", existing_player, vars(player_instance))
            current_team = self._scrape_sports_reference_for_players_team(player_instance.player_id)
            print("Current Team Scraped from Sports Reference:", current_team)
            if current_team in self._get_valid_team_names():
                formatted_team = NLPConversionUtil().normalize_text(current_team)
                self.league_roster_dict[NLPConversionUtil().normalize_text(player_instance.display)]["team"] \
                    = formatted_team
            else:
                del self.league_roster_dict[NLPConversionUtil().normalize_text(player_instance.display)]
        else:
            print("These are different people, welcome to the Michael Jordan Data quality issue, removing this "
                  "person from Banter reference dictionary",
                  existing_player, vars(player_instance))
            self.duplicate_names.append(vars(player_instance))
            self.duplicate_names.append(
                self.league_roster_dict[NLPConversionUtil().normalize_text(player_instance.display)])
            del self.league_roster_dict[NLPConversionUtil().normalize_text(player_instance.display)]

    def save_dict(self, dictionary, file_name):
        tmp_json = json.dumps(dictionary)
        f = open(f"{SAVE_LOCATION}/{file_name}.json", "w")
        f.write(tmp_json)
        f.close()

    def save_league_roster_dict(self, file_name):
        tmp_json = json.dumps(self.league_roster_dict)
        f = open(f"{SAVE_LOCATION}/{file_name}.json", "w")
        f.write(tmp_json)
        f.close()

    # Not used for time being, may be useful in future for manually scraping Rosters
    def _scrape_sports_reference_for_roster(self, roster_url: str, team_name):
        soup = self._return_soup_object(roster_url)
        roster: dict = {}
        for index, table in enumerate(soup.find_all('tbody')):
            if index == 0:
                pass
            else:
                anchors = table.find_all('tr')
                for row in anchors:
                    player_info = row.find('td', attrs={'data-stat': 'player'})
                    player_id = player_info.get('data-append-csv')
                    name = player_info.a.get_text()
                    position_info = row.find('td', attrs={'data-stat': 'pos'})
                    position = position_info.get_text().upper()
                    if position not in FANTASY_FOOTBALL_POSITIONS:
                        position = ''
                    player_instance = Player(display=name, team=team_name, position=position, player_id=player_id)
                    roster[NLPConversionUtil().normalize_text(player_instance.display)] = vars(player_instance)
        return roster

    def manually_fix_roster_dict(self, league, leage_roster_dict):
        if league == 'MLB':
            return self._manually_fix_mlb_dict(leage_roster_dict)
        elif league == 'NFL':
            return self._manually_fix_nfl_dict(leage_roster_dict)
        elif league == 'NBA':
            return self._manually_fix_nba_dict(leage_roster_dict)
        elif league == 'NHL':
            return self._manually_fix_nhl_dict(leage_roster_dict)

    def _manually_fix_nba_dict(self, league_roster_dict):
        fixed_dict = self._manually_fix_nba_positions(league_roster_dict)
        return fixed_dict

    def _manually_fix_nfl_dict(self, league_roster_dict):
        removed_dict = self._manually_fix_nfl_delete_from_dict(league_roster_dict)
        fixed_dict = self._manually_fix_nfl_add_to_dict(removed_dict)
        return fixed_dict

    def _manually_fix_mlb_dict(self, league_roster_dict):
        return league_roster_dict

    def _manually_fix_nhl_dict(self, league_roster_dict):
        return league_roster_dict

    def _manually_fix_nfl_delete_from_dict(self, league_roster_dict):
        try:
            del league_roster_dict["MICHAEL JORDAN"]
            return league_roster_dict
        except:
            return league_roster_dict

    def _manually_fix_nfl_add_to_dict(self, league_roster_dict):
        try:
            league_roster_dict["MICHAEL THOMAS"] = {"display": "Michael Thomas", "team": "NEW ORLEANS SAINTS",
                                                    "position": "WR", "player_id": "ThomMi05"}
            league_roster_dict["JOSH ALLEN"] = {'display': 'Josh Allen', 'team': 'BUFFALO BILLS', 'position': 'QB',
                                                'player_id': 'AlleJo02'}
            return league_roster_dict
        except:
            return league_roster_dict
