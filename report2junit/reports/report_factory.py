from __future__ import annotations

from abc import ABC, abstractmethod


class ReportFactory(ABC):
    def __init__(self, source: str):
        self.source_file = source

    @abstractmethod
    def convert(self, destination: str) -> None:
        """
        Convert the current report into a JUnit report and store it at the given destination.
        """
