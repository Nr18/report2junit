from unittest.mock import mock_open, patch, MagicMock

import pytest
from report2junit.junit import JUnitOutput
from report2junit.reports import NoReport
from tests import expected_payload, expected_payload_bytes


def test_no_reports(sample_reports_path: str) -> None:
    report = JUnitOutput(f"{sample_reports_path}/junit.xml")

    with pytest.raises(Exception) as exception:
        report.write()

    assert "No reports found to write" in str(exception)


def test_junit_output_non_existing(sample_reports_path) -> None:
    with patch("os.path.isfile", MagicMock(return_value=False)):
        report = JUnitOutput(f"{sample_reports_path}/junit.xml")

    report.apply(f"{sample_reports_path}/cfn-nag.json")
    destination_report = mock_open()

    with patch("report2junit.junit.open", destination_report):
        report.write()

    destination_report.assert_called_with(f"{sample_reports_path}/junit.xml", "w")
    destination_report().write.assert_called_once_with(expected_payload("cfn-nag.xml"))


def test_junit_output_merge_existing(sample_reports_path) -> None:
    existing_report = mock_open(read_data=expected_payload_bytes("cfn-guard.xml"))

    with patch("report2junit.reports.open", existing_report):
        with patch("report2junit.reports.isfile", MagicMock(return_value=True)):
            report = JUnitOutput(f"{sample_reports_path}/junit.xml")

    report.apply(f"{sample_reports_path}/cfn-nag.json")

    destination_report = mock_open()
    with patch("report2junit.junit.open", destination_report):
        report.write()

    destination_report.assert_called_with(f"{sample_reports_path}/junit.xml", "w")
    destination_report().write.assert_called_once_with(expected_payload("combined.xml"))


def test_no_report_compatibility() -> None:
    assert NoReport.compatible(b"") is True


def test_no_report_parse() -> None:
    assert NoReport.parse(b"") == {}
    assert NoReport.parse(b"Some test") == {}
    assert NoReport.parse(b"<xml></xml>") == {}
