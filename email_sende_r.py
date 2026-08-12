"""
email_sender.py

Dummy implementation for macOS.
Replace with win32com version on Windows.
"""

def preview_email(email):
    print("=" * 80)
    print("PREVIEW EMAIL")
    print("=" * 80)
    print("TO:", email.to)
    print("CC:", ", ".join(email.cc))
    print("SUBJECT:", email.subject)
    print(email.body)
    print("=" * 80)


def send_email(email):
    print(f"Email to {email.to} (simulation)")


def send_all(emails):
    for email in emails:
        send_email(email)


def send_department(emails, department):
    for email in emails:
        if email.department == department:
            send_email(email)


def send_pm(emails, pm):
    for email in emails:
        if email.pm == pm:
            send_email(email)
            break
