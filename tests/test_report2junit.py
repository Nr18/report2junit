import os.path
from unittest import mock
from unittest.mock import mock_open, patch, MagicMock
from click.testing import CliRunner
from report2junit import main
from report2junit.reports import CfnNag


def expected_payload(name: str) -> str:
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "expected_payloads", name)
    )
    with open(path) as fp:
        return fp.read()


def test_cfn_guard_conversion(sample_report_path: str) -> None:
    runner = CliRunner()
    m = mock_open()

    with patch("report2junit.reports.junit.open", m):
        result = runner.invoke(
            main,
            [
                "--source-type",
                "cfn-guard",
                f"{sample_report_path}/cfn-guard.json",
            ],
        )

    m.assert_called_once_with(f"{sample_report_path}/cfn-guard.xml", "w")
    handle = m()
    handle.write.assert_called_once_with(expected_payload("cfn-guard.xml"))
    assert result.exit_code == 0


def test_cfn_guard_conversion_explicit_destination(sample_report_path: str) -> None:
    runner = CliRunner()
    m = mock_open()

    with patch("report2junit.reports.junit.open", m):
        result = runner.invoke(
            main,
            [
                "--source-type",
                "cfn-guard",
                f"{sample_report_path}/cfn-guard.json",
                f"{sample_report_path}/cfn-guard-specific.xml",
            ],
        )

    m.assert_called_once_with(f"{sample_report_path}/cfn-guard-specific.xml", "w")
    handle = m()
    handle.write.assert_called_once_with(expected_payload("cfn-guard.xml"))
    assert result.exit_code == 0


@mock.patch("report2junit.fetch_report", return_value=CfnNag)
def test_cfn_nag_conversion(_, sample_report_path: str) -> None:
    runner = CliRunner()
    m = mock_open()

    with patch("report2junit.reports.junit.open", m):
        result = runner.invoke(
            main,
            [
                "--source-type",
                "cfn-nag",
                f"{sample_report_path}/cfn-nag.json",
            ],
        )

    m.assert_called_once_with(f"{sample_report_path}/cfn-nag.xml", "w")
    handle = m()
    handle.write.assert_called_once_with(expected_payload("cfn-nag.xml"))
    assert result.exit_code == 0


@mock.patch("report2junit.fetch_report", return_value=None)
def test_non_callable(_, sample_report_path) -> None:
    runner = CliRunner()

    with patch("report2junit.callable", MagicMock(return_value=False)):
        result = runner.invoke(
            main,
            [
                "--source-type",
                "cfn-nag",
                f"{sample_report_path}/cfn-nag.json",
            ],
        )
    assert result.exception
    assert result.exit_code == 1
    assert "Could not convert the report" in result.output
