import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Earlier experiments", page_icon="📋")

st.sidebar.header("Earlier Experiments")

st.markdown("""
    # Earlier experiments 📋
    - Sort the table by clicking on the columns
""")

df = pd.read_csv("nanopore_experiments.csv")
# st.dataframe(df)
st.markdown(df.to_html(render_links=True), unsafe_allow_html=True)

