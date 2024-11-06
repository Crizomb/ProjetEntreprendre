import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="SakurAI Market - En apprendre plus",
    page_icon="🚀",
    layout="centered"
)

# Titre principal
st.title("En apprendre plus sur SakurAI Market")

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