"""
Plotly chart builders, themed to match the app's dark / emerald palette.
"""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

COLORS = {
    "bg": "#0b1220",
    "card": "#141f35",
    "grid": "#22304a",
    "text": "#e5e9f0",
    "text_muted": "#8b98b3",
    "accent": "#10b981",
    "indigo": "#6366f1",
    "danger": "#f87171",
    "warning": "#fbbf24",
}

CATEGORICAL_SEQUENCE = ["#10b981", "#6366f1", "#fbbf24", "#f87171", "#38bdf8", "#a78bfa"]


def _base_layout(fig: go.Figure, title: str | None = None, height: int = 360) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=15, color=COLORS["text"])) if title else None,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text_muted"], size=12),
        margin=dict(l=10, r=10, t=45 if title else 15, b=10),
        height=height,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(color=COLORS["text_muted"]),
        ),
        hoverlabel=dict(bgcolor=COLORS["card"], font_color=COLORS["text"], bordercolor=COLORS["grid"]),
    )
    fig.update_xaxes(gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"], color=COLORS["text_muted"])
    fig.update_yaxes(gridcolor=COLORS["grid"], zerolinecolor=COLORS["grid"], color=COLORS["text_muted"])
    return fig


def churn_by_category_bar(df: pd.DataFrame, category: str, title: str) -> go.Figure:
    grouped = (
        df.groupby(category, observed=True)["Exited"]
        .mean()
        .mul(100)
        .round(2)
        .reset_index(name="ChurnRate")
        .sort_values("ChurnRate", ascending=False)
    )
    fig = px.bar(
        grouped, x=category, y="ChurnRate", text="ChurnRate",
        color_discrete_sequence=[COLORS["accent"]],
    )
    fig.update_traces(
        texttemplate="%{text}%", textposition="outside",
        marker_line_width=0, hovertemplate=f"%{{x}}<br>Churn Rate: %{{y}}%<extra></extra>",
    )
    fig.update_yaxes(title="Churn Rate (%)")
    fig.update_xaxes(title=None)
    return _base_layout(fig, title)


def retention_donut(df: pd.DataFrame, title: str = "Retention Split") -> go.Figure:
    counts = df["ChurnStatus"].value_counts().reindex(["Retained", "Churned"]).fillna(0)
    fig = go.Figure(
        data=[
            go.Pie(
                labels=counts.index,
                values=counts.values,
                hole=0.62,
                marker=dict(colors=[COLORS["accent"], COLORS["danger"]], line=dict(color=COLORS["bg"], width=2)),
                textinfo="percent",
                textfont=dict(color=COLORS["text"], size=13),
                hovertemplate="%{label}: %{value:,} customers (%{percent})<extra></extra>",
            )
        ]
    )
    total = int(counts.sum())
    fig.add_annotation(
        text=f"<b>{total:,}</b><br><span style='font-size:11px;color=#8b98b3'>Customers</span>",
        showarrow=False, font=dict(size=18, color=COLORS["text"]),
    )
    return _base_layout(fig, title, height=320)


def age_distribution_hist(df: pd.DataFrame, title: str = "Age Distribution by Status") -> go.Figure:
    fig = px.histogram(
        df, x="Age", color="ChurnStatus", barmode="overlay", nbins=30,
        color_discrete_map={"Retained": COLORS["accent"], "Churned": COLORS["danger"]},
        opacity=0.75,
    )
    fig.update_yaxes(title="Customers")
    fig.update_xaxes(title="Age")
    return _base_layout(fig, title)


def balance_vs_score_scatter(df: pd.DataFrame, title: str = "Balance vs. Credit Score") -> go.Figure:
    sample = df.sample(n=min(2000, len(df)), random_state=42) if len(df) > 2000 else df
    fig = px.scatter(
        sample, x="CreditScore", y="Balance", color="ChurnStatus",
        color_discrete_map={"Retained": COLORS["accent"], "Churned": COLORS["danger"]},
        opacity=0.55, hover_data=["Age", "Geography", "NumOfProducts"],
    )
    fig.update_traces(marker=dict(size=6, line=dict(width=0)))
    fig.update_yaxes(title="Balance ($)")
    fig.update_xaxes(title="Credit Score")
    return _base_layout(fig, title, height=380)


def tenure_churn_line(df: pd.DataFrame, title: str = "Churn Rate by Tenure") -> go.Figure:
    grouped = (
        df.groupby("Tenure", observed=True)["Exited"]
        .mean().mul(100).round(2).reset_index(name="ChurnRate")
        .sort_values("Tenure")
    )
    fig = go.Figure(
        data=[
            go.Scatter(
                x=grouped["Tenure"], y=grouped["ChurnRate"],
                mode="lines+markers",
                line=dict(color=COLORS["indigo"], width=3, shape="spline"),
                marker=dict(size=7, color=COLORS["indigo"]),
                fill="tozeroy", fillcolor="rgba(99,102,241,0.12)",
                hovertemplate="Tenure: %{x} yrs<br>Churn Rate: %{y}%<extra></extra>",
            )
        ]
    )
    fig.update_yaxes(title="Churn Rate (%)")
    fig.update_xaxes(title="Tenure (Years)")
    return _base_layout(fig, title)


def product_tier_heatmap(df: pd.DataFrame, title: str = "Churn Rate: Geography x Product Tier") -> go.Figure:
    pivot = (
        df.groupby(["Geography", "ProductTier"], observed=True)["Exited"]
        .mean().mul(100).round(1).unstack()
    )
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values, x=pivot.columns.astype(str), y=pivot.index,
            colorscale=[[0, "#111a2b"], [0.5, "#059669"], [1, "#10b981"]],
            text=pivot.values, texttemplate="%{text}%",
            textfont=dict(color=COLORS["text"], size=11),
            hovertemplate="%{y} / %{x}<br>Churn Rate: %{z}%<extra></extra>",
            colorbar=dict(title="Churn %", tickfont=dict(color=COLORS["text_muted"])),
        )
    )
    return _base_layout(fig, title, height=340)
