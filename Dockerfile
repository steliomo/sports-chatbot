ARG PYTHON_VERSION=3.13.0
FROM python:${PYTHON_VERSION}-slim AS base

LABEL maintainer="stelio.moiane@iu-study.org" 

VOLUME [ "/opt/sports-chatbot/data" ]

WORKDIR /opt/sports-chatbot/data/sports-chatbot/ui

ENV PYTHONPATH="/opt/sports-chatbot/data/sports-chatbot"

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

RUN python -m pip install -U pip setuptools wheel
RUN python -m pip install -U spacy
RUN python -m spacy download en_core_web_sm
RUN python -m pip install pandas
RUN python -m pip install streamlit

# Expose the port that the application listens on.
EXPOSE 8501

# Run the application.
CMD streamlit run premier_chatbot.py