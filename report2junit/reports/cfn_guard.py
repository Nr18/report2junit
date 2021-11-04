from __future__ import annotations

from typing import Callable
from junit_xml import TestSuite

from report2junit.reports.report_factory import ReportFactory


class CfnGuard(ReportFactory):
    @classmethod
    def compatible(cls, data: bytes) -> bool:
        source = cls.parse(data)

        if not isinstance(source, dict):
            return False

        return (
            "compliant" in source
            and "not_applicable" in source
            and "not_compliant" in source
        )

    def __create_report(self) -> TestSuite:
        source = self.parse(self.source)
        any(map(self.success, source.get("compliant", [])))
        any(map(self.skipped, source.get("not_applicable", [])))

        for rule in source.get("not_compliant", []):
            for check in source["not_compliant"][rule]:
                message = check["message"].split("\nMetadata")[0]

                self.failure(
                    name=check["rule"],
                    message=f"Expected: {check['expected']} Received: {check['provided']}.\n{message}",
                    classname=check["path"],
                )
        return TestSuite("cfn-guard findings", self.cases)

    def apply(self, callback: Callable[[TestSuite], None]) -> bool:
        callback(self.__create_report())
        return True
