from typing import Iterable


class EmptyStackPopError(Exception):
    """Raises when trying to pop from empty Stack"""


class Stack:

    def __init__(self, source: Iterable):
        self.__data = list(source) if not isinstance(source, list) else source

    def push(self, item):
        self.__data.append(item)

    def pop(self):
        if self.is_empty():
            raise EmptyStackPopError("Cannot pop element from empty stack!")

        return self.__data.pop()

    def is_empty(self):
        return len(self.__data) == 0



