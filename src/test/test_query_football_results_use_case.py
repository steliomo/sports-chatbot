import unittest

from src.main.service import QueryFootballResultsService

class TestQueryFootbalResultsUseCase (unittest.TestCase):

    def test_query_football_results_use_case(self):

        query = "Hi, who won the much between Liverpool and Manchaster City and how many goals?"

        query_footbal_results_service = QueryFootballResultsService()

        response = query_footbal_results_service.query(query)

        self.asserEquals(response.message(), "Hello, Liverpool won 2-0.")

if __name__ == '__main__':
    unittest.main()