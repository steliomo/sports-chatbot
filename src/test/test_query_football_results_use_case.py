import unittest
from unittest.mock import patch

from src.main.spi import NlpProcessor
from src.main.service import QueryFootballResultsService

class TestQueryFootbalResultsUseCase (unittest.TestCase):

    @patch('src.main.spi.nlp_processor')
    def test_query_football_results_use_case(self,nlp_processor: NlpProcessor ):

        query = "Hi, who won the much between Liverpool and Manchaster City and how many goals?"

        query_footbal_results_service = QueryFootballResultsService(nlp_processor)

        response = query_footbal_results_service.query(query)

        self.assertEqual(response.get_message(), "Hello, Liverpool won 2-0.")

if __name__ == '__main__':
    unittest.main()