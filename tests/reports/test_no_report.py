from unittest.mock import patch, mock_open

from report2junit.reports import fetch_report


def test_no_report(sample_report_path) -> None:
    m = mock_open(read_data=b"invalid data")

    with patch("report2junit.reports.open", m):
        candidate = fetch_report(f"{sample_report_path}/no-report.json")

    assert candidate is None
