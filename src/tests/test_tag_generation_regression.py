from tag_identifier import TagIdentifier
import unittest

test_list = ["Cowboys lose Browns bounce back",
"Bucs win",
"TB12 declining?",
"Burfict suspended"]

class TestGenerateTags(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        super(TestGenerateTags, self).setUpClass()
        self.generate_tags = TagIdentifier(store_ml_data=False)


    def testTagGenerationFullRegression(self):
        pass

