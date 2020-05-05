from utils import HelperClass
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

        self.helper_class.save_to_existing_dict_summary()
        pass

