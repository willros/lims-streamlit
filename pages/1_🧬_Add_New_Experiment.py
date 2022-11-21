import pandas as pd
import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Plotting Demo", page_icon="🧬")

st.markdown("# Add New Experiment")
st.sidebar.header("Add New Experiment")
st.write(
    """Add a new experiment to the database"""
)


# Buttons
name = st.text_input('Name', 'Lambda Control')

sample_type = st.text_input('Sample Type', 'Plasma from human')

kit = st.selectbox(
    'Kit', 
    ("Kit2", "Kit2", "Kit2"))

barcodes = st.selectbox(
    'Barcodes', 
    ("SQL100", "SQL200", "SQL300"))

adaptive_sampling = st.radio(
    'Adaptive sampling',
    ("Yes", "No"))


comment = st.text_input('Comment', 'Comment about the run')


# Create the new input
df = pd.DataFrame({"name": [name],
                   "sample_type": [sample_type],
                   "kit": [kit],
                    "barcodes": [barcodes],
                    "adaptive_sampling": [adaptive_sampling],
                    "comment": [comment],
                  })

st.dataframe(df)  # Same as st.write(df)
submit = st.button("Submit")

if submit:
    old = pd.read_csv("nanopore_experiments.csv")
    new = pd.concat([old, df], ignore_index=True)
    new.to_csv("nanopore_experiments.csv", index=False)
    st.markdown("# Saved The Experiment!")
        
