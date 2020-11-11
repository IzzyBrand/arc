import numpy as np
import operator as op
###############################################################################
# Types
###############################################################################
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

    def __str__(self):
        return f"ArrayOf{str(self.T)}"

class OptionType(Type):
    """ Some functions can handle several of a finite set of types. For
    example, + works with both ints and arrays, but not functions

    Extends:
        Type
    """
    def __init__(self, *args):
        super(OptionType, self).__init__(args)

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


###############################################################################
# Primitives and Environment
###############################################################################

class Primitive:
    def __init__(self, name, T):
        self.name = name
        self.T = T

    def __call__(self):
        return self

    def __str__(self):
        return self.name

typed_env = {'grid': np.zeros([3,3])}

class FuncCreator(Primitive):
    def __init__(self, name, T, f, env=typed_env):
        self.name = name
        self.T = T
        self.f = f

        if env is not None:
            env[self.name] = self

    def __call__(self, *args):
        return self.f(*args)

# this is a template type that only accepts ints or array
T1 = OptionTemplateType('T1', (int, np.ndarray))

# this is an OptionType that handles math between int and np.ndarray
binary_math_operator_type = OptionType(
    FuncType((int, int), int),
    FuncType((np.ndarray, int), np.ndarray),
    FuncType((int, np.ndarray), np.ndarray),
    FuncType((np.ndarray, np.ndarray), np.ndarray)
)

# create the default environment by adding symbols using FuncCreator

# arithmetic is easier
FuncCreator('+', binary_math_operator_type, op.add)
FuncCreator('-', binary_math_operator_type, op.sub)
FuncCreator('*', binary_math_operator_type, op.mul)
FuncCreator('sq', FuncType(T1, T1), np.square)

# logic is harder, because in the case of arrays, we get arrays,
# but in the case of ints we get bools.
FuncCreator('>', FuncType((T1, T1), bool), op.gt)
FuncCreator('>=', FuncType((T1, T1), bool), op.ge)
FuncCreator('==', FuncType((T1, T1), bool), op.eq)

# Array modification is much harder
# NOTE(izzy): we need to switch these to ArrayType, because some arrays are
# ints and others are bools, and they behave differently when used as slices
FuncCreator('zeros_like', FuncType(np.ndarray, np.ndarray), np.zeros_like)
FuncCreator('array_equal', FuncType((np.ndarray, np.ndarray), np.ndarray), op.eq)
FuncCreator('array_to_slice', FuncType(np.ndarray, slice), lambda x: x)




###############################################################################
# Example
###############################################################################

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
