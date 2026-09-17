"""
Segments page: deeper cross-cuts of churn by demographic / product segment.
"""
from __future__ import annotations

import streamlit as st

from components.charts import balance_vs_score_scatter, product_tier_heatmap
from utils.metrics import segment_churn_table


def render(df_filtered) -> None:
    st.markdown("## Segment Analysis")
    st.caption("Identify which customer segments carry the highest retention risk.")
    st.divider()

    if df_filtered.empty:
        st.warning("No customers match the current filter selection. Adjust filters in the sidebar.")
        return

    tab1, tab2, tab3 = st.tabs(["Geography x Product", "Relationship Tiers", "Balance vs. Score"])

    with tab1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        with st.spinner("Building heatmap..."):
            st.plotly_chart(product_tier_heatmap(df_filtered), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        try:
            table = segment_churn_table(df_filtered, "RelationshipTier")
            table = table.rename(columns={
                "RelationshipTier": "Relationship Tier",
                "Customers": "Customers",
                "Churned": "Churned",
                "ChurnRate": "Churn Rate (%)",
            })
            st.dataframe(table, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"Unable to compute relationship tier breakdown: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        with st.spinner("Rendering scatter plot..."):
            st.plotly_chart(balance_vs_score_scatter(df_filtered), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.markdown("#### Segment Churn Summary")
    dimension = st.selectbox(
        "Group by",
        ["Geography", "Gender", "AgeBand", "BalanceBand", "ProductTier", "Engagement"],
    )
    try:
        summary = segment_churn_table(df_filtered, dimension)
        summary = summary.rename(columns={"ChurnRate": "Churn Rate (%)"})
        st.dataframe(summary, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"Could not build summary table: {e}")
