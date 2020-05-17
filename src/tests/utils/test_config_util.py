import unittest

from src.main.utils.config_util import LanguageConfig
from src.main.utils.config_util import SportsConfig


class TestConfig(unittest.TestCase):

    # Iterating through all of the class variables and maxing sure they exist
    def test_sports_config_variables(self):
        for attr, value in SportsConfig.__dict__.items():
            if "__" in attr:
                pass
            else:
                self.assertIsNotNone(value)

    def test_language_config_variables(self):
        for attr, value in LanguageConfig.__dict__.items():
            if "__" in attr:
                pass
            else:
                self.assertIsNotNone(value)


if __name__ == '__main__':
    unittest.main()
