import unittest


class TestNLPGoogleUtil(unittest.TestCase):

    def test_something(self):
        self.assertEqual(True, True)

    # def test_get_google_search_results(self):
    #     sample = "TB12"
    #     response = self.tag_identifier.get_google_search_results(sample)
    #     print(response)
    #     valid_response = "['', '', 'The TB12 Method: How to Achieve a Lifetime of Sustained Peak Performance', 'Book by Tom Brady']"
    #     self.assertCountEqual(response, valid_response)
    #
    # def test_get_google_search_results_bucs(self):
    #
    #     sample = "Bucs"
    #     response = self.tag_identifier.get_google_search_results(sample)
    #     print(response)
    #
    #     self.assertNotEqual(response, [])


if __name__ == '__main__':
    unittest.main()
