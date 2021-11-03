from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any


class ReportFactory(ABC):
    __raw_source: dict = {}

    def __init__(self, source: str):
        self.source_file = source

    @property
    def raw_source(self) -> dict:
        if not self.__raw_source:
            with open(self.source_file, "rb") as fp:
                self.__raw_source = self._read_data(fp.read())

        return self.__raw_source

    @classmethod
    def _read_data(cls, data: bytes) -> Any:
        try:
            return json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    @abstractmethod
    def convert(self, destination: str) -> None:
        """
        Convert the current report into a JUnit report and store it at the given destination.
        """

    @classmethod
    @abstractmethod
    def compatible(cls, data: bytes) -> bool:
        """
        Returns True if the report can process the given data.
        """
