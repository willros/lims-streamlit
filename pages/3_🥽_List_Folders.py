import pandas as pd
import streamlit as st
import datetime
from pathlib import Path
import yaml
from typing import Union
from pandas._libs.missing import NAType
import re

st.set_page_config(page_title="List Folders", page_icon="🥽")

config_path = "/Users/wiro0005/clinical_genomics/lims-streamlit/config.yaml"
with open(config_path, "r") as f:
    config = yaml.full_load(f)


def reports(folder: list[Path], pattern: str, as_path: bool = False) -> list[Path]:
    """
    :param folder list[Path]: List of sample directiories
    :param pattern str: Pattern to search for in folder structure
    :returns: List of Path objects
    """
    if as_path:
        return [
            y[0] if (y := list(x.rglob(f"{pattern}"))) else "Not generated"
            for x in folder
        ]
    return [
        f"file:///{str(y[0])}"
        if (y := list(x.rglob(f"{pattern}")))
        else "Not generated"
        for x in folder
    ]


def return_date(text: Union[Path | str]) -> Union[str | NAType]:
    if isinstance(text, Path):
        return str(
            datetime.datetime.strptime(
                re.findall(
                    r'<div class="run-details">\n\s*(\d* \w* \d*)', text.read_text()
                )[0],
                "%d %b %y",
            ).date()
        )
    return pd.NA


# Files and directories
SEQUENCING_FOLDER = Path(config["SEQUENCING_FOLDER"])
SAMPLE_FOLDERS = [
    x for x in SEQUENCING_FOLDER.iterdir() if x.is_dir() and not x.stem.startswith(".")
]
SAMPLE_NAMES = [x.stem for x in SAMPLE_FOLDERS]

# Reports
NANOPLOT_REPORTS = reports(SAMPLE_FOLDERS, "*NanoPlot*.html")
WF_ALIGNMENT_REPORTS = reports(SAMPLE_FOLDERS, "wf-alignment*.html")
SEQUENCE_REPORTS = reports(SAMPLE_FOLDERS, "*FAV*.html")

DATES = [return_date(x) for x in reports(SAMPLE_FOLDERS, "*FAV*.html", as_path=True)]

# Dataframe
df = pd.DataFrame(
    {
        "sample": SAMPLE_NAMES,
        "nanoplot": NANOPLOT_REPORTS,
        "wf_alignment": WF_ALIGNMENT_REPORTS,
        "sequencing": SEQUENCE_REPORTS,
        "date": DATES,
    }
)

st.markdown(df.to_html(render_links=True), unsafe_allow_html=True)
