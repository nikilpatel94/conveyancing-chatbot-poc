# About
This is the PoC application for showcasing a rapid development of a simple multi-agent domain specific chatbot. 

Uses [Groq](https://groq.com/) and [Streamlit](https://streamlit.io/) and llama3 models to generate response.

Uses [sqlite3](https://docs.python.org/3/library/sqlite3.html) for database stuff.

## Domain
Conveyancing in the UK

## Simple Multi-agent chat application

1. `intent_checker_agent` checks for intent of the user query - internal interaction
2. `answer_responder_agent` responds to the end user - user exposure
3. `db_agent` queries database and parses into human readable format. 



# Instructions
## Environment variables:
GROQ_API_KEY=

USER_ID=stargazer94

## Python versions:
Python==3.13.0

pip==24.2

## How to try:

- Clone this repository
- Install python and upgrade pip if necessary
- Install libraries mentioned in the `requirements.txt`
- Create an `.env` file and populate your Groq api key under `GROQ_API_KEY`.
- Run `db_init.py` that should create some sample data for conveyancing demo. Make sure this creates `chatbot.db`file in the existing repository. 
- Open the command in the current folder and run the command `streamlit run ./chatbot.py` to start the server.



