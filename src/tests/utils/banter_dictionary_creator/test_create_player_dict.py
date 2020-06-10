import os
import unittest
from os.path import dirname, realpath

from src.main.utils.banter_dictionary_creator.create_player_dict import PositionGenerator
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
            position = PositionGenerator().get_position(player, league_and_response['league'])
            print(player_id, league_and_response, position)
            self.assertCountEqual(position, league_and_response['response'])

    def test_lebron(self):
        lebron = NBAPlayer('jamesle01')
        position = PositionGenerator().get_position(lebron, 'NBA')
        self.assertEqual(position, 'SF')

    def test_terrance_ferg(self):
        terrance_fergeson = NBAPlayer('fergute01')
        position = PositionGenerator().get_position(terrance_fergeson, 'NBA')
        self.assertEqual(position, 'SG')

    def test_PositionGenerator(self):
        player = TestPlayer(['SS', '2B', 'RF'])
        position = PositionGenerator().get_position(player, 'MLB')
        self.assertEqual(position, 'SS')

    def test_get_position_of(self):
        player = TestPlayer(['CF', 'OF', 'RF'])
        position = PositionGenerator().get_position(player, 'MLB')
        self.assertEqual(position, 'OF')

    def test_get_position_outfield_not_main_position(self):
        player = TestPlayer(['1B', 'OF', 'RF'])
        position = PositionGenerator().get_position(player, 'MLB')
        self.assertEqual(position, '1B')

    def test_get_position_bball(self):
        cp3 = NBAPlayer('paulch01')
        position = PositionGenerator().get_position(cp3, 'NBA')
        self.assertEqual(position, 'PG')

    def test_get_position_football(self):
        player = TestPlayer('QB/RB/DT')
        position = PositionGenerator().get_position(player, 'NFL')
        self.assertEqual(position, 'QB')

    def test_get_position_NFL_non_fantasy(self):
        player = TestPlayer('DT')
        position = PositionGenerator().get_position(player, 'NFL')
        self.assertEqual(position, '')

    def test_get_position_NFL_after_empty(self):
        player = TestPlayer(['', 'RB', ''])
        position = PositionGenerator().get_position(player, 'NFL')
        self.assertEqual(position, 'RB')

    def test_get_position_NFL_after_empty_non_fantasy_position(self):
        player = TestPlayer(['', 'DT', ''])
        position = PositionGenerator().get_position(player, 'NFL')
        self.assertEqual(position, '')

    def test_get_position_no_position(self):
        player = TestPlayerNoPosition()
        position = PositionGenerator().get_position(player, 'MLB')
        self.assertEqual(position, '')


if __name__ == '__main__':
    unittest.main()
