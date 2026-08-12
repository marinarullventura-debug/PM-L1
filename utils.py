"""
utils.py
---------

Common utility functions used across the Project Audit Tool.
"""

from __future__ import annotations

import calendar
from datetime import datetime

import pandas as pd


# ==========================================================
# NUMERIC CONVERSION
# ==========================================================

def to_number(value) -> float:
    """
    Convert Excel values to float.

    Supports:

        1.250,45
        1,250.45
        €
        -
        ########
    """

    if pd.isna(value):
        return 0.0

    if isinstance(value, (int, float)):
        return float(value)

    value = str(value).strip()

    if value in ("", "-", "########"):
        return 0.0

    value = value.replace("€", "")
    value = value.replace(" ", "")

    # European format
    if "," in value:

        value = value.replace(".", "")
        value = value.replace(",", ".")

    try:

        return float(value)

    except Exception:

        return 0.0


# ==========================================================
# DATE CONVERSION
# ==========================================================

def to_date(series: pd.Series):

    return pd.to_datetime(

        series,

        errors="coerce"

    )


# ==========================================================
# CLEAN TEXT
# ==========================================================

def clean_text(series: pd.Series):

    return (

        series

        .fillna("")

        .astype(str)

        .str.strip()

    )


# ==========================================================
# CLEAN UPPER TEXT
# ==========================================================

def clean_upper(series: pd.Series):

    return (

        clean_text(series)

        .str.upper()

    )


# ==========================================================
# MONTH
# ==========================================================

def month_name(date: datetime):

    return calendar.month_name[date.month]


def month_number(date: datetime):

    return date.month


# ==========================================================
# FILTER
# ==========================================================

def filter_department(

    dataframe,

    department

):

    return dataframe[

        dataframe["DEPARTMENT"]

        == department

    ].copy()


def filter_active_projects(

    dataframe

):

    return dataframe[

        dataframe["STATUS"]

        == "IN PROGRESS"

    ].copy()


# ==========================================================
# CUSTOMER
# ==========================================================

def customer_projects(

    dataframe,

    internal_customer

):

    return dataframe[

        dataframe["CUSTOMER"]

        != internal_customer

    ].copy()


def internal_projects(

    dataframe,

    internal_customer

):

    return dataframe[

        dataframe["CUSTOMER"]

        == internal_customer

    ].copy()


# ==========================================================
# VALIDATION
# ==========================================================

def validate_columns(

    dataframe,

    required_columns

):

    missing = [

        c

        for c in required_columns

        if c not in dataframe.columns

    ]

    if missing:

        raise ValueError(

            "Missing columns:\n\n"

            + "\n".join(missing)

        )


# ==========================================================
# SAFE SUM
# ==========================================================

def safe_sum(

    dataframe,

    column

):

    if dataframe.empty:

        return 0

    return dataframe[column].sum()


# ==========================================================
# SAFE COUNT
# ==========================================================

def safe_count(

    dataframe

):

    return len(dataframe)


# ==========================================================
# PROJECT HELPERS
# ==========================================================

def project_has_issue(

    issues,

    code

):

    return any(

        issue.code == code

        for issue in issues

    )


def project_has_any_issue(

    issues

):

    return len(issues) > 0


# ==========================================================
# AUDIT DATE
# ==========================================================

def normalize_date(

    audit_date

):

    if isinstance(

        audit_date,

        str

    ):

        audit_date = pd.to_datetime(

            audit_date

        )

    return pd.Timestamp(

        audit_date

    ).normalize()


# ==========================================================
# DATAFRAME
# ==========================================================

def insert_column_if_missing(

    dataframe,

    column,

    default=None

):

    if column not in dataframe.columns:

        dataframe[column] = default

    return dataframe


# ==========================================================
# FORMAT
# ==========================================================

def money(

    value

):

    return f"{value:,.2f}"


def percentage(

    value

):

    return f"{value:.2f} %"


# ==========================================================
# MONTH SHEET NAME
# ==========================================================

def monthly_sheet_name(

    audit_date

):

    return audit_date.strftime("%B %Y")