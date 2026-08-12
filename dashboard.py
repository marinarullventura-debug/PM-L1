"""
dashboard.py
------------

All Streamlit interface components.

This module contains no business logic.
"""

import streamlit as st
import pandas as pd
# ==========================================================
# HEADER
# ==========================================================

def show_header():

    st.set_page_config(

        page_title="Project Audit",

        page_icon="📊",

        layout="wide"

    )

    st.title("📊 Project Audit Tool")

    st.divider()
# ==========================================================
# AUDIT INFORMATION
# ==========================================================

def audit_information():

    st.subheader("Audit Information")

    col1, col2 = st.columns(2)

    with col1:

        audit_date = st.date_input(

            "Audit date"

        )

    with col2:

        st.info(

            f"Audit month: {audit_date.strftime('%B %Y')}"

        )

    return audit_date
# ==========================================================
# FILES
# ==========================================================

def upload_files():

    st.subheader("Input files")

    project_file = st.file_uploader(

        "Project Report",

        type="xlsx"

    )

    employee_file = st.file_uploader(

        "Employee List",

        type="xlsx"

    )

    return project_file, employee_file
# ==========================================================
# MANUAL KPIs
# ==========================================================

def manual_kpis(

    departments

):

    st.subheader(

        "Manual indicators"

    )

    reliability = {}

    excluded = {}

    for department in departments:

        st.markdown(

            f"### {department}"

        )

        c1, c2 = st.columns(2)

        with c1:

            reliability[department] = (

                st.number_input(

                    "% Hours Reliability",

                    0.0,

                    100.0,

                    key=f"rel_{department}"

                )

            )

        with c2:

            excluded[department] = (

                st.number_input(

                    "% Users Excluded",

                    0.0,

                    100.0,

                    key=f"exc_{department}"

                )

            )

    return reliability, excluded
# ==========================================================
# CC
# ==========================================================

def cc_editor(

    default_cc

):

    st.subheader(

        "Department CC"

    )

    cc = {}

    for department, people in default_cc.items():

        value = st.text_area(

            department,

            "\n".join(people)

        )

        cc[department] = [

            p.strip()

            for p in value.split("\n")

            if p.strip()

        ]

    return cc
# ==========================================================
# SUMMARY
# ==========================================================

def show_summary(

    summary

):

    st.subheader(

        "Summary"

    )

    st.dataframe(

        summary,

        use_container_width=True

    )
# ==========================================================
# DEPARTMENTS
# ==========================================================

def show_departments(

    department_data

):

    tabs = st.tabs(

        list(

            department_data.keys()

        )

    )

    for tab, department in zip(

        tabs,

        department_data

    ):

        with tab:

            data = department_data[

                department

            ]

            st.metric(

                "Customer Projects",

                len(

                    data["customer"]

                )

            )

            st.metric(

                "Projects With Issues",

                len(

                    data["customer"][

                        data["customer"]["HAS_ISSUES"]

                    ]

                )

            )

            st.dataframe(

                data["customer"],

                use_container_width=True

            )
# ==========================================================
# EMAILS
# ==========================================================

def email_panel(

    emails

):

    st.subheader(

        "Emails"

    )

    rows = []

    for email in emails:

        rows.append({

            "PM": email.pm,

            "Department": email.department,

            "To": email.to

        })

    st.dataframe(

        pd.DataFrame(rows),

        use_container_width=True

    )
# ==========================================================
# ACTIONS
# ==========================================================

def action_buttons():

    c1, c2, c3 = st.columns(3)

    with c1:

        run = st.button(

            "▶ Run Audit",

            use_container_width=True

        )

    with c2:

        excel = st.button(

            "💾 Update Excel History",

            use_container_width=True

        )

    with c3:

        emails = st.button(

            "📧 Generate Emails",

            use_container_width=True

        )

    return run, excel, emails
