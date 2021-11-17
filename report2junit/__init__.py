from typing import Optional, List
import os.path
import click

from report2junit.reports import ReportFactory
from report2junit.junit import JUnitOutput
from report2junit.reports import AVAILABLE_REPORTS


@click.command()
@click.argument("source-files", nargs=-1)
@click.option("--destination-file", required=False)
@click.option("--fail-on-failures/--ignore-failures", default=True)
def main(
    source_files: List[str], destination_file: Optional[str], fail_on_failures: bool
) -> None:
    """
    Convert2JUnit

    This tool allows you to convert various reports into the JUnit format.
    """
    report = initialize_report(destination_file, source_files)
    apply_source_files(report, source_files)
    report.write()

    if fail_on_failures and report.has_failures():
        raise click.ClickException(
            "report2junit detected that the report contains failures"
        )


def apply_source_files(report: JUnitOutput, source_files: List[str]) -> None:
    for source_file in source_files:
        source_file = os.path.abspath(source_file)

        if not report.apply(source_file):
            raise click.ClickException("Could not convert the report")


def initialize_report(
    destination_file: Optional[str], source_files: List[str]
) -> JUnitOutput:
    if not destination_file:
        destination_file = os.path.join(os.path.dirname(source_files[0]), "junit.xml")

    return JUnitOutput(destination_file)


if __name__ == "__main__":
    main()
