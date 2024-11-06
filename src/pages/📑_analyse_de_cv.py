import pypdf
import streamlit as st
from pypdf import PdfReader
import time
from dotenv import load_dotenv
from mistralai import Mistral
import os


# check https://pypi.org/project/python-dotenv/ to add MISTRAl_KEY to a .env
load_dotenv()

pre_prompt = "Tu es un RH compétent, analyse les forces et les faiblesses de ce CV, et donne lui un score, voici le poste demandé : "

MISTRAl_KEY = os.getenv("MISTRAL_KEY")
model = "mistral-small-latest"
client = Mistral(api_key=MISTRAl_KEY)

def get_mistral_response(user_input, system_prompt = ""):
    print("Getting mistral response")
    if not user_input:
        return ""
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": f"Voici le CV \n{user_input}",
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


st.title("Analyse de CV")
file = st.file_uploader("Publier un pdf du CV", type=["pdf"])

requested_job = st.text_input("Entrer le poste demandé")

if requested_job and file is not None:
    # Read the PDF file
    pdf_reader = pypdf.PdfReader(file)
    # Extract the content
    content = ""
    for page in range(pdf_reader.get_num_pages()):
        content += pdf_reader.get_page(page).extract_text() + "\n"
    # Display the content
    # st.write(content)

    response = get_mistral_response(pre_prompt + requested_job, content)
    st.write(response)



# Pied de page
st.markdown("<div class='footer'>SakurAI Market © 2024. Tous droits réservés.</div>", unsafe_allow_html=True)


