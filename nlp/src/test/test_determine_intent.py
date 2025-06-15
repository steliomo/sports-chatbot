import unittest

from nlp.src.main import SpacyNlpProcessor

class TestDetermineIntent(unittest.TestCase):

    def test_should_return_greeting_intent(self):
        query = "Hey"

        nlp_processor = SpacyNlpProcessor()

        intent = nlp_processor.determine_intent(query)

        self.assertEqual(intent, 'GREETING')

    def test_should_return_match_result_intent(self):
        query = "Did Liverpool won?"

        nlp_processor = SpacyNlpProcessor()

        intent = nlp_processor.determine_intent(query)

        self.assertEqual(intent, 'MATCH_RESULT')

if __name__ == '__main__':
    unittest.main()