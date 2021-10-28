from report2junit.reports.cfn_nag import CfnNag


def test_cfn_nag(sample_report_path) -> None:
    report = CfnNag(f"{sample_report_path}/cfn-nag.json")

    assert report.raw_source == report.raw_source
