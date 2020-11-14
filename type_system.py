import numpy as np
import operator as op

class Primitive:
    """ Primitives are our equivalent of python's object.

    Primitives are used to create the top-level environment of the DSL, which
    includes all the functions that are by-default available to the synthesis
    engine. The reason we wrap functions in a Primitive class is because this
    allows us to specify the Type of the object.

    Attributes:
        name {sting} -- the name of this primitive
        T {Type} -- The type of this Primitive
    """
    def __init__(self, name, T):
        self.name = name
        self.T = T

    def __call__(self):
        return self

    def __str__(self):
        return self.name


# NOTE(izzy): We could simply pass around the string representation of a type,
# but for type_check (when we want to ensure that the types of a program are
# consistent, ie. that the output type of a function matches the input type of
# the next function), we would have to parse the string representation of
# higher-order types. For this reason we implement the `Type` class

class Type:
    """ Base type
    """
    def __init__(self, T):
        self.T = T

    def __str__(self):
        return self.T

    def accepts(self, other):
        """ When self if the specified argument type of the function, we need
        to check if that function will  accept an argument of Type other

        Arguments:
            other {Type} -- the type of the given argument

        Returns:
            bool -- True if other is a valid argument to self
        """
        if not isinstance(other, self.__class__): return False
        else: return str(self) == str(other)

class TupleType(Type):
    """ Describes the type of a tuple of items

    Extends:
        Type
    """
    def __init__(self, *args):
        super(TupleType, self).__init__(args)

    def __str__(self):
        return f"({', '.join(str(t) for t in self.T)})"

    # make sure length and indexing still work
    def __len__(self):
        return len(self.T)
    def __getitem__(self, item):
        return tuple.__getitem__(self.T, item)

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
        self.T_in = T_in
        self.T_out = T_out

    def __str__(self):
        return f"{str(self.T_in)} -> {str(self.T_out)}"

class ArrayType(Type):
    """ Describes the type of an array or list of items.

    Extends:
        Type
    """
    def __init__(self, T):
        super(ArrayType, self).__init__(T)

    def accepts(self, other):
        if not isinstance(other, self.__class__): return False
        else: return self.T.accepts(other.T)

    def __str__(self):
        return f"Array{str(self.T)}"

class Array1DType(ArrayType):
    def __str__(self):
        return f"Array1D{str(self.T)}"

class Array2DType(ArrayType):
    def __str__(self):
        return f"Array2D{str(self.T)}"

class OptionType(Type):
    """ Some functions can handle several of a finite set of types. For
    example, + works with both ints and arrays, but not functions

    Extends:
        Type
    """
    def __init__(self, *args):
        super(OptionType, self).__init__(args)

    def accepts(self, other):
        a = False
        for t in self.T: a = a or t.accepts(other)
        return a

    def __str__(self):
        return f"({' or '.join(str(t) for t in self.T)})"

    # make sure length and indexing still work
    def __len__(self):
        return len(self.T)
    def __getitem__(self, item):
        return tuple.__getitem__(self.T, item)

class TemplateType(Type):
    """ Some functions can handle multiple types. For example map has a return
    type which depends on the function being mapped. This template type is for
    that purpose

    Extends:
        Type
    """
    def __init__(self, T):
        super(TemplateType, self).__init__(T)

    def accepts(self, other):
        return True

    def __str__(self):
        return f"<{self.T}>"


class OptionTemplateType(TemplateType):
    """ Ok, we're getting complicated here, but bear with me. Templated
    functions are nice, but notall  templated functions can accept any
    argument types. For example, while "map" is a pure templated function, in
    the sense that it can work with any arguments that match the type template
    "+" can add arrays or ints, but not functions. So the OptionTemplateType
    is a TemplateType which only allows a finite set of Types to match the
    template.

    Extends:
        TemplateType
    """
    def __init__(self, T, options):
        self.T = T
        self.options = options

    def __str__(self):
        return f"<{self.T}>: ({' or '.join(str(t) for t in self.options)})"


if __name__ == '__main__':
    Color_T = Type("Color")
    colorarray_T = ArrayType(Color_T)

    # example of a function that counts the number of pixels of a certain color
    colorcount_T = FuncType((colorarray_T, Color_T), int)
    print("colorcount:", colorcount_T)

    # example of the type of map using a template type
    T1 = TemplateType(1)
    T2 = TemplateType(2)
    input_type = (ArrayType(T1), FuncType(T1, T2))
    output_type = ArrayType(T2)
    map_T = FuncType(input_type, output_type)
    print("map:", map_T)
