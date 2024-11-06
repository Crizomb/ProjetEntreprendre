import pypdf
from streamlit_pdf_viewer import pdf_viewer
import streamlit as st
from pypdf import PdfReader
import time
from dotenv import load_dotenv
from mistralai import Mistral
import pandas as pd
from io import BytesIO
import re
import os


# check https://pypi.org/project/python-dotenv/ to add MISTRAl_KEY to a .env
load_dotenv()

pre_prompt = """
Tu es un responsable RH expérimenté. Analyse ce CV en termes de forces et de faiblesses par rapport aux critères du poste à pourvoir. Détaille les points forts et les domaines d'amélioration. 
À la fin de ton analyse, donne un score global sur 50 en suivant STRICTEMENT ce format : "Score : x/50". 
Le score doit être la dernière information affichée et rien ne doit apparaître après ce score. 
Voici la description du poste demandé : 
"""

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

st.title("Analyse de CV")
files = st.file_uploader("Publier un pdf du CV", type=["pdf"], accept_multiple_files=True)

requested_job = st.text_input("Entrer le poste demandé")

responses_and_score = []

if requested_job and files:
    for file in files:
        # Read the PDF file
        pdf_reader = pypdf.PdfReader(file)
        # Extract the content
        content = ""
        for page in range(pdf_reader.get_num_pages()):
            content += pdf_reader.get_page(page).extract_text() + "\n"

        response = get_mistral_response(pre_prompt + requested_job, content)
        score = re.search(r"Score\s*:\s*(\d{1,2})/50", response).group(1)
        responses_and_score.append((score, content, response, file))

    # Sort the results by score
    responses_and_score.sort(key=lambda x: int(x[0]), reverse=True)

    # Display the results
    st.subheader("Résultats de l'analyse des CV")

    # Create a DataFrame to export later
    data = []

    for idx, (score, content, response, file) in enumerate(responses_and_score):
        st.markdown(f"### CV #{idx + 1}")

        # Display CV score with color indication
        score_int = int(score)
        if score_int >= 40:
            score_color = "green"
        elif score_int >= 30:
            score_color = "yellow"
        else:
            score_color = "red"

        st.markdown(f"<p style='color:{score_color}; font-size:20px;'>Score: {score}/50</p>", unsafe_allow_html=True)

        # Display a snippet of the CV content
        #st.text_area("Extrait du CV", content, height=150, key=idx)
        pdf_viewer(file.read())

        # Display the analysis response (perhaps summarised)
        st.text_area("Analyse du CV", response, height=150, key=f"response_{idx}")

        # Add the data to the export list
        data.append({
            "CV #": idx + 1,
            "Score": score,
            "Content": content[:300],  # Showing just a snippet
            "Analysis": response[:300]  # Showing just a snippet
        })

    # Create a DataFrame for export
    df = pd.DataFrame(data)

    # Create an Excel file in memory using BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Résultats")
    output.seek(0)

    # Button to download the results as Excel
    st.download_button(
        label="Télécharger les résultats (Excel)",
        data=output,
        file_name="cv_analysis_results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# Pied de page
st.markdown("<div class='footer'>SakurAI Market © 2024. Tous droits réservés.</div>", unsafe_allow_html=True)