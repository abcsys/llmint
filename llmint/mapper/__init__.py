from abc import ABC, abstractmethod
from .functions import map


class Mapper(ABC):
    @abstractmethod
    def invoke(self, source, target):
        """
        Return schema mappings given source and target.
        """
        pass


__all__ = [
    'record',
    'schema',
    'output',
]
