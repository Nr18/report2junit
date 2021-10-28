from __future__ import annotations

from typing import Dict, Type

from report2junit.reports.report_factory import ReportFactory
from report2junit.reports.cfn_nag import CfnNag
from report2junit.reports.cfn_guard import CfnGuard


available_reports: Dict[str, Type[ReportFactory]] = {
    "cfn-guard": CfnGuard,
    "cfn-nag": CfnNag,
}
