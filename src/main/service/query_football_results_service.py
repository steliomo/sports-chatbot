from main.application import QueryFootballResultsUseCase
from main.domain import Response

class QueryFootballResultsService(QueryFootballResultsUseCase):

    def query(self, query: str):
        
        return Response("Hello, Liverpool won 2-0.")

