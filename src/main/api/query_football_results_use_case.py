from abc import ABC, abstractmethod

class QueryFootballResultsUseCase(ABC):

    @abstractmethod
    def query(self, query: str):
        pass
