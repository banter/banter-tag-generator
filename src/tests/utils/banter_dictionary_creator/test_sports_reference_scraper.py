import unittest

from src.main.utils.banter_dictionary_creator.sports_reference_scraper import SportsReferenceScraper


class TestSportsReferenceScraper(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.scraper = SportsReferenceScraper()

    def test_web_scrape_single_position(self):
        player_id = "CrosMa20"
        response = self.scraper.scrape_nfl(player_id)
        self.assertEqual('K', response)
        player_id = "HoopAu00"
        response = self.scraper.scrape_nfl(player_id)
        self.assertEqual('TE', response)


if __name__ == '__main__':
    unittest.main()
