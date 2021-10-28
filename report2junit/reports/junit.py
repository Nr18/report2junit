from __future__ import annotations

from typing import List, Optional

from junit_xml import TestCase, to_xml_report_string, TestSuite


class JunitReport:
    def __init__(self, name: str):
        self.__name = name
        self.__cases: List[TestCase] = []

    def success(self, name: str, classname: Optional[str] = None):
        case = TestCase(name, classname=classname)
        self.__cases.append(case)

    def failure(self, name: str, message: str, classname: Optional[str] = None) -> None:
        case = TestCase(name, classname=classname)
        case.add_failure_info(output=message)
        self.__cases.append(case)

    def skipped(self, name: str) -> None:
        case = TestCase(name)
        case.add_skipped_info("Skipped")
        self.__cases.append(case)

    def write(self, file_path: str) -> None:
        with open(file_path, "w") as f:
            f.write(
                to_xml_report_string(
                    [TestSuite(self.__name, self.__cases)], prettyprint=True
                )
            )
