""" Massachusetts Institute of Technology

Izzy Brand, 2021

Based on an implementation by Robert Smallshire
https://github.com/rob-smallshire/hindley-milner-python
"""

from util import color_names

def is_integer_literal(name):
    """Checks whether name is an integer literal string.

    Args:
        name: The identifier to check

    Returns:
        True if name is an integer literal, otherwise False
    """
    result = True
    try:
        int(name)
    except ValueError:
        result = False
    return result

def is_color_literal(name):
    """Checks whether name is an color literal string.

    Args:
        name: The identifier to check

    Returns:
        True if name is an color literal, otherwise False
    """
    return name in color_names


class InferenceError(Exception):
    """Raised if the type inference algorithm cannot infer types successfully"""

    def __init__(self, message):
        self.__message = message

    message = property(lambda self: self.__message)

    def __str__(self):
        return str(self.message)


class ParseError(Exception):
    """Raised if the supplied environment is incomplete"""

    def __init__(self, message):
        self.__message = message

    message = property(lambda self: self.__message)

    def __str__(self):
        return str(self.message)