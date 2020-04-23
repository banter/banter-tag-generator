from utils.helper_class import HelperClass
import unittest

test_list = ["Cowboys lose Browns bounce back",
"Bucs win",
"TB12 declining?",
"Burfict suspended"]

class TestGenerateTags(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        super(TestGenerateTags, self).setUpClass()
        self.helper_class = HelperClass()



    def testTagGenerationFullRegression(self):
        sample_list = []

        self.helper_class.add_to_ml_data()
        pass

