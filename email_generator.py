"""
email_generator.py
------------------

Creates the emails sent to each PM.

This module DOES NOT send emails.

It only builds them.
"""

from __future__ import annotations

import pandas as pd
from dataclasses import dataclass
from typing import List
from config import QUALITY_EMAIL


@dataclass
class Email:

    to: str

    cc: List[str]

    subject: str

    body: str

    department: str

    pm: str
def dataframe_to_html(df):

    columns = [

        "PROJECT",

        "CUSTOMER",

        "ESTIMATED END DATE",

        "AUDIT_COMMENT"

    ]

    df = df[columns].copy()
    df["AUDIT_COMMENT"] = (
        df["AUDIT_COMMENT"]
        .astype(str)
        .str.replace("\n", "<br>", regex=False)
    )

    return df.to_html(

        index=False,

        border=1,

        justify="center",

        escape=False

    )
def build_subject(

    department,

    audit_date

):

    return (

        f"[PM L1 Audit] "

        f"{department} "

        f"- "

        f"{audit_date.strftime('%B %Y')}"

    )
def build_body(
    pm,
    dataframe,
    audit_date
):

    html_table = dataframe_to_html(
        dataframe
    )

    num_projects = len(dataframe)

    return f"""
<html>

<head>

<style>

body {{
    font-family: "Segoe UI", Calibri, Arial, sans-serif;
    font-size: 14px;
    color: #333333;
    margin: 25px;
}}

.container {{
    max-width: 900px;
}}

.header {{
    border-bottom: 3px solid #FF6A01;
    padding-bottom: 12px;
    margin-bottom: 25px;
}}

.title {{
    color: #FF6A01;
    font-size: 24px;
    font-weight: 600;
}}

.subtitle {{
    color: #777777;
    font-size: 14px;
    margin-top: 4px;
}}

p {{
    line-height: 1.6;
}}

.audit-title {{
    margin-top: 30px;
    margin-bottom: 12px;
    font-size: 16px;
    font-weight: 600;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
    margin-bottom: 30px;
}}

th {{
    background: #F7F7F7;
    color: #333333;
    font-weight: 600;
    text-align: left;
    padding: 10px;
    border-bottom: 2px solid #FF6A01;
}}

td {{
    padding: 10px;
    border-bottom: 1px solid #E6E6E6;
    vertical-align: top;
}}

.footer {{
    margin-top: 35px;
    padding-top: 15px;
    border-top: 1px solid #DDDDDD;
    color: #666666;
}}

</style>

</head>

<body>

<div class="container">



</div>

<p>
Dear <strong>{pm}</strong>,
</p>

<p>
The monthly PM L1 Audit has identified
<strong>{num_projects} project(s)</strong>
requiring your review.
</p>

<p>
Please review the projects listed below and update the corresponding information if necessary.
</p>

<div class="audit-title">
Projects requiring review
</div>

{html_table}

<p>
Please verify that:
</p>

<ul>
<li>The project information is correct.</li>
<li>Any required updates have been completed.</li>
<li>The detected findings have a justified business reason.</li>
<li>The project status is still valid.</li>
</ul>

<p>
If you have any questions, please contact the Quality Team.
</p>

<div class="footer">

Kind regards,

<br><br>

<strong>Quality Team</strong><br>
Applus+ IDIADA

</div>

</div>

</body>

</html>
"""

def build_pm_email(

    pm,

    pm_projects,

    to,

    cc,

    department,

    audit_date

):
    cc=list(cc)
    if QUALITY_EMAIL not in cc:
        cc.append(QUALITY_EMAIL)

    return Email(

        to=to,

        cc=cc,

        subject=build_subject(

            department,

            audit_date

        ),

        body=build_body(

            pm,

            pm_projects,

            audit_date

        ),

        department=department,

        pm=pm

    )
def build_department_emails(

    department,

    department_data,

    employee_directory,

    cc_emails,

    audit_date

):

    emails = []

    pm_summary = department_data[

        "pm_summary"

    ]

    for pm, info in pm_summary.items():

        issues = info["issues"]

        if issues.empty:

            continue

        to = employee_directory.get(

            pm.upper().replace(" ", "")

        )

        if to is None:

            print(f"PM not found: {pm}")

            continue

        emails.append(

            build_pm_email(

                pm,

                issues,

                to,

                cc_emails,

                department,

                audit_date

            )

        )

    return emails
def build_all_emails(

    audit,

    employee_directory,

    department_cc,

    audit_date

):

    emails = []

    for department in audit["departments"]:

        emails.extend(

            build_department_emails(

                department,

                audit["departments"][

                    department

                ],

                employee_directory,

                department_cc[department],

                audit_date

            )

        )

    return emails
