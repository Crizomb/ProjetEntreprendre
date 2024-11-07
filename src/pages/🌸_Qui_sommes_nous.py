import streamlit as st

# Configuration de la page
# Configuration de la page
st.set_page_config(
    page_title="SakurAI Market - Qui sommes-nous",
    page_icon="🌸",
    layout="wide"  # Utiliser la largeur complète de l'écran
)

# Titre principal
st.title("En apprendre plus sur SakurAI Market")

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

# Texte descriptif
st.markdown("""
### Bienvenue chez SakurAI Market !

Nous sommes une **équipe innovante** composée de :
- 🛠️ **Deux ingénieurs de Télécom SudParis**
- 💻 **Deux ingénieurs de l'ENSIIE**
- 📈 **Un expert de l'IMT-BS**

Notre mission est de construire une **boîte à outils d'intelligence artificielle** spécialement conçue pour répondre aux besoins des entreprises modernes, en leur offrant des solutions intuitives et puissantes pour optimiser leurs processus.

#### Un projet au service de l'innovation
Avec SakurAI Market, nous développons des outils d'IA, comme un **module d'analyse de CV** avancé, permettant aux recruteurs de gagner du temps en identifiant rapidement les meilleurs talents grâce à une technologie de pointe.

> **Rejoignez-nous dans cette aventure passionnante et révolutionnaire, où chaque solution apporte une réelle valeur ajoutée aux entreprises.** 

Nous croyons fermement que notre projet apportera une transformation significative pour toutes les entreprises cherchant à exploiter le potentiel de l'IA. 🌟
""")


# Pied de page
st.markdown("<div class='footer'>SakurAI Market © 2024. Tous droits réservés.</div>", unsafe_allow_html=True)