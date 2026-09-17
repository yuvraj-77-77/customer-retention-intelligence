"""
Data Health page: dataset diagnostics and quality summary.
"""
from __future__ import annotations

import pandas as pd
import streamlit as st


def render(df_full: pd.DataFrame) -> None:
    st.markdown("## Data Health")
    st.caption("Diagnostics on the currently loaded dataset.")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Rows</div>'
            f'<div class="metric-value">{len(df_full):,}</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Columns</div>'
            f'<div class="metric-value">{df_full.shape[1]}</div></div>',
            unsafe_allow_html=True,
        )
    with col3:
        dupes = int(df_full["CustomerId"].duplicated().sum())
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">Duplicate Customer IDs</div>'
            f'<div class="metric-value">{dupes}</div></div>',
            unsafe_allow_html=True,
        )

    st.write("")
    st.markdown("#### Column Overview")
    try:
        dtypes = df_full.dtypes.astype(str)
        nulls = df_full.isna().sum()
        overview = pd.DataFrame({
            "Column": dtypes.index,
            "Type": dtypes.values,
            "Null Count": nulls.values,
        })
        st.dataframe(overview, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Could not build column overview: {e}")

    st.write("")
    st.markdown("#### Descriptive Statistics")
    try:
        numeric_cols = df_full.select_dtypes(include="number").columns.tolist()
        st.dataframe(df_full[numeric_cols].describe().round(2), use_container_width=True)
    except Exception as e:
        st.error(f"Could not compute descriptive statistics: {e}")
