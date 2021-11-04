from typing import Callable
from unittest import TestSuite

from report2junit.reports.report_factory import ReportFactory


class NoReport(ReportFactory):
    @classmethod
    def compatible(cls, data: bytes) -> bool:
        return True

    def apply(self, callback: Callable[[TestSuite], None]) -> bool:
        return False
