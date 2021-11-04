from typing import Optional
import os.path
import click

from report2junit.reports import ReportFactory
from report2junit.junit import JUnitOutput
from report2junit.reports import AVAILABLE_REPORTS


@click.command()
@click.option(
    # DEPRECATED source type is being auto-detected, this option will be removed in a future release.
    "--source-type",
    type=click.Choice(["cfn-guard", "cfn-nag"], case_sensitive=False),
    required=False,
)
@click.argument("source-file")
@click.argument("destination-file", required=False)
def main(
    source_file: str, destination_file: Optional[str], source_type: Optional[str] = None
):
    """
    Convert2JUnit

    This tool allows you to convert various reports into the JUnit format.
    """
    source_file = os.path.abspath(source_file)

    if not destination_file:
        destination_file = os.path.join(os.path.dirname(source_file), "junit.xml")

    report = JUnitOutput(destination_file)

    if not report.apply(source_file):
        raise click.ClickException("Could not convert the report")

    report.write()


if __name__ == "__main__":
    main()
