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
        elif num_types == 2:
            return f"({self.types[0]} {self.name} {self.types[1]})"
        else:
            return f"{self.name} {' '.join(self.types)}"


class Function(TypeOperator):
    """A binary type constructor which builds function types"""

    def __init__(self, from_type, to_type):
        super(Function, self).__init__("->", [from_type, to_type])


class CurriedFunction(Function):
    """Syntactic sugar for creating a curried function with multiple argu"""
    def __init__(self,types):
        if len(types) > 2:
            super(CurriedFunction, self).__init__(types[0], CurriedFunction(types[1:]))
        else:
            super(CurriedFunction, self).__init__(types[0], types[1])


# Basic types are constructed with a nullary type constructor
Integer = TypeOperator("int", [])  # Basic integer
Bool = TypeOperator("bool", [])  # Basic bool
Color = TypeOperator("color", [])