import pytest

from unittest.mock import mock_open, patch
from click.testing import CliRunner
from report2junit import main
from tests import expected_payload


@pytest.mark.parametrize(
    "fail_on_failures, input_file, expected_exit_code",
    [
        (False, "cfn-guard.json", 0),
        (True, "cfn-guard.json", 1),
        (False, "cfn-guard-fully-compliant.json", 0),
        (True, "cfn-guard-fully-compliant.json", 0),
        (False, "cfn-nag.json", 0),
        (True, "cfn-nag.json", 1),
        (False, "cfn-guard-skipped-only.json", 0),
        (True, "cfn-guard-skipped-only.json", 0),
    ],
)
def test_single_report_conversion(
    fail_on_failures: bool,
    input_file: str,
    expected_exit_code: int,
    sample_reports_path: str,
) -> None:
    runner = CliRunner()
    m = mock_open()

    with patch("report2junit.junit.open", m):
        result = runner.invoke(
            main,
            [
                "--fail-on-failures" if fail_on_failures else "--ignore-failures",
                f"{sample_reports_path}/{input_file}",
            ],
        )

    m.assert_called_once_with(f"{sample_reports_path}/junit.xml", "w")
    handle = m()
    handle.write.assert_called_once_with(
        expected_payload(input_file.replace(".json", ".xml"))
    )
    assert result.exit_code == expected_exit_code


def test_cfn_guard_conversion_explicit_destination(sample_reports_path: str) -> None:
    runner = CliRunner()
    m = mock_open()

    with patch("report2junit.junit.open", m):
        result = runner.invoke(
            main,
            [
                "--ignore-failures",
                f"{sample_reports_path}/cfn-guard.json",
                "--destination-file",
                f"{sample_reports_path}/cfn-guard-specific.xml",
            ],
        )

    m.assert_called_once_with(f"{sample_reports_path}/cfn-guard-specific.xml", "w")
    handle = m()
    handle.write.assert_called_once_with(expected_payload("cfn-guard.xml"))
    assert result.exit_code == 0


def test_unknown_report(sample_reports_path: str) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            f"{sample_reports_path}/unknown-format.json",
        ],
    )

    assert result.exception
    assert result.exit_code == 1
    assert "Could not convert the report" in result.output
