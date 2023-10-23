from abc import ABC, abstractmethod


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
