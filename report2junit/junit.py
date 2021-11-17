from __future__ import annotations


from typing import List
from junit_xml import to_xml_report_string, TestSuite, TestCase

from report2junit.reports import Report


class JUnitOutput:
    __destination: str
    __reports: List[TestSuite]

    def __init__(self, destination: str):
        self.__destination = destination
        self.__reports = self.__load_existing()

    def __load_existing(self) -> List[TestSuite]:
        self.__reports = []
        self.apply(self.__destination)

        return self.__reports

    def apply(self, source: str) -> bool:
        return Report.select(source).apply(callback=self.add_test_suite)

    def add_test_suite(self, report: TestSuite) -> None:
        self.__reports.append(report)

    def has_failures(self) -> bool:
        def report_has_failures(report: TestSuite) -> bool:
            return any(map(case_has_failures, report.test_cases))

        def case_has_failures(case: TestCase) -> bool:
            return len(case.failures) > 0

        return any(map(report_has_failures, self.__reports))

    def write(self) -> None:
        if len(self.__reports) == 0:
            raise Exception("No reports found to write")

        with open(self.__destination, "w") as f:
            f.write(to_xml_report_string(self.__reports, prettyprint=True))
