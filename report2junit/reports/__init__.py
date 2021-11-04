from __future__ import annotations

from typing import Type, List

from report2junit.reports.noreport import NoReport
from report2junit.reports.report_factory import ReportFactory
from report2junit.reports.cfn_nag import CfnNag
from report2junit.reports.cfn_guard import CfnGuard
from report2junit.reports.junit import JUnit
from os.path import isfile


AVAILABLE_REPORTS: List[Type[ReportFactory]] = [JUnit, CfnGuard, CfnNag]


class Report:
    @staticmethod
    def select(source: str) -> ReportFactory:
        champion: Type[ReportFactory] = NoReport

        if not isfile(source):
            return champion(b"")

        with open(source, "rb") as fp:
            data = fp.read()
            for challenger in AVAILABLE_REPORTS:
                if challenger.compatible(data):
                    champion = challenger
                    break

        return champion(data)
