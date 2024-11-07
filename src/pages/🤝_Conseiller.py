import streamlit as st
import random
import os
import time
from dotenv import load_dotenv
from mistralai import Mistral

st.set_page_config(
    page_title="SakurAI Market - Conseiller virtuel",
    page_icon="🌸",
    layout="wide"  # Utiliser la largeur complète de l'écran
)


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


# Style CSS pour personnaliser l'arrière-plan et le style des éléments
st.markdown("""
    <style>
        .main { background-color: #f5f5f5; }  /* Couleur de fond principale */
        .header { color: #ff69b4; text-align: center; }  /* Couleur de l'en-tête */
        .subheader { color: #6a1b9a; font-size: 24px; text-align: center; } /* Sous-titre */
        .image-container { text-align: center; margin-top: 30px; }  /* Conteneur d'images */
        .footer { text-align: center; padding-top: 30px; font-size: 16px; color: #888; }

        div[data-testid="stSidebarHeader"] > img, div[data-testid="collapsedControl"] > img {
      height: 8rem;
      width: auto;
  }

  div[data-testid="stSidebarHeader"], div[data-testid="stSidebarHeader"] > *,
  div[data-testid="collapsedControl"], div[data-testid="collapsedControl"] > * {
      display: flex;
      align-items: center;
  }
    </style>
""", unsafe_allow_html=True)


# Logo SakurAI en haut de la page
st.logo("sakurai_proto.png", size="large")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "has_started" not in st.session_state:
    st.session_state.has_started = False

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
Je suis là pour vous guider vers l'outil qui répondra le mieux à vos besoins. Si vous chercher une assistance avec nos solutions ou des conseils pour optimiser vos processus, je suis à votre disposition pour vous aiguiller ! Comment puis-je vous aider aujourd’hui ?"""

# Display assistant response in chat message container
with st.chat_message("assistant"):
    if prompt:
        response = st.write_stream(response_generator(get_mistral_response(prompt)))
    elif not st.session_state.has_started:
        response = st.write_stream(response_generator(hello_msg))
        st.session_state.has_started = True
    else:
        response = ""


# Add assistant response to chat history
if response != "" : st.session_state.messages.append({"role": "assistant", "content": response})


# Pied de page
st.markdown("<div class='footer'>SakurAI Market © 2024. Tous droits réservés.</div>", unsafe_allow_html=True)