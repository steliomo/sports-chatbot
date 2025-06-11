from abc import ABC, abstractmethod

class NlpProcessor(ABC):

    @abstractmethod
    def process_query(self, query):
        pass