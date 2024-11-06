import streamlit as st
import random
import os
import time
from dotenv import load_dotenv
from mistralai import Mistral



# check https://pypi.org/project/python-dotenv/ to add MISTRAl_KEY to a .env
load_dotenv()



MISTRAl_KEY = os.getenv("MISTRAL_KEY")
model = "mistral-small-latest"
client = Mistral(api_key=MISTRAl_KEY)

def get_mistral_response(user_input):
    print("Getting mistral response")
    if not user_input:
        return ""
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"{user_input}",
            },
        ]
    )
    return chat_response.choices[0].message.content

# Streamed response emulator
def response_generator(response):
    if not response:
        return "Hi how can, I help you ?"

    for word in f"Assistant : {response}".split(" "):
        yield word + " "
        time.sleep(0.05)

st.title("Helper ChatBot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input():
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

hello_msg = """Bonjour et bienvenue sur SakurAI Market ! 🌸
Je suis là pour vous guider vers l'outil qui répondra le mieux à vos besoins. Que vous cherchiez une analyse de CV, une assistance avec nos solutions ou des conseils pour optimiser vos processus, je suis à votre disposition pour vous aiguiller ! Comment puis-je vous aider aujourd’hui ?"""

# Display assistant response in chat message container
with st.chat_message("assistant"):
    if prompt:
        response = st.write_stream(response_generator(get_mistral_response(prompt)))
    else:
        response = st.write_stream(response_generator(hello_msg))
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})


# Pied de page
st.markdown("<div class='footer'>SakurAI Market © 2024. Tous droits réservés.</div>", unsafe_allow_html=True)