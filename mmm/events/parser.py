from abc import ABC, abstractmethod
from typing import List

from . import Event


class Parser(ABC):
    @abstractmethod
    def parse(self, data) -> "Event" or List["Event"]:
        """"""
