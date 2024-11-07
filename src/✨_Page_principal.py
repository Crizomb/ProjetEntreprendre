import streamlit as st
import base64
from st_clickable_images import clickable_images

# Configuration de la page
st.set_page_config(
    page_title="SakurAI Market",
    page_icon="🌸",
    layout="wide"  # Utiliser la largeur complète de l'écran
)

# Fonction pour charger les images en base64
@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
        return base64.b64encode(data).decode()

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

# Titre principal et sous-titre
st.title("SakurAI Market", anchor="center")
st.write("SakurAI : L'intelligence artificielle, en toute simplicité.")
st.header("Nos solutions")

st.subheader("Solutions ressources humaines")

# Section de projets avec images cliquables
st.markdown("<div class='image-container'>", unsafe_allow_html=True)
clicked = clickable_images(
    [
        f"data:image/png;base64,{get_img_as_base64('analyse_cv.webp')}"
        # f"data:image/png;base64,{get_img_as_base64('helper_chat_bot.webp')}"
    ],
    titles=["Analyse de CV"],
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"margin": "25px", "height": "300px", "width": "300px", "border-radius": "10px"},
)
st.markdown("</div>", unsafe_allow_html=True)

# Redirection vers une autre page si une image est cliquée
pages_str = ["pages/📑_Analyse_de_CVs.py"]
if clicked != -1 and clicked < len(pages_str):
    st.switch_page(pages_str[clicked])

st.markdown("D'autres à venir... (Prédiction d'évolution de carrières automatisée) ")

st.subheader("Solutions marketing")
st.markdown("à venir... (Analyse de marché automatisé...)")

st.subheader("Solutions financière")
st.markdown("à venir... (Analyse et rédaction de factures automatisé...)")



# Pied de page
st.markdown("<div class='footer'>SakurAI Market © 2024. Tous droits réservés.</div>", unsafe_allow_html=True)
