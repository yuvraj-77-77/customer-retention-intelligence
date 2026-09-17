"""
Data loading, validation, and enrichment utilities for
Customer Retention Analytics Pro.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

REQUIRED_COLUMNS = [
    "CustomerId",
    "Surname",
    "CreditScore",
    "Geography",
    "Gender",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary",
    "Exited",
]

INTEGER_COLUMNS = [
    "CustomerId",
    "CreditScore",
    "Age",
    "Tenure",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "Exited",
]

NUMERIC_COLUMNS = ["Balance", "EstimatedSalary"]


class DataValidationError(Exception):
    """Raised when the uploaded / source dataset fails validation."""


@st.cache_data(show_spinner=False)
def load_dataset(path: str | Path) -> pd.DataFrame:
    """Load, validate, and enrich the customer dataset. Cached for performance."""
    df = pd.read_csv(path)
    return _validate_and_enrich(df)


@st.cache_data(show_spinner=False)
def load_dataset_from_upload(file_bytes: bytes) -> pd.DataFrame:
    """Load a dataset from an uploaded file's raw bytes (cached by content)."""
    import io

    df = pd.read_csv(io.BytesIO(file_bytes))
    return _validate_and_enrich(df)


def _validate_and_enrich(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise DataValidationError(
            f"Dataset is missing required columns: {', '.join(missing)}"
        )

    df = df.copy()

    for col in INTEGER_COLUMNS + NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    if df[REQUIRED_COLUMNS].isna().any().any():
        bad = df[REQUIRED_COLUMNS].isna().sum()
        bad = bad[bad > 0].to_dict()
        raise DataValidationError(
            f"Dataset contains missing or non-numeric values in: {bad}"
        )

    for col in ["CustomerId", "CreditScore", "Age", "Tenure", "NumOfProducts",
                "HasCrCard", "IsActiveMember", "Exited"]:
        df[col] = df[col].astype(int)

    invalid_binary = (
        ~df["Exited"].isin([0, 1])
        | ~df["HasCrCard"].isin([0, 1])
        | ~df["IsActiveMember"].isin([0, 1])
    )
    if invalid_binary.any():
        raise DataValidationError(
            "Binary fields (Exited, HasCrCard, IsActiveMember) must contain only 0/1."
        )

    # --- Derived / enrichment fields -------------------------------------------------
    df["Engagement"] = np.where(
        df["IsActiveMember"].eq(1), "Active", "Inactive"
    )

    df["ProductTier"] = pd.cut(
        df["NumOfProducts"],
        bins=[0, 1, 2, np.inf],
        labels=["Single Product", "Two Products", "3+ Products"],
        include_lowest=True,
    )

    df["BalanceBand"] = pd.cut(
        df["Balance"],
        bins=[-1, 0, 50_000, 100_000, 150_000, np.inf],
        labels=["Zero", "< $50K", "$50K-$100K", "$100K-$150K", "$150K+"],
    )

    df["AgeBand"] = pd.cut(
        df["Age"],
        bins=[17, 30, 40, 50, 60, np.inf],
        labels=["18-30", "31-40", "41-50", "51-60", "61+"],
    )

    # Transparent, rules-based relationship index (explicitly not a prediction).
    product_score = np.clip(df["NumOfProducts"] / 4.0, 0, 1)
    activity_score = df["IsActiveMember"]
    card_score = df["HasCrCard"]
    tenure_score = np.clip(df["Tenure"] / 10.0, 0, 1)

    df["RelationshipStrength"] = (
        100
        * (
            0.40 * activity_score
            + 0.25 * product_score
            + 0.15 * card_score
            + 0.20 * tenure_score
        )
    ).round(1)

    df["RelationshipTier"] = pd.cut(
        df["RelationshipStrength"],
        bins=[-1, 35, 60, 80, 101],
        labels=["Weak", "Developing", "Strong", "Very Strong"],
    )

    df["ChurnStatus"] = np.where(df["Exited"].eq(1), "Churned", "Retained")

    return df


def default_filters(df: pd.DataFrame) -> dict:
    """Return a filters dict covering the full dataset range."""
    return {
        "geographies": sorted(df["Geography"].unique().tolist()),
        "genders": sorted(df["Gender"].unique().tolist()),
        "engagement": sorted(df["Engagement"].unique().tolist()),
        "product_range": (int(df["NumOfProducts"].min()), int(df["NumOfProducts"].max())),
        "age_range": (int(df["Age"].min()), int(df["Age"].max())),
    }


def apply_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    """Apply the sidebar filter selections to the dataframe."""
    mask = (
        df["Geography"].isin(filters["geographies"])
        & df["Gender"].isin(filters["genders"])
        & df["Engagement"].isin(filters["engagement"])
        & df["NumOfProducts"].between(*filters["product_range"])
        & df["Age"].between(*filters["age_range"])
    )
    return df.loc[mask].copy()


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")
