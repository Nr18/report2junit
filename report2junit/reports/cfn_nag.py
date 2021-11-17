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
        list(self.__findings())
        return TestSuite("cfn-nag findings", self.cases)

    def __findings(self) -> map:
        return map(self.__parse_findings, self.parse(self.source))

    def __parse_findings(self, file_finding: dict) -> None:
        for violation in file_finding["file_results"]["violations"]:
            self.__parse_violation(file_finding["filename"], violation)

    def __parse_violation(self, file_name: str, violation) -> None:
        for index, resource_id in enumerate(violation["logical_resource_ids"]):
            self.failure(
                name=f"{violation['id']} - {violation['message']}",
                message=f"{file_name}#L{violation['line_numbers'][index]}",
                classname=resource_id,
            )

    def apply(self, callback: Callable[[TestSuite], None]) -> bool:
        callback(self.__create_report())
        return True
