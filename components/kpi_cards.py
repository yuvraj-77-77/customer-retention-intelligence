"""
KPI metric card rendering helpers.
"""
from __future__ import annotations

import streamlit as st


def _delta_html(delta: float | None, suffix: str = "", invert: bool = False) -> str:
    if delta is None:
        return ""
    sign = "+" if delta > 0 else ""
    css_class = "neutral"
    if delta > 0:
        css_class = "negative" if invert else "positive"
    elif delta < 0:
        css_class = "positive" if invert else "negative"
    return f'<span class="metric-delta {css_class}">{sign}{delta}{suffix} vs. full dataset</span>'


def render_kpi_card(label: str, value: str, delta: float | None = None,
                     suffix: str = "", invert: bool = False) -> str:
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {_delta_html(delta, suffix, invert)}
    </div>
    """


def render_kpi_row(kpis: dict, deltas: dict | None = None) -> None:
    """Render the standard 5-column KPI row on Overview."""
    deltas = deltas or {}
    cols = st.columns(5)

    with cols[0]:
        st.markdown(
            render_kpi_card(
                "Total Customers",
                f"{kpis['total_customers']:,}",
            ),
            unsafe_allow_html=True,
        )
    with cols[1]:
        st.markdown(
            render_kpi_card(
                "Churn Rate",
                f"{kpis['churn_rate']}%",
                deltas.get("churn_rate"),
                suffix=" pts",
                invert=True,
            ),
            unsafe_allow_html=True,
        )
    with cols[2]:
        st.markdown(
            render_kpi_card(
                "Active Member Rate",
                f"{kpis['active_rate']}%",
                deltas.get("active_rate"),
                suffix=" pts",
            ),
            unsafe_allow_html=True,
        )
    with cols[3]:
        st.markdown(
            render_kpi_card(
                "Avg. Balance",
                f"${kpis['avg_balance']:,.0f}",
                deltas.get("avg_balance"),
                suffix="",
            ),
            unsafe_allow_html=True,
        )
    with cols[4]:
        st.markdown(
            render_kpi_card(
                "Avg. Relationship Score",
                f"{kpis['avg_relationship']}",
                deltas.get("avg_relationship"),
            ),
            unsafe_allow_html=True,
        )
