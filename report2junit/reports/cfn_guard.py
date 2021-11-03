from __future__ import annotations

from report2junit.reports.report_factory import ReportFactory
from report2junit.reports.junit import JunitReport


class CfnGuard(ReportFactory):
    @classmethod
    def compatible(cls, data: bytes) -> bool:
        source = cls._read_data(data)

        if not isinstance(source, dict):
            return False

        return (
            "compliant" in source
            and "not_applicable" in source
            and "not_compliant" in source
        )

    def convert(self, destination: str) -> None:
        report = JunitReport("cfn-guard findings")
        any(map(report.success, self.raw_source.get("compliant", [])))
        any(map(report.skipped, self.raw_source.get("not_applicable", [])))

        for rule in self.raw_source.get("not_compliant", []):
            for check in self.raw_source["not_compliant"][rule]:
                message = check["message"].split("\nMetadata")[0]

                report.failure(
                    name=check["rule"],
                    message=f"Expected: {check['expected']} Received: {check['provided']}.\n{message}",
                    classname=check["path"],
                )

        report.write(destination)
