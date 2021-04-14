from old_types.type_system import *

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
T_slice2D = Type('slice2D')

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
    FuncType((Array1DType(T1), T_slice), Array1DType(T1)), # slice a 1D array
    FuncType((Array2DType(T1), T_slice), Array2DType(T1)), # slice a 2D array
    FuncType((Array1DType(T1), T_int), T1),                # integer index 1D
    FuncType((Array2DType(T1), T_int), Array1DType(T1)),   # integer index 2D
    FuncType((Array1DType(T1), Array1DType(T_int)), Array1DType(T1)), # array index 1D
    FuncType((Array2DType(T1), Array1DType(T_int)), Array2DType(T1))  # array index 2D
)

array_assign_type = OptionType(
    FuncType((Array1DType(T1), T_slice, Array1DType(T1)), Array1DType(T1)), # set slice to array
    FuncType((Array1DType(T1), T_slice, T1), Array1DType(T1)),              # set slice to value
    FuncType((Array1DType(T1), T_int, T1), Array1DType(T1)),                # set index to value

    FuncType((Array2DType(T1), T_slice, Array2DType(T1)), Array2DType(T1)), # set slice to array
    FuncType((Array2DType(T1), T_slice, T1), Array2DType(T1)),              # set slice to value
    FuncType((Array2DType(T1), T_int, Array1DType(T1)), Array2DType(T1)),   # set row to array
    FuncType((Array2DType(T1), T_int, T1), Array2DType(T1)),                # set row to value
    FuncType((Array2DType(T1), T_slice2D, T1), Array2DType(T1)),            # set mask to value
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
FuncCreator('index', index_type, lambda a, x: a[x])
FuncCreator('array_to_slice', FuncType(Array1DType(OptionType(T_int, T_bool)), T_slice), lambda x: x)
FuncCreator('array_to_slice2D', FuncType(Array2DType(T_bool), T_slice2D), lambda x: x)

# array functions
FuncCreator('zeros_like', FuncType(ArrayType(T1), ArrayType(T1)), np.zeros_like)
FuncCreator('transpose', FuncType(Array2DType(T1), Array2DType(T1)), np.transpose)


# Array modification is much harder
# NOTE(izzy): we need to switch these to ArrayType, because some arrays are
# ints and others are bools, and they behave differently when used as slices
# FuncCreator('zeros_like', FuncType(np.ndarray, np.ndarray), np.zeros_like)
# FuncCreator('array_equal', FuncType((np.ndarray, np.ndarray), np.ndarray), op.eq)