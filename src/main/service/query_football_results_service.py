
from src.main.spi import NlpProcessor
from src.main.api import QueryFootballResultsUseCase
from src.main.domain import Response

class QueryFootballResultsService(QueryFootballResultsUseCase):

    def __init__(self, nlp: NlpProcessor):
        self.nlp = nlp

    def query(self, query: str):
        
        return Response("Hello, Liverpool won 2-0.")

