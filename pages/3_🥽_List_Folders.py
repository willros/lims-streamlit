import pandas as pd
import streamlit as st
import numpy as np
import datetime
from pathlib import Path
import yaml

config_path = "/Users/wiro0005/clinical_genomics/lims-streamlit/config.yaml"
with open(config_path, "r") as f:
    config = yaml.full_load(f)

SEQUENCING_FOLDER = Path(config["SEQUENCING_FOLDER"])

SAMPLE_NAMES = [
    x
    for x in SEQUENCING_FOLDER.iterdir()
    if x.is_dir() and not x.stem.startswith(".")
]

st.markdown(SAMPLE_NAMES)
