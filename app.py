"""
Customer Retention Analytics Pro
==================================
Enterprise-grade Streamlit application for analyzing customer churn
and retention across a banking customer base.

Run with:  streamlit run app.py
"""
from __future__ import annotations

from pathlib import Path

import streamlit as st

from components import page_data_health, page_explorer, page_overview, page_segments
from components.sidebar import render_sidebar
from utils.data import DataValidationError, apply_filters, load_dataset, load_dataset_from_upload

APP_DIR = Path(__file__).parent
DEFAULT_DATA_PATH = APP_DIR / "data" / "European_Bank.csv"
CSS_PATH = APP_DIR / "utils" / "style.css"


def inject_css() -> None:
    try:
        css = CSS_PATH.read_text()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Stylesheet not found; using default Streamlit styling.")


def get_dataframe():
    """Load either the uploaded dataset (if present in session) or the default sample."""
    if st.session_state.get("uploaded_file_bytes"):
        try:
            return load_dataset_from_upload(st.session_state["uploaded_file_bytes"])
        except DataValidationError as e:
            st.error(f"Uploaded file failed validation: {e}")
            st.info("Falling back to the default dataset.")
        except Exception as e:
            st.error("An unexpected error occurred while reading the uploaded file.")
            st.exception(e)

    try:
        return load_dataset(DEFAULT_DATA_PATH)
    except FileNotFoundError:
        st.error(
            f"Default dataset not found at `{DEFAULT_DATA_PATH}`. "
            "Please upload a CSV file from the sidebar to continue."
        )
        st.stop()
    except DataValidationError as e:
        st.error(f"The default dataset failed validation: {e}")
        st.stop()
    except Exception as e:
        st.error("An unexpected error occurred while loading the dataset.")
        st.exception(e)
        st.stop()


def main() -> None:
    st.set_page_config(
        page_title="Customer Retention Analytics Pro",
        page_icon="◆",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_css()

    with st.spinner("Loading customer dataset..."):
        df_full = get_dataframe()

    filters = render_sidebar(df_full)

    try:
        df_filtered = apply_filters(df_full, filters)
    except Exception as e:
        st.error("Unable to apply the selected filters. Showing the full dataset instead.")
        st.exception(e)
        df_filtered = df_full

    active_page = st.session_state.get("active_page", "Overview")

    if active_page == "Overview":
        page_overview.render(df_full, df_filtered)
    elif active_page == "Segments":
        page_segments.render(df_filtered)
    elif active_page == "Customer Explorer":
        page_explorer.render(df_filtered)
    elif active_page == "Data Health":
        page_data_health.render(df_full)
    else:
        st.error("Unknown page selected.")


if __name__ == "__main__":
    main()
