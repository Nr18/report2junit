from report2junit.reports import fetch_report


def test_cfn_guard(sample_report_path) -> None:
    candidate = fetch_report(f"{sample_report_path}/cfn-guard.json")
    report = candidate(f"{sample_report_path}/cfn-guard.json")

    assert report.raw_source == report.raw_source
