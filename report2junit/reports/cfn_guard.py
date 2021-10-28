from __future__ import annotations

import json

from report2junit.reports.report_factory import ReportFactory
from report2junit.reports.junit import JunitReport


class CfnGuard(ReportFactory):
    __raw_source: dict = {}

    @property
    def raw_source(self) -> dict:
        if not self.__raw_source:
            with open(self.source_file) as f:
                self.__raw_source = json.load(f)

        return self.__raw_source

    def convert(self, destination: str) -> None:
        report = JunitReport("cfn-guard findings")
        any(map(report.success, self.raw_source.get("compliant", [])))
        any(map(report.skipped, self.raw_source.get("not_applicable", [])))

        for rule in self.__raw_source.get("not_compliant", []):
            for check in self.__raw_source["not_compliant"][rule]:
                message = check["message"].split("\nMetadata")[0]

                report.failure(
                    name=check["rule"],
                    message=f"Expected: {check['expected']} Received: {check['provided']}.\n{message}",
                    classname=check["path"],
                )

        report.write(destination)
