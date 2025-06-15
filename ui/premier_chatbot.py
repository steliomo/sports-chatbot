import streamlit as st

from src.main.service import QueryFootballResultsService
from nlp.src.main import SpacyNlpProcessor

st.title("Premier League!")

# intitialize the messages
if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask about Premier League")

query_football_results_use_case = QueryFootballResultsService(SpacyNlpProcessor())

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = query_football_results_use_case.query(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response.get_message()})

# Dispaly messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])