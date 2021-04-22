""" Massachusetts Institute of Technology

Izzy Brand, 2021

Based on an implementation by Robert Smallshire
https://github.com/rob-smallshire/hindley-milner-python
"""

class TypeVariable(object):
    """A type variable standing for an arbitrary type.

    All type variables have a unique id, but names are only assigned lazily,
    when required.
    """

    next_variable_id = 0
    next_variable_name = "T0"

    def __init__(self):
        self.id = TypeVariable.next_variable_id
        TypeVariable.next_variable_id += 1
        self.__name = None

    @property
    def name(self):
        """Names are allocated to TypeVariables lazily, so that only TypeVariables
        present after analysis consume names.
        """
        if self.__name is None:
            self.__name = TypeVariable.next_variable_name
            TypeVariable.next_variable_name = "T" +\
                str(int(TypeVariable.next_variable_name[1:]) + 1)

        return self.__name

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"TypeVariable(id = {self.id})"

    @classmethod
    def reset_counters(cls):
        cls.next_variable_id = 0
        cls.next_variable_name = "T0"


class TypeOperator(object):
    """An n-ary type constructor which builds a new type from old"""

    def __init__(self, name, types):
        self.name = name
        self.types = types

    def __str__(self):
        num_types = len(self.types)
        if num_types == 0:
            return self.name
        if num_types == 1:
            return f"{self.name}({self.types[0]})"
        elif num_types == 2:
            # infix notation (specifically for functions)
            return f"({self.types[0]} {self.name} {self.types[1]})"
        elif self.name == "->":
            # multi-function notation
            return f"({', '.join([str(t) for t in self.types][:-1])} {self.name} {self.types[-1]})"
        else:
            return f"{self.name}({', '.join([str(t) for t in self.types])})"


class Function(TypeOperator):
    """A binary type constructor which builds function types"""

    def __init__(self, from_type, to_type):
        super(Function, self).__init__("->", [from_type, to_type])


class MultiFunction(TypeOperator):
    """An n-ary type constructor which builds function types"""

    def __init__(self, types):
        super(MultiFunction, self).__init__("->", types)

    # def __str__(self):
    #     print("here")
    #     return f"({', '.join([str(t) for t in self.types][:-1])} {self.name} {self.types[-1]})"


def curried_type(*types):
    """Syntactic sugar for creating a curried function with multiple args"""
    if len(types) > 2:
        return Function(types[0], curried_type(*types[1:]))
    elif len(types) == 2:
        return Function(types[0], types[1])
    else:
        assert 0, "Cannot create a function with one type."


# Basic types are constructed with a nullary type constructor
Integer = TypeOperator("int", [])  # Basic integer
Bool = TypeOperator("bool", [])  # Basic bool
Color = TypeOperator("color", [])
