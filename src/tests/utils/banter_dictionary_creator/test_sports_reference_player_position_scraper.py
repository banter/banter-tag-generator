import unittest

from src.main.utils.banter_dictionary_creator.sports_reference_player_scraper import SportsReferencePlayerScraper


class TestSportsReferenceScraper(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.scraper = SportsReferencePlayerScraper("NFL")

    def test_create_player_url(self):
        response = self.scraper._create_player_url("GoffJa00")
        self.assertEqual(response, "https://www.pro-football-reference.com/players/G/GoffJa00.htm")

    def test_web_scrape_single_position(self):
        player_id = "CrosMa20"
        response = self.scraper._scrape_sports_reference_for_nfl_players_position(player_id)
        self.assertEqual('K', response)
        player_id = "HoopAu00"
        response = self.scraper._scrape_sports_reference_for_nfl_players_position(player_id)
        self.assertEqual('TE', response)


if __name__ == '__main__':
    unittest.main()
