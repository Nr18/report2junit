from __future__ import annotations

from typing import Callable
from junit_xml import TestSuite

from report2junit.reports.report_factory import ReportFactory


class CfnNag(ReportFactory):
    @classmethod
    def compatible(cls, data: bytes) -> bool:
        source = cls.parse(data)

        if not isinstance(source, list):
            return False

        entry: dict = next(iter(source), {})

        return "filename" in entry and "file_results" in entry

    def __create_report(self) -> TestSuite:
        source = self.parse(self.source)

        for file_findings in source:
            for violation in file_findings["file_results"]["violations"]:
                for i, resource_id in enumerate(violation["logical_resource_ids"]):
                    self.failure(
                        name=f"{violation['id']} - {violation['message']}",
                        message=f"{file_findings['filename']}#L{violation['line_numbers'][i]}",
                        classname=resource_id,
                    )

        return TestSuite("cfn-nag findings", self.cases)

    def apply(self, callback: Callable[[TestSuite], None]) -> bool:
        callback(self.__create_report())
        return True
