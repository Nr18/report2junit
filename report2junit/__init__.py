import os.path
from typing import Optional, Type

import click

from report2junit.reports import available_reports, ReportFactory


@click.command()
@click.option(
    "--source-type",
    type=click.Choice(list(available_reports.keys()), case_sensitive=False),
    required=True,
)
@click.argument("source-file")
@click.argument("destination-file", required=False)
def main(source_file: str, source_type: str, destination_file: Optional[str]):
    """
    Convert2JUnit

    This tool allows you to convert various reports into the JUnit format.
    """
    source_file = os.path.abspath(source_file)

    if not destination_file:
        destination_file = os.path.splitext(source_file)[0] + ".xml"

    destination_file = os.path.abspath(destination_file)
    candidate: Optional[Type[ReportFactory]] = available_reports.get(source_type)

    if not callable(candidate):
        raise click.ClickException("Could not convert the report")

    report = candidate(source=source_file)
    report.convert(destination=destination_file)


if __name__ == "__main__":
    main()
