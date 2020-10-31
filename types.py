class Type:
    """ Base type for things like numbers and arrays
    """
    def __init__(self, T):
        self.T = T

    def __str__(self):
        return self.T

class TupleType(Type):
    """ Describes the type of a tuple of items

    Extends:
        Type
    """
    def __init__(self, *args):
        super(TupleType, self).__init__(args)

    def __str__(self):
        return f"({', '.join(str(t) for t in self.T)})"

class ArrayType(Type):
    """ Describes the type of an array or list of items.

    Extends:
        Type
    """
    def __init__(self, T):
        super(ArrayType, self).__init__(T)

    def __str__(self):
        return f"ArrayOf{str(self.T)}"

class FuncType(Type):
    """ Describes the type of a function. Functions with multiple inputs or
    multiples outputs use the TupleType to wrap the inputs and outputs

    Extends:
        Type
    """
    def __init__(self, T_in, T_out):

        # convert types to tuples as needed
        if isinstance(T_in, tuple): T_in = TupleType(*T_in)
        if isinstance(T_out, tuple): T_out = TupleType(*T_out)

        super(FuncType, self).__init__((T_in, T_out))

    def __str__(self):
        return f"{str(self.T[0])} -> {str(self.T[1])}"

class TemplateType(Type):
    """ Some functions can handle multiple types. For example map has a return
    type which depends on the function being mapped. This template type is for
    that purpose

    Extends:
        Type
    """
    def __init__(self, T):
        super(TemplateType, self).__init__(T)

    def __str__(self):
        return f"<{self.T}>"


if __name__ == '__main__':
    i_T = Type("Int")
    c_T = Type("Color")
    a_T = Type("Array")
    l_t = Type("List")

    # example of a function that counts the number of pixels of a certain color
    colorcount_T = FuncType((a_T, c_T), i_T)
    print("colorcount:", colorcount_T)

    # example of the type of map using a template type
    T1 = TemplateType(1)
    T2 = TemplateType(2)
    input_type = (ArrayType(T1), FuncType(T1, T2))
    output_type = ArrayType(T2)
    map_T = FuncType(input_type, output_type)
    print("map:", map_T)
