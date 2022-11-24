import pandas as pd
import streamlit as st
import datetime
from pathlib import Path
import yaml

config_path = "/Users/wiro0005/clinical_genomics/lims-streamlit/config.yaml"
with open(config_path, "r") as f:
    config = yaml.full_load(f)


def reports(folder: list[Path], pattern: str) -> list[Path]:
    """
    :param folder list[Path]: List of sample directiories
    :param pattern str: Pattern to search for in folder structure
    :returns: List of Path objects
    """
    return [
       f"file:///{str(y[0])}" if (y := list(x.rglob(f"{pattern}"))) else "Not generated" for x in folder
    ]

# Files and directories
SEQUENCING_FOLDER = Path(config["SEQUENCING_FOLDER"])
SAMPLE_FOLDERS = [
    x for x in SEQUENCING_FOLDER.iterdir() if x.is_dir() and not x.stem.startswith(".")
]
SAMPLE_NAMES = [x.stem for x in SAMPLE_FOLDERS]

# Reports
NANOPLOT_REPORTS = reports(SAMPLE_FOLDERS, "*NanoPlot*.html")
WF_ALIGNMENT_REPORTS = reports(SAMPLE_FOLDERS, "wf-alignment*.html")
SEQUENCE_REPORTS = reports(SAMPLE_FOLDERS, "*fav*.html")

# Dataframe
df = pd.DataFrame(
    {
        "sample": SAMPLE_NAMES,
        "nanoplot": NANOPLOT_REPORTS,
         "wf_alignment": WF_ALIGNMENT_REPORTS,
         "sequencing": SEQUENCE_REPORTS
    }
)

st.markdown(df.to_html(render_links=True), unsafe_allow_html=True)
