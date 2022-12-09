import pandas as pd
import streamlit as st
import numpy as np
import datetime

st.set_page_config(page_title="New Experiment", page_icon="🧬")

st.sidebar.header("Add New Experiment")
st.markdown(
    """
    # Add New Experiment 🧬
    - Add a new experiments to the database
"""
)


# Buttons
name = st.text_input("Name", "")

sample_type = st.text_input("Sample Type", "")

kit = st.selectbox("Kit", ("Kit2", "Kit2", "Kit2"))

barcodes = st.selectbox("Barcodes", ("SQL100", "SQL200", "SQL300"))

adaptive_sampling = st.radio("Adaptive sampling", ("Yes", "No"))

reference_genome = st.text_input("Reference Genome", "")

comment = st.text_input("Comment", "")

sample_concentration = st.number_input("sample concentration")

volume = st.number_input("volume loaded")

oligos_and_adapters = st.text_input("Oligos and Adapters used. Example: AAATTTGGCCC")

# Create the new input
df = pd.DataFrame(
    {
        "name": [name],
        "sample_type": [sample_type],
        "kit": [kit],
        "barcodes": [barcodes],
        "adaptive_sampling": [adaptive_sampling],
        "reference_genome": [reference_genome],
        "comment": [comment],
        "date": [str(datetime.datetime.now())],
        "sample_concentration": [sample_concentration],
        "volume": [volume],
        "oligos_and_adapters": [oligos_and_adapters],
    }
)
st.markdown(
    """
    ### Make sure that everthing is correct before submitting! 🧐
    """
)

st.dataframe(df)

# submit
submit = st.button("Submit")

if submit:
    old = pd.read_csv("nanopore_experiments.csv")
    new = pd.concat([old, df], ignore_index=True)
    new.to_csv("nanopore_experiments.csv", index=False)
    st.markdown("# Saved The Experiment!")
