from report2junit.reports import fetch_report


def test_cfn_nag(sample_report_path) -> None:
    candidate = fetch_report(f"{sample_report_path}/cfn-nag.json")
    assert callable(candidate)

    report = candidate(f"{sample_report_path}/cfn-nag.json")
    assert report.raw_source == report.raw_source
