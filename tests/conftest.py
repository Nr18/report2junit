import pytest
import os.path


@pytest.fixture(scope="module")
def sample_report_path() -> str:
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "sample-reports")
    )
