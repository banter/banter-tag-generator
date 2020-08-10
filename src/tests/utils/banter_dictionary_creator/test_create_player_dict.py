import os
import unittest
from os.path import dirname, realpath

from src.main.utils.banter_dictionary_creator.sports_reference_player_scraper import SportsReferencePlayerScraper
from src.main.utils.nlp_resource_util import NLPResourceUtil

BASEDIR = os.path.abspath(os.path.dirname(dirname(dirname(realpath(__file__)))))
from sportsreference.nba.roster import Player as NBAPlayer
from sportsreference.nfl.roster import Player as NFLPlayer
from sportsreference.mlb.roster import Player as MLBPlayer
from sportsreference.nhl.roster import Player as NHLPlayer


class TestPlayer():
    def __init__(self, position, player_id=None):
        self.position = None
        self._position = position
        self.player_id = player_id


class TestPlayerNoPosition():
    def __init__(self):
        pass


class TestCreatePlayerDict(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.util = NLPResourceUtil()
        FIXTURE_LOCATION = '%s/resources/fixtures' % BASEDIR
        self.integration_test_fixture = self.util.read_json_file(FIXTURE_LOCATION,
                                                                 "create_player_dict_position_fixture.json")

    # @unittest.skip("Skip when testing locally, this is a full integration test, uncomment in production")
    def test_get_sports_tags_normalized_text_test(self):
        for (player_id, league_and_response) in self.integration_test_fixture.items():
            if league_and_response['league'] == "NFL":
                player = NFLPlayer(player_id)
            elif league_and_response['league'] == "NBA":
                player = NBAPlayer(player_id)
            elif league_and_response['league'] == "MLB":
                player = MLBPlayer(player_id)
            else:
                player = NHLPlayer(player_id)
            position = SportsReferencePlayerScraper(league_and_response['league']).get_position(player)
            print(player_id, league_and_response, position)
            self.assertCountEqual(position, league_and_response['response'])

    def test_lebron(self):
        lebron = NBAPlayer('jamesle01')
        position = SportsReferencePlayerScraper('NBA').get_position(lebron)
        self.assertEqual(position, 'SF')

    def test_denzel_valentine(self):
        denzel = NBAPlayer('valende01')
        position = SportsReferencePlayerScraper('NBA').get_position(denzel)
        self.assertEqual('SG', position)

    def test_dejounte_murray(self):
        murray = NBAPlayer('murrade01')
        position = SportsReferencePlayerScraper('NBA').get_position(murray)
        self.assertEqual('PG', position)

    def test_bol_bol(self):
        bol = NBAPlayer("bolbo01")
        position = SportsReferencePlayerScraper('NBA').get_position(bol)
        self.assertEqual('SF', position)


    def test_terrance_ferg(self):
        terrance_fergeson = NBAPlayer('fergute01')
        position = SportsReferencePlayerScraper('NBA').get_position(terrance_fergeson)
        self.assertEqual(position, 'SG')

    def test_PositionGenerator(self):
        player = TestPlayer(['SS', '2B', 'RF'])
        position = SportsReferencePlayerScraper('MLB').get_position(player)
        self.assertEqual(position, 'SS')

    def test_get_position_of(self):
        player = TestPlayer(['CF', 'OF', 'RF'])
        position = SportsReferencePlayerScraper('MLB').get_position(player)
        self.assertEqual(position, 'OF')

    def test_brantmi02(self):
        brantmi = MLBPlayer('brantmi02')
        position = SportsReferencePlayerScraper('MLB').get_position(brantmi)
        self.assertEqual(position, 'DH')


    def test_get_position_outfield_not_main_position(self):
        player = TestPlayer(['1B', 'OF', 'RF'])
        position = SportsReferencePlayerScraper('MLB').get_position(player)
        self.assertEqual(position, '1B')

    def test_get_position_bball(self):
        cp3 = NBAPlayer('paulch01')
        position = SportsReferencePlayerScraper('NBA').get_position(cp3)
        self.assertEqual(position, 'PG')


    def test_joe_burrow(self):
        burrow = NFLPlayer('BurrJo01')
        position = SportsReferencePlayerScraper('NFL').get_position(burrow)
        self.assertEqual(position, 'QB')

    def test_tua(self):
        burrow = NFLPlayer('TagoTu00')
        position = SportsReferencePlayerScraper('NFL').get_position(burrow)
        self.assertEqual(position, 'QB')

    def test_get_position_football(self):
        player = TestPlayer('QB/RB/DT')
        position = SportsReferencePlayerScraper('NFL').get_position(player)
        self.assertEqual(position, 'QB')

    def test_get_position_NFL_non_fantasy(self):
        player = TestPlayer('DT')
        position = SportsReferencePlayerScraper('NFL').get_position(player)
        self.assertEqual(position, '')

    def test_get_position_NFL_after_empty(self):
        player = TestPlayer(['', 'RB', ''])
        position = SportsReferencePlayerScraper('NFL').get_position(player)
        self.assertEqual(position, 'RB')

    def test_get_position_NFL_after_empty_non_fantasy_position(self):
        player = TestPlayer(['', 'DT', ''])
        position = SportsReferencePlayerScraper('NFL').get_position(player)
        self.assertEqual(position, '')

    def test_get_position_no_position(self):
        player = TestPlayerNoPosition()
        position = SportsReferencePlayerScraper('NFL').get_position(player)
        self.assertEqual(position, '')


if __name__ == '__main__':
    unittest.main()
