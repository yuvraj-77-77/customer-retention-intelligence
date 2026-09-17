"""
Overview page: headline KPIs and top-level retention visuals.
"""
from __future__ import annotations

import streamlit as st

from components.charts import (
    age_distribution_hist,
    churn_by_category_bar,
    retention_donut,
    tenure_churn_line,
)
from components.kpi_cards import render_kpi_row
from utils.metrics import compute_kpis, kpi_deltas


def render(df_full, df_filtered) -> None:
    st.markdown("## Executive Overview")
    st.caption("Real-time snapshot of customer retention health across the filtered segment.")
    st.divider()

    if df_filtered.empty:
        st.warning("No customers match the current filter selection. Adjust filters in the sidebar.")
        return

    with st.spinner("Computing KPIs..."):
        kpis_full = compute_kpis(df_full)
        kpis_filtered = compute_kpis(df_filtered)
        deltas = kpi_deltas(kpis_filtered, kpis_full)

    render_kpi_row(kpis_filtered, deltas)

    st.write("")
    col1, col2 = st.columns([1, 1.4])

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        with st.spinner("Rendering chart..."):
            st.plotly_chart(retention_donut(df_filtered), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        with st.spinner("Rendering chart..."):
            st.plotly_chart(
                tenure_churn_line(df_filtered), use_container_width=True
            )
        st.markdown("</div>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        with st.spinner("Rendering chart..."):
            st.plotly_chart(
                churn_by_category_bar(df_filtered, "Geography", "Churn Rate by Geography"),
                use_container_width=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        with st.spinner("Rendering chart..."):
            st.plotly_chart(
                age_distribution_hist(df_filtered), use_container_width=True
            )
        st.markdown("</div>", unsafe_allow_html=True)
