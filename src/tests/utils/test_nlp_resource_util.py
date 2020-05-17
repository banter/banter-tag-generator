import unittest
from src.main.utils.nlp_resource_util import NLPResourceUtil

class TestNLPResourceUtil(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.nlp_resource = NLPResourceUtil()

    # Iterating through all of the class variables and maxing sure they exist
    def test_sports_reference_dicts(self):
        members = [attr for attr in dir(self.nlp_resource) if not callable(getattr(self.nlp_resource, attr)) and not attr.startswith("__")]
        for attr, member in enumerate(members):
            self.assertIsNotNone(self.nlp_resource.__getattribute__(member))


if __name__ == '__main__':
    unittest.main()
