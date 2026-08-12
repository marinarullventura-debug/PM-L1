"""
email_sender.py

Utilities to preview and send Outlook emails.
"""

from __future__ import annotations

import pythoncom
import win32com.client


# ==========================================================
# OUTLOOK
# ==========================================================

_outlook = None


def get_outlook():

    global _outlook

    if _outlook is None:

        pythoncom.CoInitialize()

        _outlook = win32com.client.Dispatch(
            "Outlook.Application"
        )

    return _outlook


# ==========================================================
# CREATE MAIL
# ==========================================================

def create_mail(email):

    outlook = get_outlook()

    mail = outlook.CreateItem(0)

    mail.To = email.to

    mail.CC = ";".join(email.cc)

    mail.Subject = email.subject

    mail.HTMLBody = email.body

    return mail


# ==========================================================
# PREVIEW
# ==========================================================

def preview_email(email):

    pythoncom.CoInitialize()

    try:

        outlook = win32com.client.DispatchEx(
            "Outlook.Application"
        )

        mail = outlook.CreateItem(0)

        mail.To = email.to
        mail.CC = ";".join(email.cc)
        mail.Subject = email.subject
        mail.HTMLBody = email.body

        mail.Display()

    finally:

        pythoncom.CoUninitialize()


# ==========================================================
# SEND
# ==========================================================

def send_email(email):

    import pythoncom
    import win32com.client

    pythoncom.CoInitialize()

    outlook = win32com.client.DispatchEx(
        "Outlook.Application"
    )

    mail = outlook.CreateItem(0)

    mail.To = email.to
    mail.CC = ";".join(email.cc)
    mail.Subject = email.subject
    mail.HTMLBody = email.body

    mail.Send()

    pythoncom.CoUninitialize()


# ==========================================================
# SEND ALL
# ==========================================================

def send_all(emails):

    for email in emails:

        send_email(email)


# ==========================================================
# SEND DEPARTMENT
# ==========================================================

def send_department(

    emails,

    department

):

    for email in emails:

        if email.department == department:

            send_email(email)


# ==========================================================
# SEND PM
# ==========================================================

def send_pm(

    emails,

    pm

):

    for email in emails:

        if email.pm == pm:

            send_email(email)

            break