import streamlit as st

st.set_page_config(
    page_title="Nanopore Experiment",
    page_icon="🧪",
)

st.sidebar.success("Select what you want to do above.")

st.markdown(
    """
    # Nanopore Sequencing 🧪
    
    ### Click on the "Add New Experiment tab above" 🧬
    - Adds new experiment to the database
    
    ### View Old Experiments 📋
    - Look at old experiments
"""
)
