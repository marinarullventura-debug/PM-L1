"""
employee_lookup.py

Employee directory.

Responsible for

- Reading employee list
- Finding employee emails
- Finding CC emails
"""

from __future__ import annotations

import pandas as pd

from config import DEFAULT_CC

# ==========================================================
# NORMALIZE NAME
# ==========================================================

def normalize_name(name):

    if pd.isna(name):

        return ""

    name = str(name)

    name = name.upper()

    name = name.replace(",", " ")

    name = name.replace(".", " ")

    name = " ".join(name.split())

    name = name.replace(" ", "")

    return name

# ==========================================================
# PREPARE EMPLOYEE LIST
# ==========================================================

def prepare_employee_dataframe(df):

    df = df.copy()

    df["NORMALIZED_NAME"] = (

        df["Name"]

        .apply(normalize_name)

    )

    return df

# ==========================================================
# FIND EMAIL
# ==========================================================

def get_email(

    employee_df,

    person

):

    person = normalize_name(person)

    result = employee_df[

        employee_df["NORMALIZED_NAME"]

        == person

    ]

    if result.empty:

        return None

    return result.iloc[0]["Email"]

# ==========================================================
# MULTIPLE EMAILS
# ==========================================================

def get_emails(

    employee_df,

    people

):

    emails = []

    missing = []

    for person in people:

        email = get_email(

            employee_df,

            person

        )

        if email:

            emails.append(email)

        else:

            missing.append(person)

    return emails, missing

# ==========================================================
# PM EMAIL
# ==========================================================

def get_pm_email(

    employee_df,

    pm

):

    return get_email(

        employee_df,

        pm

    )
# ==========================================================
# DEFAULT CC
# ==========================================================

def get_department_cc(

    employee_df,

    department,

    custom_cc=None

):
    """
    Returns email addresses for CC.

    If custom_cc is provided,
    Streamlit settings override
    config.py.
    """

    if custom_cc is None:

        people = DEFAULT_CC.get(

            department,

            []

        )

    else:

        people = custom_cc

    return get_emails(

        employee_df,

        people

    )
# ==========================================================
# EMPLOYEE DICTIONARY
# ==========================================================

def build_employee_dictionary(

    employee_df

):

    directory = {}

    for _, row in employee_df.iterrows():

        directory[

            row["NORMALIZED_NAME"]

        ] = row["Email"]

    return directory
