from abc import ABC, abstractmethod

class NlpProcessor(ABC):

    GREETING = 'GREETING'

    LIST_TEAMS = 'LIST_TEAMS'

    TEAMS_NUMBER = 'TEAMS_NUMBER'

    MATCH_RESULT = 'MATCH_RESULT'

    UNKOWN_INTENT = 'UNKOWN_INTENT'

    @abstractmethod
    def determine_intent(self, query):
        pass

    @abstractmethod
    def process_intent(self, intent):
        pass