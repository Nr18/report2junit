from __future__ import annotations

from report2junit.reports.report_factory import ReportFactory
from report2junit.reports.junit import JunitReport


class CfnNag(ReportFactory):
    @classmethod
    def compatible(cls, data: bytes) -> bool:
        source = cls._read_data(data)

        if not isinstance(source, list):
            return False

        entry: dict = next(iter(source), {})

        return "filename" in entry and "file_results" in entry

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
