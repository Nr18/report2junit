from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Callable, Optional, List
from junit_xml import TestCase, TestSuite


class ReportFactory(ABC):
    def __init__(self, source: bytes):
        self.source = source
        self.cases: List[TestCase] = []

    @classmethod
    def parse(cls, data: bytes) -> dict:
        try:
            return json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    @classmethod
    @abstractmethod
    def compatible(cls, data: bytes) -> bool:
        """
        Returns True if the report can process the given data.
        """

    @abstractmethod
    def apply(self, callback: Callable[[TestSuite], None]) -> bool:
        """
        Apply the current report to the given destination
        """

    def success(self, name: str, classname: Optional[str] = None):
        case = TestCase(name, classname=classname)
        self.cases.append(case)

    def failure(self, name: str, message: str, classname: Optional[str] = None) -> None:
        case = TestCase(name, classname=classname)
        case.add_failure_info(output=message)
        self.cases.append(case)

    def skipped(self, name: str) -> None:
        case = TestCase(name)
        case.add_skipped_info("Skipped")
        self.cases.append(case)
