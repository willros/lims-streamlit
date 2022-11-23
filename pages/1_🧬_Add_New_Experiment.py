import pandas as pd
import streamlit as st
import numpy as np
import datetime

st.set_page_config(page_title="New Experiment", page_icon="🧬")

st.sidebar.header("Add New Experiment")
st.markdown("""
    # Add New Experiment 🧬
    - Add a new experiments to the database
""")


# Buttons
name = st.text_input('Name', '')

sample_type = st.text_input('Sample Type', '')

kit = st.selectbox(
    'Kit', 
    ("Kit2", "Kit2", "Kit2"))

barcodes = st.selectbox(
    'Barcodes', 
    ("SQL100", "SQL200", "SQL300"))

adaptive_sampling = st.radio(
    'Adaptive sampling',
    ("Yes", "No"))

reference_genome = st.text_input('Reference Genome', '')

comment = st.text_input('Comment', '')
url = st.text_input('url', '')


# Create the new input
df = pd.DataFrame({"name": [name],
                   "sample_type": [sample_type],
                   "kit": [kit],
                    "barcodes": [barcodes],
                    "adaptive_sampling": [adaptive_sampling],
                    "reference_genome": [reference_genome],
                    "comment": [comment],
                    "date": [str(datetime.datetime.now())],
                    "url": [url],
                  })
st.dataframe(df)  

# submit
submit = st.button("Submit")

if submit:
    old = pd.read_csv("nanopore_experiments.csv")
    new = pd.concat([old, df], ignore_index=True)
    new.to_csv("nanopore_experiments.csv", index=False)
    st.markdown("# Saved The Experiment!")
        
