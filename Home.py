import streamlit as st

st.set_page_config(
    page_title="Nanopore Experiment",
    page_icon="🧪",
)

st.write("# Welcome to the Nanopore Telomere Laboration Notebook")

st.sidebar.success("Select what you want to do above.")

st.markdown( """
    # This Laboration notebook let you add information about the sequencing:
    ### Click on the "Add New Experiment tab above"
    - Adds new experiment to the database
    ### View Old Experiments
    - Look at old experiments
"""
)