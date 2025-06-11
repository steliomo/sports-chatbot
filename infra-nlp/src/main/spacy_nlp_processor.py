import spacy
from src.main.spi import NlpProcessor

class SpacyNlpProcessor(NlpProcessor):

    def __init__(self):
      self.nlp = spacy.load('en_core_web_sm')

    def process_query(self, query):
        raise NotImplementedError
