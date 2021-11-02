from __future__ import annotations

import json

from report2junit.reports.report_factory import ReportFactory
from report2junit.reports.junit import JunitReport


class CfnNag(ReportFactory):
    __raw_source: dict = {}

    @property
    def raw_source(self) -> dict:
        if not self.__raw_source:
            with open(self.source_file) as f:
                self.__raw_source = json.load(f)

        return self.__raw_source

    @staticmethod
    def compatible(data: bytes) -> bool:
        try:
            source = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            return False

        return "filename" in source[0] and "file_results" in source[0]

    def convert(self, destination: str) -> None:
        report = JunitReport("cfn-nag findings")

        for file_findings in self.raw_source:
            for violation in file_findings["file_results"]["violations"]:
                for i, resource_id in enumerate(violation["logical_resource_ids"]):
                    report.failure(
                        name=f"{violation['id']} - {violation['message']}",
                        message=f"{file_findings['filename']}#L{violation['line_numbers'][i]}",
                        classname=resource_id,
                    )

        report.write(destination)
