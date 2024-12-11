import streamlit as st
from groq import Groq
from streamlit_chat import message
from dotenv import load_dotenv
import os
from db import fetch_case_information
import logging
from streamlit import logger

logger = logging.getLogger('chatbot-')

load_dotenv()
USER_ID = os.environ.get("USER_ID")

def human_expert_agent():
    logger.info("Requesting human expert agent")
    return "Your query has been forwarded to a human expert. They will contact you shortly."

def chat_error(exception):
    logger.info(f"Internal Error occurred.{exception}")
    return "Chat is unavailable due to some technical issues. Please contact us via our email or contact number. "

def intent_checker_agent(prompt):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are an intent checker for a given question."""
            },
            {
                "role": "user",
                "content": f"""
                *Instructions:
                ONLY output a single digit while responding. Output either 0,1,2,3 for the provided question using following conditions.
                1. If question is related to getting the status of the case, output "0". 
                2. If question is about asking a human help or something pertaining to the conveyancing domain that you are not aware of , output "1".
                3. Otherwise, output "2"
                *Question: {prompt}

                *Output:
                """
            }
        ],
        model="llama3-70b-8192",
    )
    response = chat_completion.choices[0].message.content
    if len(response)==1:
        logger.info(f"Intent checker generated code,",response)
        return response
    else:
        logger.error(f"Intent checker failed to generate proper code.")
        return "-1"

def db_agent():
    case_information = fetch_case_information(USER_ID)
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant with professional personality."""
            },
            {
                "role": "user",
                "content": f"""
                *Instructions:
                -You work for the company named WSG Strategies based in the UK.
                -Answer only with the following update about the user's case status. Do not respond with any extra information.
                -If you get multiple fields separated by comma, respond in the following format: 
                    
                        ->User: <first field>
                        ->Status: <second field>
                        ->Details: <third_field>
                        ->Documents: <third_field>
                -If not, respond with the provided case information.
                
                *Case Information :{case_information}"""
            }
        ],
        model="llama3-8b-8192",
    )
    response = chat_completion.choices[0].message.content
    return response
    

def answer_responder_agent(prompt):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant with professional personality."""
            },
            {
                "role": "user",
                "content": f"""
                *Instructions:
                -You work for the company named WS Strategic based in the UK.
                -Greet them back if the user greet you and inquire about how you can help them regarding any conveyancing related queries.
                -Answer only for conveyancing queries of the company named. Also, make sure that you answer ONLY and ONLY when the query is related to legal conveyancing process in the UK.
                -For other queries, politely deny to reveal any information with small talk.

                *Query:{prompt}"""
            }
        ],
        model="llama3-70b-8192",
    )
    response = chat_completion.choices[0].message.content
    return response

st.title("WS Strategic Conveyancing bot")
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = []

if 'openai_response' not in st.session_state:
    st.session_state['openai_response'] = []

def get_text():
    input_text = st.text_input("Enter your conveyancing query", key="input")
    return input_text

user_input = get_text()

if user_input:
    intent_response = intent_checker_agent(user_input)
    logger.info(f"Intent responder:{intent_response}")
    print(f"Intent responder:{intent_response}")
    if intent_response =="0":
        try:
            output = db_agent()
        except Exception as e:
            logger.exception(f"Exception occurred:{e}")
            output = human_expert_agent()
    elif intent_response=="1":
        output = human_expert_agent()
    else:
        output = answer_responder_agent(user_input)
    st.session_state.user_input.append(output)
    st.session_state.openai_response.append(user_input)
    
message_history = st.empty()

if st.session_state['user_input']:
    for i in range(len(st.session_state['user_input']) - 1, -1, -1):
        message(st.session_state["user_input"][i],
                key=str(i), avatar_style="icons")
        message(st.session_state['openai_response'][i],
                avatar_style="bottts", is_user=True
                , key=str(i) + 'data_by_user')