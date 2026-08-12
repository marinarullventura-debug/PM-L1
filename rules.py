"""
rules.py
---------

Audit rules.

Each rule analyses ONE project and returns
an AuditIssue if the project violates the rule.
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import pandas as pd

from models import AuditIssue
from config import INTERNAL_CUSTOMER


# ============================================================
# BASE RULE
# ============================================================

class AuditRule(ABC):

    """
    Base class for all audit rules.
    """

    code = ""

    title = ""

    message = ""

    columns = []

    @abstractmethod
    def check(
        self,
        project: pd.Series,
        audit_date: pd.Timestamp
    ):
        pass

    # --------------------------------------------------------

    def evaluate(

        self,

        project,

        audit_date

    ):

        if self.check(

            project,

            audit_date

        ):

            return AuditIssue(

                code=self.code,

                title=self.title,

                message=self.message,

                columns=self.columns

            )

        return None

# ============================================================
# PO CONSUMED
# ============================================================

class POConsumedRule(AuditRule):

    code = "PO"

    title = "PO Consumed"

    message = (
        "Purchase Order has been fully consumed."
    )

    columns = [

        "PROJECT",

        "PO PENDING AMOUNT (SCY)"

    ]

    def check(

        self,

        project,

        audit_date

    ):

        if project["CUSTOMER"] == INTERNAL_CUSTOMER:

            return False

        return (

            project["PO PENDING AMOUNT (SCY)"]

            <= 0

        )


# ============================================================
# WITHOUT PM HOURS
# ============================================================

class NoPMHoursRule(AuditRule):

    code = "NO_PM"

    title = "Without PM Hours"

    message = (

        "Project has no PM hours."

    )

    columns = [

        "PROJECT",

        "WITH PM HOURS"

    ]

    def check(

        self,

        project,

        audit_date

    ):

        if project["CUSTOMER"] == INTERNAL_CUSTOMER:

            return False

        return (

            project["WITH PM HOURS"]

            == "NO"

        )

# ============================================================
# WITHOUT HOURS LAST 3 MONTHS
# ============================================================

class NoHoursLast3MonthsRule(AuditRule):

    code = "NO_HOURS"

    title = "Without Hours During Last 3 Months"

    message = (

        "Project has no hours during the last 3 months."

    )

    columns = [

        "PROJECT",

        "WITH HOURS DURING LAST 3 MONTHS"

    ]

    def check(

        self,

        project,

        audit_date

    ):

        if project["CUSTOMER"] == INTERNAL_CUSTOMER:

            return False

        return (

            project[

                "WITH HOURS DURING LAST 3 MONTHS"

            ]

            == "NO"

        )

# ============================================================
# DELAYED PROJECT
# ============================================================

class DelayedRule(AuditRule):

    code = "DELAYED"

    title = "Delayed"

    message = (

        "Estimated End Date has passed."

    )

    columns = [

        "PROJECT",

        "ESTIMATED END DATE"

    ]

    def check(

        self,

        project,

        audit_date

    ):

        if project["CUSTOMER"] == INTERNAL_CUSTOMER:

            return False

        end_date = project["ESTIMATED END DATE"]

        if pd.isna(end_date):

            return False

        return (

            end_date

            < audit_date

        )

# ============================================================
# REGISTER RULES
# ============================================================

AUDIT_RULES = [

    POConsumedRule(),

    NoPMHoursRule(),

    NoHoursLast3MonthsRule(),

    DelayedRule()

]