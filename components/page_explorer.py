"""
Customer Explorer page: searchable, sortable record-level table with export.
"""
from __future__ import annotations

import streamlit as st

from utils.data import to_csv_bytes


def render(df_filtered) -> None:
    st.markdown("## Customer Explorer")
    st.caption("Search, inspect, and export individual customer records.")
    st.divider()

    if df_filtered.empty:
        st.warning("No customers match the current filter selection. Adjust filters in the sidebar.")
        return

    col_search, col_status = st.columns([2, 1])
    with col_search:
        query = st.text_input("Search by Customer ID or Surname", placeholder="e.g. 15634602 or Hargrave")
    with col_status:
        status_filter = st.selectbox("Status", ["All", "Retained", "Churned"])

    result = df_filtered
    if query:
        q = query.strip().lower()
        result = result[
            result["Surname"].str.lower().str.contains(q, na=False)
            | result["CustomerId"].astype(str).str.contains(q, na=False)
        ]
    if status_filter != "All":
        result = result[result["ChurnStatus"] == status_filter]

    st.markdown(f'<span class="tag">{len(result):,} records</span>', unsafe_allow_html=True)
    st.write("")

    display_cols = [
        "CustomerId", "Surname", "Geography", "Gender", "Age", "Tenure",
        "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember",
        "EstimatedSalary", "RelationshipStrength", "RelationshipTier", "ChurnStatus",
    ]

    try:
        st.dataframe(
            result[display_cols].sort_values("RelationshipStrength", ascending=False),
            use_container_width=True,
            hide_index=True,
            height=460,
            column_config={
                "Balance": st.column_config.NumberColumn(format="$%.2f"),
                "EstimatedSalary": st.column_config.NumberColumn(format="$%.2f"),
                "RelationshipStrength": st.column_config.ProgressColumn(
                    "Relationship Score", min_value=0, max_value=100, format="%.1f"
                ),
            },
        )
    except Exception as e:
        st.error("Unable to render the customer table. Please check the dataset formatting.")
        st.exception(e)
        return

    st.write("")
    try:
        csv_bytes = to_csv_bytes(result[display_cols])
        st.download_button(
            "Download filtered results (CSV)",
            data=csv_bytes,
            file_name="customer_export.csv",
            mime="text/csv",
        )
    except Exception:
        st.warning("Export is temporarily unavailable.")
