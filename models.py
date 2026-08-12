"""
models.py
----------

Core data models used across the Project Audit Tool.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


# ============================================================
# AUDIT ISSUE
# ============================================================

@dataclass
class AuditIssue:
    """
    Represents a single audit issue detected in a project.
    """

    code: str
    title: str
    message: str
    columns: List[str]

    def __str__(self):

        return self.title


# ============================================================
# PROJECT AUDIT
# ============================================================

@dataclass
class ProjectAudit:
    """
    Stores all audit information for one project.
    """

    project: str
    pm: str
    department: str

    data: Dict

    issues: List[AuditIssue] = field(default_factory=list)

    # --------------------------------------------------------
    # Add issue
    # --------------------------------------------------------

    def add_issue(
        self,
        issue: AuditIssue
    ):

        self.issues.append(issue)

    # --------------------------------------------------------
    # Has issues?
    # --------------------------------------------------------

    @property
    def has_issues(self):

        return len(self.issues) > 0

    # --------------------------------------------------------
    # List of issue titles
    # --------------------------------------------------------

    @property
    def issue_titles(self):

        return [

            issue.title

            for issue in self.issues

        ]

    # --------------------------------------------------------
    # List of messages
    # --------------------------------------------------------

    @property
    def issue_messages(self):

        return [

            issue.message

            for issue in self.issues

        ]

    # --------------------------------------------------------
    # Highlight columns
    # --------------------------------------------------------

    @property
    def highlight_columns(self):

        columns = set()

        for issue in self.issues:

            columns.update(issue.columns)

        return sorted(columns)

    # --------------------------------------------------------
    # Excel comments
    # --------------------------------------------------------

    @property
    def audit_comment(self):

        return "\n".join(

            self.issue_titles

        )

    # --------------------------------------------------------
    # Dictionary
    # --------------------------------------------------------

    def to_dict(self):

        row = self.data.copy()

        row["AUDIT ISSUES"] = self.issue_titles

        row["AUDIT COMMENT"] = self.audit_comment

        row["AUDIT COLUMNS"] = self.highlight_columns

        row["HAS ISSUES"] = self.has_issues

        return row


# ============================================================
# DEPARTMENT AUDIT
# ============================================================

@dataclass
class DepartmentAudit:

    department: str

    projects: List[ProjectAudit] = field(
        default_factory=list
    )

    # --------------------------------------------------------

    def add_project(
        self,
        project: ProjectAudit
    ):

        self.projects.append(project)

    # --------------------------------------------------------

    @property
    def total_projects(self):

        return len(self.projects)

    # --------------------------------------------------------

    @property
    def projects_with_issues(self):

        return [

            p

            for p in self.projects

            if p.has_issues

        ]

    # --------------------------------------------------------

    @property
    def pm_list(self):

        return sorted({

            p.pm

            for p in self.projects

        })

    # --------------------------------------------------------

    def get_pm_projects(
        self,
        pm
    ):

        return [

            p

            for p in self.projects

            if p.pm == pm

        ]

    # --------------------------------------------------------

    def get_pm_projects_with_issues(
        self,
        pm
    ):

        return [

            p

            for p in self.projects

            if p.pm == pm
            and p.has_issues

        ]


# ============================================================
# AUDIT RESULT
# ============================================================

@dataclass
class AuditResult:
    """
    Final object returned by run_audit().
    """

    summary_df: object

    departments: Dict[str, DepartmentAudit]

    active_projects: object