import streamlit as st
import spacy
from spacy import displacy
import pandas as pd
from spacy.pipeline import EntityRuler
from spacy.matcher import PhraseMatcher
import base64

SPACY_MODEL_NAMES = ["soft_skills"]
#SPACY_MODEL_NAMES = ["ergonomy_spacy_model"]
DEFAULT_TEXT = "Ability to cope with changes"
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; 
                margin-bottom: 2.5rem">{}</div>"""

@st.cache()
def load_model(name):
    return spacy.load(name)

@st.cache(ignore_hash=True)
def process_text(model_name, text):
    nlp = load_model(model_name)
    return nlp(text)

# Sidebar Title
from PIL import Image
img= Image.open("logo.png")
st.sidebar.image(img, width=300)

# Description
st.sidebar.markdown(
"""This interactive web application is a demo of the SkillNER.
It uses spaCy's built-in [displaCy](http://spacy.io/usage/visualizers) visualizer under the hood.
"""
)
st.sidebar.title("")

# Spacy
spacy_model = "soft_skills"
model_load_state = st.info(f"Loading model '{spacy_model}'...")
nlp = load_model(spacy_model)
model_load_state.empty()
#nlp.to_disk("./jobtitles")

# Page Title
st.title("Try the SkillNER")

# Text_Area
text = st.text_area("Please, paste your text below!", DEFAULT_TEXT)



# Code
st.subheader("Soft Skills")
doc = nlp(text)
html = displacy.render(doc, style="ent")

    # Newlines seem to mess with the rendering
html = html.replace("\n", " ")
st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)

    # Download csv file

st.sidebar.subheader("Soft Skills List")
dataframe = pd.read_excel('softSkillsLexicon.xlsx')

csv = dataframe.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
href = f'<a href="data:file/csv;base64,{b64}" download="prova.csv">Download CSV File</a>'
st.sidebar.markdown(href, unsafe_allow_html=True)
