from type_system import *

typed_env = {'igrid': np.random.randint(10, size=[3,3]),
             'bgrid': np.random.randint(1, size=[3,3], dtype=bool)}


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
Tif = OptionTemplateType('Tif', (int, bool))
# T1 = OptionTemplateType('T1', (int, np.ndarray))

# this is an OptionType that handles math between int and np.ndarray
binary_math_operator_type = OptionType(
    FuncType((int, int), int),
    FuncType((ArrayType(int), int), ArrayType(int)),
    FuncType((int, ArrayType(int)), ArrayType(int)),
    FuncType((ArrayType(int), ArrayType(int)), ArrayType(int))
)

# create the default environment by adding symbols using FuncCreator

# arithmetic is easier
FuncCreator('+', binary_math_operator_type, op.add)
FuncCreator('-', binary_math_operator_type, op.sub)
FuncCreator('*', binary_math_operator_type, op.mul)

# FuncCreator('sq', FuncType(T1, T1), np.square)

# logic is harder, because in the case of arrays, we get arrays,
# but in the case of ints we get bools.
# FuncCreator('>', FuncType((T1, T1), bool), op.gt)
# FuncCreator('>=', FuncType((T1, T1), bool), op.ge)
# FuncCreator('==', FuncType((T1, T1), bool), op.eq)

# Array modification is much harder
# NOTE(izzy): we need to switch these to ArrayType, because some arrays are
# ints and others are bools, and they behave differently when used as slices
# FuncCreator('zeros_like', FuncType(np.ndarray, np.ndarray), np.zeros_like)
# FuncCreator('array_equal', FuncType((np.ndarray, np.ndarray), np.ndarray), op.eq)
# FuncCreator('array_to_slice', FuncType(np.ndarray, slice), lambda x: x)