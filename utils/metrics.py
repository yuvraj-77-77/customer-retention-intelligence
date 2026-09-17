"""
KPI computation helpers for Customer Retention Analytics Pro.
"""
from __future__ import annotations

import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def compute_kpis(df: pd.DataFrame) -> dict:
    """Compute headline KPI figures for a (filtered) dataframe."""
    if df.empty:
        return {
            "total_customers": 0,
            "churn_rate": 0.0,
            "retained": 0,
            "churned": 0,
            "avg_balance": 0.0,
            "avg_credit_score": 0.0,
            "active_rate": 0.0,
            "avg_products": 0.0,
            "avg_relationship": 0.0,
        }

    total = len(df)
    churned = int(df["Exited"].sum())
    retained = total - churned

    return {
        "total_customers": total,
        "churn_rate": round(100 * churned / total, 2) if total else 0.0,
        "retained": retained,
        "churned": churned,
        "avg_balance": round(df["Balance"].mean(), 2),
        "avg_credit_score": round(df["CreditScore"].mean(), 1),
        "active_rate": round(100 * df["IsActiveMember"].mean(), 2),
        "avg_products": round(df["NumOfProducts"].mean(), 2),
        "avg_relationship": round(df["RelationshipStrength"].mean(), 1),
    }


def kpi_deltas(current: dict, baseline: dict) -> dict:
    """Compute simple deltas between a filtered KPI set and the unfiltered baseline."""
    deltas = {}
    for key in current:
        if isinstance(current[key], (int, float)) and isinstance(baseline.get(key), (int, float)):
            deltas[key] = round(current[key] - baseline[key], 2)
        else:
            deltas[key] = None
    return deltas


@st.cache_data(show_spinner=False)
def segment_churn_table(df: pd.DataFrame, by: str) -> pd.DataFrame:
    """Return churn rate and volume grouped by a categorical column."""
    if df.empty:
        return pd.DataFrame(columns=[by, "Customers", "Churned", "ChurnRate"])

    grouped = (
        df.groupby(by, observed=True)
        .agg(Customers=("CustomerId", "count"), Churned=("Exited", "sum"))
        .reset_index()
    )
    grouped["ChurnRate"] = (100 * grouped["Churned"] / grouped["Customers"]).round(2)
    return grouped.sort_values("ChurnRate", ascending=False)
