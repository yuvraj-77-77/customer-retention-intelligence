"""
Sidebar navigation and global filters.
"""
from __future__ import annotations

import pandas as pd
import streamlit as st


NAV_PAGES = ["Overview", "Segments", "Customer Explorer", "Data Health"]


def render_sidebar(df: pd.DataFrame) -> dict:
    """Render the sidebar (branding, nav, filters). Returns the active filter dict."""
    with st.sidebar:
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:0.25rem;">
                <div style="width:34px;height:34px;border-radius:9px;
                            background:linear-gradient(135deg,#10b981,#059669);
                            display:flex;align-items:center;justify-content:center;
                            font-weight:800;color:#05140f;font-size:1.1rem;">R</div>
                <div>
                    <div class="app-title">Retention Pro</div>
                    <div class="app-subtitle">Customer Analytics Suite</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()

        if "active_page" not in st.session_state:
            st.session_state.active_page = NAV_PAGES[0]

        st.session_state.active_page = st.radio(
            "Navigate",
            NAV_PAGES,
            index=NAV_PAGES.index(st.session_state.active_page),
            label_visibility="collapsed",
        )

        st.divider()
        st.markdown("**Filters**")

        if "filters" not in st.session_state:
            from utils.data import default_filters
            st.session_state.filters = default_filters(df)

        geographies = sorted(df["Geography"].unique().tolist())
        genders = sorted(df["Gender"].unique().tolist())
        engagement_opts = sorted(df["Engagement"].unique().tolist())

        geo_sel = st.multiselect(
            "Geography", geographies,
            default=st.session_state.filters.get("geographies", geographies),
        )
        gender_sel = st.multiselect(
            "Gender", genders,
            default=st.session_state.filters.get("genders", genders),
        )
        engagement_sel = st.multiselect(
            "Engagement Status", engagement_opts,
            default=st.session_state.filters.get("engagement", engagement_opts),
        )

        min_p, max_p = int(df["NumOfProducts"].min()), int(df["NumOfProducts"].max())
        product_range = st.slider(
            "Number of Products", min_p, max_p,
            value=st.session_state.filters.get("product_range", (min_p, max_p)),
        )

        min_a, max_a = int(df["Age"].min()), int(df["Age"].max())
        age_range = st.slider(
            "Customer Age", min_a, max_a,
            value=st.session_state.filters.get("age_range", (min_a, max_a)),
        )

        col_a, col_b = st.columns(2)
        with col_a:
            reset = st.button("Reset", use_container_width=True, type="secondary")
        with col_b:
            apply_clicked = st.button("Apply", use_container_width=True, type="primary")

        if reset:
            from utils.data import default_filters
            st.session_state.filters = default_filters(df)
            st.rerun()

        if apply_clicked or "filters" not in st.session_state:
            st.session_state.filters = {
                "geographies": geo_sel or geographies,
                "genders": gender_sel or genders,
                "engagement": engagement_sel or engagement_opts,
                "product_range": product_range,
                "age_range": age_range,
            }

        st.divider()
        st.caption("Data Source")
        uploaded = st.file_uploader("Replace dataset (CSV)", type=["csv"], label_visibility="collapsed")
        if uploaded is not None:
            st.session_state.uploaded_file_bytes = uploaded.getvalue()
            st.session_state.uploaded_file_name = uploaded.name

        st.divider()
        st.caption("© 2026 Retention Pro • Internal Analytics")

    return st.session_state.filters
