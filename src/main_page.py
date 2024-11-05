import streamlit as st

from st_clickable_images import clickable_images
from streamlit import title

st.set_page_config(
    page_title="SakurAI Market",
    page_icon="🌸"
)

clicked = clickable_images(
    [
        "https://images.unsplash.com/photo-1565130838609-c3a86655db61?w=700",
        "https://images.unsplash.com/photo-1565372195458-9de0b320ef04?w=700",
        "https://images.unsplash.com/photo-1582550945154-66ea8fff25e1?w=700",
        "https://images.unsplash.com/photo-1591797442444-039f23ddcc14?w=700",
        "https://images.unsplash.com/photo-1518727818782-ed5341dbd476?w=700",
    ],
    titles=[f"Image #{str(i*2)}" for i in range(5)],
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"margin": "5px", "height": "200px"},
    
    

)

st.markdown(f"Image #{clicked} clicked" if clicked > -1 else "No image clicked")

pages_str = ["pages/learn.py", "pages/cv_analysis.py", "pages/marketing_chatbot.py"]

if clicked != -1:
    print(clicked)
    st.switch_page(pages_str[clicked])