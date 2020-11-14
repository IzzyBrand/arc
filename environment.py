from type_system import *

def make_slice(start, end):
    if end == 0: end = None
    return slice(start, end)

typed_env = {}

class FuncCreator(Primitive):
    def __init__(self, name, T, f, env=typed_env):
        self.name = name
        self.T = T
        self.f = f

        if env is not None:
            env[self.name] = self

    def __call__(self, *args):
        return self.f(*args)

T1 = TemplateType('T1')
T_int = Type('int')
T_bool = Type('bool')
T_slice = Type('slice')

# this is an OptionType that handles math between int and np.ndarray
binary_math_operator_type = OptionType(
    FuncType((T_int, T_int), T_int),
    FuncType((Array1DType(T_int), T_int), Array1DType(T_int)),
    FuncType((Array2DType(T_int), T_int), Array2DType(T_int)),
    FuncType((T_int, Array1DType(T_int)), Array1DType(T_int)),
    FuncType((T_int, Array2DType(T_int)), Array2DType(T_int)),
    FuncType((Array1DType(T_int), Array1DType(T_int)), Array1DType(T_int)),
    FuncType((Array2DType(T_int), Array2DType(T_int)), Array2DType(T_int))
)

binary_math_comparator_type = OptionType(
    FuncType((T_int, T_int), T_bool),
    FuncType((Array1DType(T_int), T_int), Array1DType(T_bool)),
    FuncType((Array2DType(T_int), T_int), Array2DType(T_bool)),
    FuncType((T_int, Array1DType(T_int)), Array1DType(T_bool)),
    FuncType((T_int, Array2DType(T_int)), Array2DType(T_bool)),
    FuncType((Array1DType(T_int), Array1DType(T_int)), Array1DType(T_bool)),
    FuncType((Array2DType(T_int), Array2DType(T_int)), Array2DType(T_bool))
)

index_type = OptionType(
    FuncType((ArrayType(T1), T_slice), ArrayType(T1)),
    FuncType((Array1DType(T1), int), T1),
    FuncType((Array2DType(T1), int), Array1DType(T1))
)


# create the default environment by adding symbols using FuncCreator

# arithmetic
FuncCreator('+', binary_math_operator_type, op.add)
FuncCreator('-', binary_math_operator_type, op.sub)
FuncCreator('*', binary_math_operator_type, op.mul)
FuncCreator('>', binary_math_comparator_type, op.gt)
FuncCreator('>=', binary_math_comparator_type, op.ge)
FuncCreator('==', binary_math_comparator_type, op.eq)

# array indexing
FuncCreator('make_slice', FuncType((T_int, T_int), T_slice), make_slice)








# Array modification is much harder
# NOTE(izzy): we need to switch these to ArrayType, because some arrays are
# ints and others are bools, and they behave differently when used as slices
# FuncCreator('zeros_like', FuncType(np.ndarray, np.ndarray), np.zeros_like)
# FuncCreator('array_equal', FuncType((np.ndarray, np.ndarray), np.ndarray), op.eq)
# FuncCreator('array_to_slice', FuncType(np.ndarray, slice), lambda x: x)