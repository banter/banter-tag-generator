import unittest

from src.main.tag_identifier import TagIdentifier

test_list = ["Cowboys lose Browns bounce back",
             "Bucs win",
             "TB12 declining?",
             "Burfict suspended"]


class TestTagIdentifier(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        super(TestTagIdentifier, self).setUpClass()
        self.tag_identifier = TagIdentifier()
