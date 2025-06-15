import unittest

from nlp.src.main import SpacyNlpProcessor

class TestProcessIntent(unittest.TestCase):
    
    nlp_processor = SpacyNlpProcessor()

    def test_should_process_greeting_intent(self):
        query = "Hi"

        message = "you"

        intent = self.nlp_processor.determine_intent(query)

        self.assertTrue(message in self.nlp_processor.process_intent(intent))


    def test_should_process_match_result_intent(self):
        query = "what was the result of Manchester City vs Manchester United"

        message = "Manchester City won 3-1 against Manchester United on 2024-03-03"
       
        intent = self.nlp_processor.determine_intent(query)

        self.assertEqual(self.nlp_processor.process_intent(intent), message)


    def test_should_process_match_result_intent_to_return_teams(self):
        query = "list teams"

        message = "Manchester City"
       
        intent = self.nlp_processor.determine_intent(query)

        result_message = self.nlp_processor.process_intent(intent)

        self.assertTrue(message in result_message)

if __name__ == '__main__':
    unittest.main()
