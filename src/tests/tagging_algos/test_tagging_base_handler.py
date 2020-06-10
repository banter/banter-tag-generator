import unittest
from typing import *

from src.main.models.tag_model import TagModel
from src.main.tagging_algos.tagging_base_handler import TaggingBaseHandler


class TestTaggingBaseHandler(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        super(TestTaggingBaseHandler, self).setUpClass()
        self.base_handler = TaggingBaseHandler()

    def remove_confidence_for_test_verification(self, response: List[TagModel]):
        """
        :param response: Response from method being tested
        :return:
        """
        for tag in response:
            del tag['confidence']
        return response

    def test_get_person_tags(self):
        sample = {'text': 'Cam Bedrosian', 'type': 'PERSON', 'start_char': 13, 'end_char': 19}
        response = self.base_handler.get_person_tags(sample)
        response = self.remove_confidence_for_test_verification(response)
        valid_response = [{'type': 'person', 'value': 'Cam Bedrosian', 'isPrimary': True}]
        self.assertCountEqual(response, valid_response)

    def test_generate_tags_non_specific(self):
        sample = "Hello this is Joe Rogan and im glad to be on the Banter Podcast."
        valid_response = [{'type': 'person', 'value': 'Joe Rogan', 'isPrimary': True}]
        response = self.base_handler.get_basic_tags(sample)
        response = self.remove_confidence_for_test_verification(response)
        self.assertEqual(response, valid_response)


if __name__ == '__main__':
    unittest.main()
