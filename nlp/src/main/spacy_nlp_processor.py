import random
import spacy
import pandas as pd

from spacy.matcher import Matcher
from src.main.spi import NlpProcessor

class SpacyNlpProcessor(NlpProcessor):
    
    def __init__(self):
      self.nlp = spacy.load('en_core_web_sm')

      self.matches = pd.read_csv('../nlp/data/matches.csv')
      self.matches['date'] = pd.to_datetime(self.matches['date']).dt.date
      self.matches['result'] = self.matches['result'].map({'L': 'lost', 'W': 'won', 'D':'drew'})
      self.matches = self.matches.sort_values('date')

      self.teams_data = pd.read_excel('../nlp/data/teams.xlsx')
      self.teams_data['pts'] = self.teams_data['pts'].astype(int)
      self.teams_data['goals'] = self.teams_data['goals'].astype(int)
      
      # Initialize matcher
      self.matcher = Matcher(self.nlp.vocab)

      self.matcher.add(self.GREETING,[
         [{"LOWER": {"IN":['hi', 'hello', 'hey']}}],
         [{"LOWER":"how"}, {"LOWER":"are"}, {"LOWER":"you"}]
      ])

      self.matcher.add(self.LIST_TEAMS, [
         [{"LOWER":"can"}, {"LOWER": "you"}, {"LOWER":"list"}],
         [{"LOWER":"list"}]
      ])

      self.matcher.add(self.TEAM_CLASSIFICATION, [
         [{"LOWER":"how"}, {"LOWER": "many"}, {"LOWER":"points"}, {"LOWER":"does"}, {"ENT_TYPE": "TEAM", "OP": "*"}],
         [{"LOWER":"points"}, {"LOWER": "of"}, {"ENT_TYPE": "TEAM", "OP": "*"}]
      ])

      self.matcher.add(self.TEAMS_NUMBER, [
         [{"LOWER":"how"}, {"LOWER": "many"}, {"LOWER":"teams"}],
         [{"LOWER":"teams"}]
      ])

      self.matcher.add(self.MATCH_RESULT,[
        [{"LOWER": "did"}, {"ENT_TYPE": "TEAM", "OP": "*"}, {"LEMMA": "win"}],
        [{"LOWER": "did"}, {"ENT_TYPE": "TEAM", "OP": "*"}, {"LEMMA": "lose"}],
        [{"LOWER": "score"}, {"LOWER": "between"}, {"ENT_TYPE": "TEAM", "OP": "*"}, {"LOWER": "and"}, {"ENT_TYPE": "TEAM", "OP": "*"}],
        [{"LOWER": "result"}, {"LOWER": "of"}, {"ENT_TYPE": "TEAM", "OP": "*"}, {"LOWER": "vs"}, {"ENT_TYPE": "TEAM", "OP": "*"}],
        [{"LOWER": "who"}, {"LEMMA": "win"}, {"LOWER": "between"}, {"ENT_TYPE": "TEAM", "OP": "*"}, {"LOWER": "and"}, {"ENT_TYPE": "TEAM", "OP": "*"}],
        [{"ENT_TYPE": "TEAM", "OP": "*"}, {"LOWER": "'s",  "OP": "*"}, {"LOWER": "last"}, {"LOWER": "result"}],
        [{"ENT_TYPE": "TEAM", "OP": "*"}, {"LOWER": "last"}, {"LOWER": "match"}]
      ])

      # load premier teams
      premier_teams = self.matches['team'].unique()
      
      ruler = self.nlp.add_pipe("entity_ruler", before="ner", config={"overwrite_ents": True})
      ruler.add_patterns([{"label": "TEAM", "pattern": team.lower()} for team in premier_teams])

    def determine_intent(self, query):
       
       intent = self.UNKOWN_INTENT

       self.document = self.nlp(query.lower())
       matches = self.matcher(self.document)
       
       if matches:
          intent_id = matches[0][0]
          intent = self.nlp.vocab.strings[intent_id]

          return intent

       return intent

    def process_intent(self, intent):
       
       if self.UNKOWN_INTENT == intent:
          return "Sorry, I did not understand that."
       
       if self.GREETING == intent:
          return random.choice(["Hello! How can I assist you today?",
                                "Hey! What can I help you with?",
                                "Good to see you! Ready to talk about the Premier League?"])
       
       if self.LIST_TEAMS == intent:
          teams = self.matches['team'].unique()

          teams = "Yes the teams are: \n"+"\n".join(f"{i}. {team}" for i, team in enumerate(teams, start=1))

          return teams
       
       if self.TEAMS_NUMBER == intent:
        
          return f"The Premier League as a total of {len(self.matches['team'].unique())} teams"
       
       if self.TEAM_CLASSIFICATION == intent:
          team = [team.text for team in self.document.ents if team.label_ == 'TEAM'][0]

          team = self.teams_data[self.teams_data['team'].str.lower() == team].to_dict(orient='records')

          if len(team) == 0:
             return "Sorry I don't have the requested data."
          
          team = team[0]

          return f"{team['team']} has {team['pts']} point(s) and the top scorer is: {team['scorer']}, with a total of {team['goals']} goal(s)." 
       
       if self.MATCH_RESULT == intent:
          
          teams = [team.text for team in self.document.ents if team.label_ == 'TEAM']

          if len(teams) == 1:
            team = self.matches[self.matches['team'].str.lower() == teams[0]].tail(1).to_dict(orient='records')[0]

          if len(teams) == 2:
            team = self.matches[(self.matches['team'].str.lower() == teams[0]) & (self.matches['opponent'].str.lower() == teams[1])].tail(1).to_dict(orient='records')[0]

          if team['result'] == 'drew':
             return f"{team['team']} {team['result']} {team['gf']}-{team['ga']} with {team['opponent']} on {team['date']}" 
          
          return f"{team['team']} {team['result']} {team['gf']}-{team['ga']} against {team['opponent']} on {team['date']}"