import os.path


def expected_payload_bytes(name: str) -> bytes:
    path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "expected_payloads", name)
    )
    with open(path, "rb") as fp:
        return fp.read()


def expected_payload(name: str) -> str:
    return expected_payload_bytes(name).decode("utf-8")
