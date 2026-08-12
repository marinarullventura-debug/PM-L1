"""
audit.py
---------

Main audit engine.

Responsibilities
----------------
- Validate project report
- Clean dataframe
- Apply audit rules
- Calculate KPIs
- Prepare department data
"""

from __future__ import annotations

import pandas as pd

from config import (
    DEPARTMENTS,
    INTERNAL_CUSTOMER,
    SPECIAL_PM_DEPARTMENTS
)

from rules import AUDIT_RULES

from utils import (
    clean_text,
    clean_upper,
    to_number,
    filter_active_projects,
    filter_department,
    customer_projects,
    internal_projects,
    safe_sum,
    normalize_date
)

# ==========================================================
# REQUIRED COLUMNS
# ==========================================================

REQUIRED_COLUMNS = [

    "PROJECT",
    "PM",
    "CUSTOMER",
    "STATUS",
    "PO PENDING AMOUNT (SCY)",
    "ESTIMATED END DATE",
    "DEPARTMENT",
    "WITH PM HOURS",
    "WITH HOURS DURING LAST 3 MONTHS",
    "NUM SAMPLES"

]

# ==========================================================
# SPLIT VD / NVH
# ==========================================================

def split_vd_nvh(df):

    df = df.copy()

    for pm, department in SPECIAL_PM_DEPARTMENTS.items():

        mask = (
            (df["DEPARTMENT"] == "VD_NVH_AT") &
            (df["PM"].str.upper().str.strip() == pm)
        )

        df.loc[mask, "DEPARTMENT"] = department

    # Todos los demás pasan a VD_AT
    df.loc[
        df["DEPARTMENT"] == "VD_NVH_AT",
        "DEPARTMENT"
    ] = "VD_AT"

    return df
    
# ==========================================================
# PREPARE DATAFRAME
# ==========================================================

def prepare_dataframe(df: pd.DataFrame):

    """
    Cleans imported project report.
    """

    df = df.copy()

    # -----------------------------
    # Validate columns
    # -----------------------------

    missing = [

        c

        for c in REQUIRED_COLUMNS

        if c not in df.columns

    ]

    if missing:

        raise ValueError(

            "Missing columns:\n\n"

            + "\n".join(missing)

        )

    # -----------------------------
    # Text
    # -----------------------------

    df["PROJECT"] = clean_text(

        df["PROJECT"]

    )

    df["PM"] = clean_text(

        df["PM"]

    )

    df["CUSTOMER"] = clean_text(

        df["CUSTOMER"]

    )

    df["STATUS"] = clean_upper(

        df["STATUS"]

    )

    df["DEPARTMENT"] = clean_text(

        df["DEPARTMENT"]

    )

    df["WITH PM HOURS"] = clean_upper(

        df["WITH PM HOURS"]

    )

    df["WITH HOURS DURING LAST 3 MONTHS"] = clean_upper(

        df["WITH HOURS DURING LAST 3 MONTHS"]

    )

    # -----------------------------
    # Numbers
    # -----------------------------

    df["PO PENDING AMOUNT (SCY)"] = (

        df["PO PENDING AMOUNT (SCY)"]

        .apply(to_number)

    )

    df["NUM SAMPLES"] = (

        pd.to_numeric(

            df["NUM SAMPLES"],

            errors="coerce"

        )

        .fillna(0)

    )

    # -----------------------------
    # Dates
    # -----------------------------

    df["ESTIMATED END DATE"] = pd.to_datetime(

        df["ESTIMATED END DATE"],

        errors="coerce"

    )
    df = split_vd_nvh(df)


    return df
# ==========================================================
# APPLY RULES
# ==========================================================

def apply_rules(

    dataframe,

    audit_date

):

    dataframe = dataframe.copy()

    issues = []

    comments = []

    highlight_columns = []

    has_issues = []

    has_po = []

    has_pm = []

    has_hours = []

    has_delayed = []

    for _, row in dataframe.iterrows():

        project_issues = []

        project_comments = []

        project_columns = set()

        flags = {

            "PO": False,

            "NO_PM": False,

            "NO_HOURS": False,

            "DELAYED": False

        }

        for rule in AUDIT_RULES:

            issue = rule.evaluate(

                row,

                audit_date

            )

            if issue is None:

                continue

            project_issues.append(

                issue

            )

            project_comments.append(

                issue.title

            )

            project_columns.update(

                issue.columns

            )

            flags[issue.code] = True
            
        # -----------------------------------------
        # Save project audit information
        # -----------------------------------------

        issues.append("; ".join(issue.code for issue in project_issues))

        comments.append(

            "\n".join(project_comments)

        )

        highlight_columns.append(

            sorted(project_columns)

        )

        has_issues.append(

            len(project_issues) > 0

        )

        has_po.append(

            flags["PO"]

        )

        has_pm.append(

            flags["NO_PM"]

        )

        has_hours.append(

            flags["NO_HOURS"]

        )

        has_delayed.append(

            flags["DELAYED"]

        )

    dataframe["AUDIT_ISSUES"] = issues

    dataframe["AUDIT_COMMENT"] = comments

    dataframe["AUDIT_COLUMNS"] = highlight_columns

    dataframe["HAS_ISSUES"] = has_issues

    dataframe["HAS_PO_CONSUMED"] = has_po

    dataframe["HAS_NO_PM_HOURS"] = has_pm

    dataframe["HAS_NO_HOURS_LAST_3_MONTHS"] = has_hours

    dataframe["HAS_DELAYED"] = has_delayed

    return dataframe


# ==========================================================
# KPI CALCULATION
# ==========================================================

def calculate_kpis(

    department,

    department_df,

    audit_date

):

    internal_df = internal_projects(

        department_df,

        INTERNAL_CUSTOMER

    )

    customer_df = customer_projects(

        department_df,

        INTERNAL_CUSTOMER

    )

    po_consumed = customer_df[

        customer_df["HAS_PO_CONSUMED"]

    ]

    no_pm = customer_df[

        customer_df["HAS_NO_PM_HOURS"]

    ]

    no_hours = customer_df[

        customer_df["HAS_NO_HOURS_LAST_3_MONTHS"]

    ]

    delayed = customer_df[

        customer_df["HAS_DELAYED"]

    ]

    close_this_year = customer_df[

        customer_df["ESTIMATED END DATE"]

        .dt.year == audit_date.year

    ]

    kpis = {

        "Department": department,

        "Internal Projects": len(

            internal_df

        ),

        "External Projects": len(

            customer_df

        ),

        "Projects with PO Consumed": len(

            po_consumed

        ),

        "Projects to Close This Year": len(

            close_this_year

        ),

        "Projects Without Hours Last 3 Months": len(

            no_hours

        ),

        "Number of Samples": safe_sum(

            customer_df,

            "NUM SAMPLES"

        ),

        "Pending PO Amount": round(

            safe_sum(

                customer_df,

                "PO PENDING AMOUNT (SCY)"

            ),

            2

        ),

        "Projects Without PM Hours": len(

            no_pm

        ),

        "Delayed Projects": len(

            delayed

        ),

        "Samples In Delayed Projects": safe_sum(

            delayed,

            "NUM SAMPLES"

        )

    }

    department_data = {

        "all": department_df,

        "customer": customer_df,

        "internal": internal_df,

        "po_consumed": po_consumed,

        "without_pm_hours": no_pm,

        "without_hours_last_3_months": no_hours,

        "delayed": delayed,

        "close_this_year": close_this_year

    }

    return kpis, department_data
# ==========================================================
# BUILD PM SUMMARY
# ==========================================================

def build_pm_summary(customer_df):

    """
    Groups customer projects by PM.

    Returns
    -------
    dict

    {
        "John Smith":
        {
            "projects": DataFrame,
            "issues": DataFrame
        }
    }
    """

    summary = {}

    if customer_df.empty:
        return summary

    for pm in sorted(customer_df["PM"].dropna().unique()):

        pm_df = customer_df[
            customer_df["PM"] == pm
        ].copy()

        summary[pm] = {

            "projects": pm_df,

            "issues": pm_df[
                pm_df["HAS_ISSUES"]
            ].copy()

        }

    return summary


# ==========================================================
# BUILD DEPARTMENT
# ==========================================================

def build_department(

    active_projects,

    department,

    audit_date

):

    department_df = filter_department(

        active_projects,

        department

    )

    department_df = apply_rules(

        department_df,

        audit_date

    )

    kpis, department_data = calculate_kpis(

        department,

        department_df,

        audit_date

    )

    department_data["pm_summary"] = build_pm_summary(

        department_data["customer"]

    )

    return kpis, department_data


# ==========================================================
# RUN AUDIT
# ==========================================================

def run_audit(

    project_df,

    audit_date

):

    audit_date = normalize_date(

        audit_date

    )

    # ---------------------------------------------
    # Prepare dataframe
    # ---------------------------------------------

    project_df = prepare_dataframe(

        project_df

    )

    # ---------------------------------------------
    # Keep only IN PROGRESS
    # ---------------------------------------------

    active_projects = filter_active_projects(

        project_df

    )

    summary = []

    departments = {}

    # ---------------------------------------------
    # Loop departments
    # ---------------------------------------------

    for department in DEPARTMENTS:

        kpis, data = build_department(

            active_projects,

            department,

            audit_date

        )

        summary.append(

            kpis

        )

        departments[department] = data

    summary_df = pd.DataFrame(

        summary

    )

    audit = {

        "summary": summary_df,

        "departments": departments,

        "active_projects": active_projects,

        "audit_date": audit_date

    }

    return audit

            
