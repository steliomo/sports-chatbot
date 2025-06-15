import unittest
from unittest.mock import patch

from src.main.spi import NlpProcessor
from src.main.service import QueryFootballResultsService

class TestQueryFootbalResultsUseCase (unittest.TestCase):

    @patch('src.main.spi.nlp_processor')
    def test_query_football_results_use_case(self,nlp_processor: NlpProcessor ):

        message = "The match between Liverpool and Manchaster City ended 2-0 on 2025-06-14."

        nlp_processor.determine_intent.return_value = "MATCH_RESULT"

        nlp_processor.process_intent.return_value = message
        
        query = "Who won the much between Liverpool and Manchaster City and how many goals?"

        query_footbal_results_service = QueryFootballResultsService(nlp_processor)

        response = query_footbal_results_service.query(query)

        self.assertEqual(response.get_message(), message)

if __name__ == '__main__':
    unittest.main()