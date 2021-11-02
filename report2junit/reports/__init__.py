from __future__ import annotations

from typing import Type, Optional

from report2junit.reports.report_factory import ReportFactory
from report2junit.reports.cfn_nag import CfnNag
from report2junit.reports.cfn_guard import CfnGuard


def fetch_report(file: str) -> Optional[Type[ReportFactory]]:
    with open(file, "rb") as fp:
        data = fp.read()
        for report in [CfnGuard, CfnNag]:
            if report.compatible(data):
                return report

    return None
