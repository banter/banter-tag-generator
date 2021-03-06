import os
import unittest
from os.path import dirname, realpath

from src.main.utils.nlp_resource_util import NLPResourceUtil

BASEDIR = os.path.abspath(os.path.dirname(dirname(dirname(realpath(__file__)))))
from sportsreference.nfl.roster import Roster as NFLRoster
from sportsreference.nba.roster import Roster as NBARoster
from src.main.utils.banter_dictionary_creator.sports_reference_roster_scraper import SportsReferenceRosterScraper, \
    Player


class TestSportsReferenceScraper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.buffalo_roster = NFLRoster('BUF', '2019', False)
        cls.cin_roster = NFLRoster('CIN', '2020', False)
        cls.sf_roster = NFLRoster('SFO', '2020', False)
        cls.den_roster = NBARoster('DEN', '2020', False)
        cls.nfl_scraper = SportsReferenceRosterScraper(league="NFL")
        cls.mlb_scraper = SportsReferenceRosterScraper(league="MLB")
        cls.nba_scraper = SportsReferenceRosterScraper(league="NBA")
        cls.util = NLPResourceUtil()
        FIXTURE_LOCATION = '%s/resources/fixtures/league_rosters' % BASEDIR
        cls.nfl_integration_test_fixture = cls.util.read_json_file(FIXTURE_LOCATION,
                                                                   "NFL_player_dict_2019.json")

    def create_team_roster_validation(self, player_dict: dict, team_name: str):
        team = {}
        for key, value in player_dict.items():
            if value["team"] == team_name:
                team[key] = value
        return team

    def remove_player_id_for_test_verification(self, response: dict):
        for key, value in response.items():
            del value['player_id']
        return response

    def test_get_list_of_abbreviations(self):
        response = self.nfl_scraper.get_list_of_team_details()
        print(response)
        self.assertEqual(len(response), 32)

    def test_get_list_of_abbreviations_raiders(self):
        response = self.nfl_scraper.get_list_of_team_details()
        count = 0
        for team in response:
            if team["team_name"] == "Las Vegas Raiders":
                count += 1
            if team["team_name"] == "Oakland Raider":
                count -= 1
        self.assertEqual(count, 1)

    @unittest.skip("Skipping Test for Bills")
    def test_get_team_roster(self):
        team_roster = self.nfl_scraper.get_team_roster("BUF")
        self.assertEqual(type(self.buffalo_roster), type(team_roster))

    def test_create_team_player_dict_sf(self):
        scraped = self.nfl_scraper.create_team_player_dict(self.sf_roster, "SAN FRANCISCO 49ERS", "NFL")
        print("Scraped", scraped)
        scraped = self.remove_player_id_for_test_verification(scraped)
        print(self.nfl_scraper.duplicate_names)
        self.assertEqual(False, "AJ GREEN" in scraped)
        self.assertEqual(True, "GEORGE KITTLE" in scraped)

    def test_create_team_player_dict_den(self):
        scraped = self.nba_scraper.create_team_player_dict(self.den_roster, "DENVER NUGGETS", "NBA")
        print("Scraped", scraped)
        scraped = self.remove_player_id_for_test_verification(scraped)
        print(self.nfl_scraper.duplicate_names)
        self.assertEqual(True, "BOL BOL" in scraped)
        self.assertEqual(False, "GEORGE KITTLE" in scraped)

    def test_create_team_player_dict_cin(self):
        scraped = self.nfl_scraper.create_team_player_dict(self.cin_roster, "CINCINNATI BENGALS", "NFL")
        print("Scraped", scraped)
        scraped = self.remove_player_id_for_test_verification(scraped)
        print(self.nfl_scraper.duplicate_names)
        self.assertEqual(True, "AJ GREEN" in scraped)
        self.assertEqual(False, "RODNEY ANDERSON" in scraped)

    @unittest.skip("Skipping Bills Test")
    def test_create_team_player_dict_bills(self):
        bills_roster = self.nfl_scraper.create_team_player_dict(self.buffalo_roster, "BUFFALO BILLS", "NFL")
        bills_roster = self.remove_player_id_for_test_verification(bills_roster)
        expected_roster = self.create_team_roster_validation(self.nfl_integration_test_fixture, 'BUFFALO BILLS')
        print("Scraped", bills_roster)
        print("Reference", expected_roster)
        print(self.nfl_scraper.duplicate_names)
        self.assertEqual(bills_roster, expected_roster)

    def test_handle_duplicate_names_same_player_id(self):
        self.nfl_scraper.league_roster_dict = {"JARED GOFF": {"display": "Jared Goff",
                                                              "team": "WRONG TEAM",
                                                              "position": "P",
                                                              "player_id": "GoffJa00"}}
        self.nfl_scraper.handle_duplicate_names(Player("JARED GOFF", "WRONG TEAM 2", "RB", "GoffJa00"))
        expected = {"JARED GOFF": {"display": "Jared Goff",
                                   "team": "LOS ANGELES RAMS",
                                   "position": "P",
                                   "player_id": "GoffJa00"}}
        self.assertEqual(self.nfl_scraper.league_roster_dict, expected)

    def test_handle_duplicate_names_same_player_id_no_current_team(self):
        self.mlb_scraper.league_roster_dict = {"MIKE WRIGHT": {"display": "Mike Wright",
                                                               "team": "TEAM 1",
                                                               "position": "P",
                                                               "player_id": "wrighmi01"}}
        self.mlb_scraper.handle_duplicate_names(Player("Mike Wright", "TEAM 2", "RB", "wrighmi01"))
        self.assertEqual(self.mlb_scraper.league_roster_dict, {})

    def test_handle_duplicate_names_different_player_id(self):
        self.nfl_scraper.league_roster_dict = {"JARED GOFF": {"display": "Jared Goff",
                                                              "team": "TEAM 1",
                                                              "position": "P",
                                                              "player_id": "GoffJa01"}}
        self.nfl_scraper.handle_duplicate_names(Player("JARED GOFF", "TEAM 2", "RB", "GoffJa00"))
        expected = {}
        self.assertEqual(self.nfl_scraper.league_roster_dict, expected)

    def test_manually_fix_nba_positions(self):
        result = self.nba_scraper.manually_fix_roster_dict("NBA", {"JIMMY BUTLER": {"position": "SG-SF"}})
        self.assertEqual(result, {"JIMMY BUTLER": {"position": "SF"}})

    def test_manually_fix_nfl_dict(self):
        result = self.nfl_scraper.manually_fix_roster_dict("NFL", {"MICHAEL JORDAN": {"position": "SG-SF"}})
        expected = {
            "JOSH ALLEN": {'display': 'Josh Allen', 'team': 'BUFFALO BILLS', 'position': 'QB', 'player_id': 'AlleJo02'},
            "MICHAEL THOMAS": {"display": "Michael Thomas", "team": "NEW ORLEANS SAINTS", "position": "WR",
                               "player_id": "ThomMi05"}}
        self.assertEqual(result, expected)

    @unittest.skip("Skip this unless verifying the new results")
    def test_post_dict_creation(self):
        self.assertTrue(self.util.sports_player_dict["NFL"]["TOM BRADY"].team == "TAMPA BAY BUCCANEERS")
        self.assertTrue(self.util.sports_player_dict["NFL"]["STEFON DIGGS"].team == "BUFFALO BILLS")
        self.assertTrue(self.util.sports_player_dict["MLB"]["AARON JUDGE"].position == "OF")
        self.assertTrue(self.util.sports_player_dict["MLB"]["RYAN DULL"].position == "TORONTO BLUE JAYS")
        self.assertTrue(self.util.sports_player_dict["NBA"]["JIMMY BUTTLER"].position == "SF")
        self.assertTrue(self.util.sports_player_dict["NBA"]["THON MAKER"].position == "C")
        self.assertFalse("MICHAEL JORDAN" in self.util.sports_player_dict["NFL"])


if __name__ == '__main__':
    unittest.main()
