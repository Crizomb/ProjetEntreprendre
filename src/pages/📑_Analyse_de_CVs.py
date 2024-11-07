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

st.set_page_config(
    page_title="SakurAI Market - Conseiller virtuel",
    page_icon="🌸",
    layout="wide"  # Utiliser la largeur complète de l'écran
)

# check https://pypi.org/project/python-dotenv/ to add MISTRAl_KEY to a .env
load_dotenv()

def generate_pre_prompt(criteria):
    pre_prompt = f"""
    Tu es un responsable RH expérimenté. Analyse ce CV en fonction des sections suivantes pour évaluer les forces et faiblesses du candidat par rapport aux exigences du poste. Pour chaque section, attribue un score partiel sur 10, puis justifie cette note en citant des éléments précis du CV. 
    
    **Sections d’évaluation :**
    {criteria}
    
    Après avoir évalué chaque section, additionne les scores partiels pour un score global précis sur 50, en privilégiant des notes non arrondies à 5 (ex : 43/50, 28/50) pour plus de finesse.
    
    **Format de réponse :**
    1. La première ligne doit contenir STRICTEMENT le nom et prénom de la personne, sans autre information.
    2. Les forces et faiblesses doivent être listées par section d’évaluation, chaque section étant notée sur 10 avec une brève justification.
    3. Le score global doit apparaître en dernière ligne, strictement au format "Score : x/50" sans aucun texte supplémentaire.
    
    Voici la description du poste demandé : 
    """

    return pre_prompt

MISTRAl_KEY = os.getenv("MISTRAL_KEY")
#model = "ministral-3b-latest"
model = "mistral-small-latest"
client = Mistral(api_key=MISTRAl_KEY)

@st.cache_data
def get_mistral_response(user_input, system_prompt = ""):
    chat_response = client.chat.complete(
        model=model,
        random_seed = 0,
        temperature = 0.4,
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
files = st.file_uploader("Publier des pdfs de CV", type=["pdf"], accept_multiple_files=True)
requested_job = st.text_input("Entrer le poste demandé")
evaluated_criteria = st.text_area("Entrer les critères évalués :", """1. Compétences techniques (maîtrise des outils, logiciels, ou technologies requis pour le poste). 
2. Expérience professionnelle (pertinence et durée des expériences précédentes en lien avec le poste). 
3. Éducation et certifications (niveau et pertinence des diplômes et formations suivies). 
4. Compétences interpersonnelles (communication, leadership, collaboration, etc.). 
5. Adaptabilité au poste (capacité à s'adapter aux responsabilités et à la culture de l’entreprise).""")


responses_and_score = []

if requested_job and files:
    my_bar = st.progress(0, text="Analyse des CVs en cours...")
    for count, file in enumerate(files):
        my_bar.progress(count/len(files), text="Analyse des CVs en cours...")
        # Read the PDF file
        pdf_reader = pypdf.PdfReader(file)
        # Extract the content
        content = ""
        for page in range(pdf_reader.get_num_pages()):
            content += pdf_reader.get_page(page).extract_text() + "\n"

        response = get_mistral_response(generate_pre_prompt(evaluated_criteria) + requested_job, content)
        try:
            score = re.search(r"(\d{1,2})/50", response).group(1)
        except:
            score = -1
        name = response.split("\n")[0].replace("*","").replace("#", "").replace("_","")
        responses_and_score.append((score, content, response, file, name))

    # Sort the results by score
    responses_and_score.sort(key=lambda x: int(x[0]), reverse=True)

    # Display the results
    st.subheader("Résultats de l'analyse des CV")

    # Create a DataFrame to export later
    data = []

    my_bar.progress(1.0, text="Analyse des CVs en cours...")

    for idx, (score, content, response, file, name) in enumerate(responses_and_score):

        st.markdown(f"### CV #{idx + 1}")

        # Display CV score with color indication
        score_int = int(score)
        if score_int >= 40:
            score_color = "#00bd39"
        elif score_int >= 30:
            score_color = "#bdba00"
        else:
            score_color = "#9e0000"

        st.markdown(f"<p style='color:{score_color}; font-size:20px;'>Score: {score}/50</p>", unsafe_allow_html=True)

        # Display a snippet of the CV content
        #st.text_area("Extrait du CV", content, height=150, key=idx)
        pdf_viewer(input=file.getvalue())

        with st.expander(f"### Détails de l'analyse ###"):
            # Display the analysis response (perhaps summarised)
            st.markdown(response)

        # Add the data to the export list
        data.append({
            "Nom": name,
            "Score": score,
            "Contenu": content,
            "Analyse": response
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