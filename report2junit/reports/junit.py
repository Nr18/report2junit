from __future__ import annotations
from typing import Callable

from report2junit.reports.report_factory import ReportFactory
from xml.dom.minicompat import NodeList
from junit_xml import TestCase, TestSuite
from xml.dom.minidom import parseString


class JUnit(ReportFactory):
    @classmethod
    def compatible(cls, data: bytes) -> bool:
        try:
            parseString(data.decode("utf-8"))
        except Exception:
            return False

        return True

    def __parse_testsuite(self, testsuite) -> TestSuite:
        cases = []

        for case in testsuite.getElementsByTagName("testcase"):
            cases.append(self.__parse_test_case(case))

        return TestSuite(name=testsuite.getAttribute("name"), test_cases=cases)

    def __parse_test_case(self, case) -> TestCase:
        junit_case = TestCase(
            case.getAttribute("name"), classname=case.getAttribute("classname")
        )
        for failure in case.getElementsByTagName("failure"):
            junit_case.add_failure_info(
                output=self.__parse_node_list(failure.childNodes)
            )
        for skipped in case.getElementsByTagName("skipped"):
            junit_case.add_skipped_info(skipped.getAttribute("message"))
        return junit_case

    @staticmethod
    def __parse_node_list(nodes: NodeList) -> str:
        rc = []
        for node in nodes:
            rc.append(node.data)

        return "".join(rc)

    def apply(self, callback: Callable[[TestSuite], None]) -> bool:
        dom = parseString(self.source.decode("utf-8"))

        for testsuite in dom.getElementsByTagName("testsuite"):
            callback(self.__parse_testsuite(testsuite))

        return True
