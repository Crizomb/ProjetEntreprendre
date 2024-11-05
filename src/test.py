import os
from mistralai import Mistral

import streamlit as st
import requests
from dotenv import load_dotenv
# check https://pypi.org/project/python-dotenv/ to add MISTRAl_KEY to a .env
load_dotenv()

MISTRAl_KEY = os.getenv("MISTRAL_KEY")
model = "ministral-3b-latest"
client = Mistral(api_key=MISTRAl_KEY)

# Function to communicate with Mistral API
def get_mistral_response(user_input):
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": "What is the best French cheese?",
            },
        ]
    )
    return chat_response.choices[0].message.content



print(get_mistral_response(""))