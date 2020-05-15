import streamlit as st
import spacy
from spacy import displacy
import pandas as pd
from spacy.pipeline import EntityRuler
from spacy.matcher import PhraseMatcher
from spacy.tokens import Span
import base64

SPACY_MODEL_NAMES = ["soft_skills"]
#SPACY_MODEL_NAMES = ["ergonomy_spacy_model"]
DEFAULT_TEXT = "The ability to cope with changes is a soft skill. Another soft skill is the empathy. There are some others like: critical thinking, problem solving, communication and assertiveness."
HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; 
                margin-bottom: 2.5rem">{}</div>"""



@st.cache(allow_output_mutation=True)
def load_model():
    
    nlp = spacy.load('soft_skill_rule')
#    nlp = spacy.load("en_core_web_sm", disable=['ner'])
    return nlp



@st.cache()
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
#model_load_state = st.info(f"Loading model '{spacy_model}'...")
#nlp = load_model(spacy_model)
#model_load_state.empty()
#nlp.to_disk("./jobtitles")

nlp = load_model()
matcher = PhraseMatcher(nlp.vocab)

with open('terms.txt', 'r') as f:
    terms = f.readlines()
    terms = [t.replace('\n','') for t in terms if t != '\n']

def add_phraseMatcher_ent(matcher, doc, i, matches):
    # Get the current match and create tuple of entity label, start and end.
    # Append entity to the doc's entity. (Don't overwrite doc.ents!)
    match_id, start, end = matches[i]
    entity = Span(doc, start, end, label = "SOFT SKILL")
    try: 
        doc.ents += (entity,)
    except Exception:
        pass

patterns = [nlp.make_doc(text) for text in terms]
matcher.add("TerminologyList", add_phraseMatcher_ent, *patterns)

# Page Title
st.title("Try the SkillNER")

# Text_Area
text = st.text_area("Please, paste your text below!", DEFAULT_TEXT)



# Code
st.subheader("Soft Skills")
doc = nlp(text)
matcher(doc)
#matcher(doc)
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
