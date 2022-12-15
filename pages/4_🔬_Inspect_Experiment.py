from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import yaml
import altair as alt
import base64
from dataclasses import dataclass, field

# configs
st.set_page_config(page_title="Inspect Experiments", page_icon="🔬")
st.sidebar.header("Inspect Experiments")

config_path = "/Users/wiro0005/clinical_genomics/lims-streamlit/config.yaml"
with open(config_path, "r") as f:
    config = yaml.full_load(f)

# Functions and classes
@dataclass
class Files:
    polyA: str
    polyT: str
    raw_read_info: pd.DataFrame
    num_raw_reads: int
    telo_tag: pd.DataFrame
    num_telo_tag: int
    alignment_report: str
    telomere_df: pd.DataFrame


def find_files(sample: str) -> Files:
    """
    Finds all relevant files for the sample in question
    """
    whole_path = Path(config["SAMPLES"]) / sample

    # alignment report
    alignment_report = str(list(whole_path.rglob("raw_report/*raw*.html"))[0])
    alignment_report = f"file:///{alignment_report}"

    # pdfs
    try:
        polyA_plot = list(whole_path.rglob("*polyA-plot.pdf"))[0]
        polyT_plot = list(whole_path.rglob("*polyT-plot.pdf"))[0]
    except:
        polyA_plot = ""
        polyT_plot = ""

    # read info
    raw_read_info = pd.read_csv(
        list(whole_path.rglob("read_statistics/*raw.tsv"))[0], sep="\t"
    )
    num_raw_reads = raw_read_info.num_seqs.squeeze()

    # telotag
    telo_tag = pd.read_csv(
        list(whole_path.rglob("read_statistics/*telotag.tsv"))[0], sep="\t"
    )
    num_telo_tag = telo_tag.num_seqs.squeeze()

    
    # telomere df
    chr_lengths = pd.read_csv("chm13v2_chr_lengths.csv")
    telomere_df = (
        pd.read_csv(
            list(whole_path.rglob("results/*results.csv"))[0],
        )
        .assign(read_length=lambda x: x.align_end - x.align_start)
        .rename(columns={"region_length": "telomere_length"})
        .merge(chr_lengths, on="chr")
        .rename(columns={"total_length": "chr_length"})
        .assign(
            arm=lambda x: np.select(
                [x.align_start < 100_000, x.align_start > x.chr_length - 100_000],
                ["left", "right"],
                default=pd.NA,
            )
        )
        .dropna()
        .reset_index()
    )

    # tail_info = pd.read_csv(
    #    list(whole_path.rglob("read_statistics/*tails.csv"))[0],
    # )

    files = Files(
        polyA=polyA_plot,
        polyT=polyT_plot,
        raw_read_info=raw_read_info,
        num_raw_reads=num_raw_reads,
        telo_tag=telo_tag,
        num_telo_tag=num_telo_tag,
        alignment_report=alignment_report,
        telomere_df=telomere_df,
    )
    return files


def display_pdf(pdf: str) -> None:
    """
    Function for displaying pdf
    """
    with open(pdf, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


st.markdown(
    """
    # Inspect Experiments 🔬
    ## Choose the sample you want to inspect closer below
"""
)


def plot_telomeres(telomere_df: pd.DataFrame) -> None:
    """
    Plots information about found telomeres
    """
    plot = (
        alt.Chart(telomere_df)
        .mark_boxplot()
        .encode(
            alt.X("chr:N", title="Chromosome"),
            alt.Color("arm:N"),
            alt.Y("telomere_length", title="Length of Telomere"),
        )
        .properties(
            title=f"Number of telomeric reads: {telomere_df.shape[0]}",
            height=700,
        )
        .facet(column="arm")
    )
    return plot


# choose samples
SAMPLES = [
    x.stem
    for x in Path(config["SAMPLES"]).iterdir()
    if x.is_dir() and not x.stem.startswith(".")
]

sample = st.selectbox(
    "Choose sample",
    SAMPLES,
)

sample_files = find_files(sample)

# present data
st.markdown(
    f"""
    # 🌟🌟🌟
    # Alignment Report
    ### [Alignment Report]({sample_files.alignment_report})
    """,
)

# read statistics
st.markdown(
    f"""
    ----
    # Read statistics:
    ### Number of raw reads:
    #### {sample_files.num_raw_reads:,}
    
    ### Number of reads with TeloTag:
    #### {sample_files.num_telo_tag:,}
    """
)

# polyA and polyT
if sample_files.polyT:
    st.markdown(
        """
        ----
        # PolyA and PolyT plots
        """
    )

    # polyT and polyA plots
    display_pdf(sample_files.polyT)
    display_pdf(sample_files.polyA)

# telomere information
st.markdown(
    f"""
    ----
    # Information about Telomeres
    #### Left reads:
    Reads that are aligned between 0 and 100,000 of the chromosome
    #### Right reads: 
    Reads that are aligned between chromosome end - 100,000 and end of the chromosome
    """
)
telomere_plot = plot_telomeres(sample_files.telomere_df)
st.altair_chart(telomere_plot)

st.markdown(
    """
    ### Table with telomere information
    """
)
st.dataframe(sample_files.telomere_df.style.format(thousands=","))
