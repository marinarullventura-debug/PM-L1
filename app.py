"""
app.py

Main Streamlit application.
"""

import pandas as pd
import streamlit as st
from pathlib import Path

from datetime import datetime

from config import (
    DEPARTMENTS,
    DEFAULT_CC,
    DEFAULT_EMPLOYEE_FILE
)

from audit import run_audit

from employee_lookup import (
    prepare_employee_dataframe,
    build_employee_dictionary,
    get_department_cc
)

from excel_history import (
    save_histories
)

from email_generator import (
    build_all_emails
)

from email_sender import (
    send_all,
    send_department,
    send_pm,
    preview_email
)

# ==========================================================
# PAGE
# ==========================================================

st.set_page_config(

    page_title="Audit PM L1",

    page_icon="📊",

    layout="wide"

)

st.title("📊 Audit PM L1")

st.divider()

# ==========================================================
# SESSION STATE
# ==========================================================

if "audit" not in st.session_state:

    st.session_state.audit = None

if "emails" not in st.session_state:

    st.session_state.emails = None

# NUEVO
if "employee_directory" not in st.session_state:

    st.session_state.employee_directory = None

# NUEVO
if "department_cc" not in st.session_state:

    st.session_state.department_cc = None

# NUEVO
if "audit_date" not in st.session_state:

    st.session_state.audit_date = None

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("Audit configuration")

    audit_date = st.date_input(

        "Audit date",

        value=datetime.today()

    )

    st.write(

        f"Selected month: **{audit_date.strftime('%B %Y')}**"

    )

    st.divider()

    project_file = st.file_uploader(

        "Project Performance",

        type="xlsx"

    )

    default_employee_file = None

    if Path(DEFAULT_EMPLOYEE_FILE).exists():

        st.success("Default employee list found.")

        default_employee_file = DEFAULT_EMPLOYEE_FILE

    else:

        st.warning("Default employee list not found.")

    employee_file = st.file_uploader(

        "Employee List (optional if default exists)",

        type="xlsx"

    )

    st.divider()

    st.subheader(

        "Manual indicators"

    )

    reliability = {}

    excluded = {}

    for department in DEPARTMENTS:

        st.markdown(

            f"### {department}"

        )

        reliability[department] = st.number_input(

            f"{department} Reliability",

            min_value=0.0,

            max_value=100.0,

            value=0.0,

            key=f"rel_{department}"

        )

        excluded[department] = st.number_input(

            f"{department} Excluded",

            min_value=0.0,

            max_value=100.0,

            value=0.0,

            key=f"exc_{department}"

        )

    st.divider()

    st.subheader(

        "Department CC"

    )

    cc_people = {}

    for department in DEPARTMENTS:

        cc_people[department] = st.text_area(

            department,

            value="\n".join(

                DEFAULT_CC[department]

            ),

            height=100

        ).split("\n")

    st.divider()

    run_button = st.button(

        "▶ Run Audit",

        use_container_width=True

    )

# ==========================================================
# RUN AUDIT
# ==========================================================

if run_button:

    if project_file is None:

        st.error(
            "Please upload the Project Report."
        )

        st.stop()

    with st.spinner(
        "Running audit..."
    ):

        # ----------------------------------------
        # Read Project Excel
        # ----------------------------------------

        project_df = pd.read_excel(
            project_file
        )

        # ----------------------------------------
        # Read Employee Excel
        # ----------------------------------------

        if employee_file is not None:

            employee_df = pd.read_excel(
                employee_file
            )

        elif default_employee_file is not None:

            employee_df = pd.read_excel(
                default_employee_file
            )

        else:

            st.error(
                "Employee list is required."
            )

            st.stop()

        # ----------------------------------------
        # Prepare employee dataframe
        # ----------------------------------------

        employee_df = prepare_employee_dataframe(
            employee_df
        )

        employee_directory = (
            build_employee_dictionary(
                employee_df
            )
        )

        # ----------------------------------------
        # Department CC
        # ----------------------------------------

        department_cc = {}

        for department in DEPARTMENTS:

            names = [

                name.strip()

                for name in cc_people[department]

                if name.strip()

            ]

            emails, missing = get_department_cc(

                employee_df,

                department,

                names

            )

            department_cc[department] = emails

        # ----------------------------------------
        # Run audit
        # ----------------------------------------

        audit = run_audit(

            project_df,

            pd.Timestamp(audit_date)

        )

        # ----------------------------------------
        # Save everything
        # ----------------------------------------

        st.session_state.audit = audit

        st.session_state.employee_directory = (
            employee_directory
        )

        st.session_state.department_cc = (
            department_cc
        )

        st.session_state.audit_date = (
            pd.Timestamp(audit_date)
        )

        # VERY IMPORTANT:
        # Remove previous generated emails

        st.session_state.emails = None

    st.success(
        "Audit completed successfully."
    )
# ==========================================================
# RESULTS
# ==========================================================

if st.session_state.audit is not None:

    audit = st.session_state.audit

    st.header(
        "Summary"
    )

    st.dataframe(
        audit["summary"],
        use_container_width=True
    )

    # ==========================================================
    # GLOBAL METRICS
    # ==========================================================

    summary = audit["summary"]

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Departments",
            len(summary)
        )

    with c2:

        st.metric(
            "Customer Projects",
            int(
                summary[
                    "External Projects"
                ].sum()
            )
        )

    projects_with_issues = sum(

    len(

        department["customer"][
            department["customer"]["HAS_ISSUES"]
        ]

    )

    for department in audit["departments"].values()

)

    with c3:

        st.metric(

            "Projects With Issues",

            projects_with_issues

        )
    with c4:

        st.metric(
            "Pending PO (€)",
            round(
                summary[
                    "Pending PO Amount"
                ].sum(),
                2
            )
        )
    # ==========================================================
    # DEPARTMENTS
    # ==========================================================

    tabs = st.tabs(

        DEPARTMENTS

    )

    for tab, department in zip(

        tabs,

        DEPARTMENTS

    ):

        with tab:

            data = audit["departments"][

                department

            ]

            st.subheader(

                department

            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(

                    "Customer Projects",

                    len(

                        data["customer"]

                    )

                )

            with col2:

                st.metric(

                    "Projects With Issues",
                    

                    len(

                        data["customer"][

                            data["customer"]["HAS_ISSUES"]

                        ]

                    )

                )

            with col3:

                st.metric(

                    "Delayed",

                    len(

                        data["delayed"]

                    )

                )

            display_df = data["customer"].copy()

            # Guardamos la información de auditoría
            audit_columns = display_df["AUDIT_COLUMNS"].copy()

            # Quitamos columnas internas
            display_df = display_df.drop(

                columns=[

                    "AUDIT_ISSUES",

                    "AUDIT_COLUMNS",

                    "HAS_ISSUES",

                    "HAS_PO_CONSUMED",

                    "HAS_NO_PM_HOURS",

                    "HAS_NO_HOURS_LAST_3_MONTHS",

                    "HAS_DELAYED"

                ],

                errors="ignore"

            )

            # -----------------------------------------
            # Highlight cells with issues
            # -----------------------------------------

            def highlight_row(row):

                styles = [

                    ""

                    for _ in row.index

                ]

                columns_to_paint = audit_columns.loc[row.name]

                if not isinstance(columns_to_paint, list):

                    return styles

                for column in columns_to_paint:

                    if column in row.index:

                        idx = row.index.get_loc(column)

                        styles[idx] = (
                            "background-color:#ffb3b3;"
                            "font-weight:bold;"
                        )

                return styles

            styled_df = display_df.style.apply(

                highlight_row,

                axis=1

            )

            st.dataframe(

                styled_df,

                use_container_width=True,

                height=500

            )
# ==========================================================
# ACTIONS
# ==========================================================

if st.session_state.audit is not None:

    st.divider()

    st.header("Actions")

    c1, c2 = st.columns(2)

    with c1:

        update_history = st.button(

            "💾 Update Excel History",

            use_container_width=True

        )

    with c2:

        generate_emails = st.button(

            "📧 Generate Emails",

            use_container_width=True

        )

# ==========================================================
# UPDATE HISTORY
# ==========================================================

if (

    st.session_state.audit is not None

    and

    update_history

):

    with st.spinner(

        "Updating Excel history..."

    ):

        save_histories(

            st.session_state.audit,

            reliability,

            excluded,

            st.session_state.audit_date

        )

    st.success(

        "Excel history updated."

    )

# ==========================================================
# GENERATE EMAILS
# ==========================================================

if (

    st.session_state.audit is not None

    and

    generate_emails

):

    with st.spinner(

        "Generating emails..."

    ):

        st.session_state.emails = build_all_emails(

            st.session_state.audit,

            st.session_state.employee_directory,

            st.session_state.department_cc,

            st.session_state.audit_date

        )

    st.success(

        f"{len(st.session_state.emails)} emails generated."

    )
    
# ==========================================================
# EMAILS
# ==========================================================

if st.session_state.emails is not None:

    emails = st.session_state.emails

    st.divider()

    st.header("Emails")

    rows = []

    for email in emails:

        rows.append({

            "PM": email.pm,

            "Department": email.department,

            "To": email.to,

            "CC": ", ".join(email.cc)

        })

    email_df = pd.DataFrame(rows)

    st.dataframe(

        email_df,

        use_container_width=True

    )

    st.info(

        f"{len(emails)} emails generated."

    )

    # ------------------------------------------------------
    # Global actions
    # ------------------------------------------------------

    c1, c2 = st.columns(2)

    with c1:

        send_all_button = st.button(

            "📧 Send All",

            use_container_width=True

        )

    with c2:

        preview_all_button = st.button(

            "👁 Preview All",

            use_container_width=True

        )

    if preview_all_button:

        for email in emails:

            preview_email(email)

    if send_all_button:

        with st.spinner("Sending emails..."):

            send_all(emails)

        st.success(

            f"{len(emails)} emails sent."

        )

    # ------------------------------------------------------
    # Department
    # ------------------------------------------------------

    st.divider()

    st.subheader(

        "Send by department"

    )

    department = st.selectbox(

        "Department",

        DEPARTMENTS,

        key="department_send"

    )

    if st.button(

        "📧 Send Department",

        use_container_width=True

    ):

        send_department(

            emails,

            department

        )

        st.success(

            f"{department} emails sent."

        )

    # ------------------------------------------------------
    # Individual PM
    # ------------------------------------------------------

    st.divider()

    st.subheader(

        "Send individual"

    )

    pm = st.selectbox(

        "Project Manager",

        sorted(

            [

                email.pm

                for email in emails

            ]

        ),

        key="pm_send"

    )

    c1, c2 = st.columns(2)

    with c1:

        send_pm_button = st.button(

            "📧 Send Email",

            use_container_width=True

        )

    with c2:

        preview_pm_button = st.button(

            "👁 Preview Email",

            use_container_width=True

        )

    if preview_pm_button:

        for email in emails:

            if email.pm == pm:

                preview_email(

                    email

                )

                break

    if send_pm_button:

        send_pm(

            emails,

            pm

        )

        st.success(

            f"Email sent to {pm}."

        )
        

# ==========================================================
# EMPTY PAGE
# ==========================================================

if st.session_state.audit is None:

    st.info(
        """
Welcome to the PM L1 Audit Tool.

Steps:

1. Select the audit date.
2. Upload the Project Report.
3. Upload the Employee List (optional if the default file exists).
4. Fill in the manual indicators.
5. Review the CC recipients.
6. Click **Run Audit**.
7. Review the results.
8. Click **Update Excel History** if you want to update the monthly history.
9. Click **Generate Emails** if you want to prepare the emails.
10. Preview or send the emails.
"""
    )

# ==========================================================
# ERROR HANDLING
# ==========================================================

try:

    pass

except FileNotFoundError as e:

    st.error(

        f"File not found:\n\n{e}"

    )

except PermissionError:

    st.error(

        "The Excel file is open.\n\n"
        "Please close it before updating."

    )

except ValueError as e:

    st.error(str(e))

except Exception as e:

    st.exception(e)

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

c1, c2 = st.columns([8, 2])

with c1:

    st.caption(

        "PM L1 Audit Tool"

    )

with c2:

    st.caption(

        "Version 1.0"

    )