import numpy as np
from language.types import *

type_env = {}
eval_env = {}

def make(name, func, functype):
    """adds a command to the type and evaluation environments"""
    eval_env[name] = func
    type_env[name] = functype

# create some type variables used to define polymorphic types
T0 = TypeVariable()
T1 = TypeVariable()

T0_array = TypeOperator('array', [T0])
T1_array = TypeOperator('array', [T1])
Integer_array = TypeOperator('array', [Integer])

T0_array_2 = TypeOperator('array', [T0_array])
T1_array_2 = TypeOperator('array', [T1_array])
Integer_array_2 = TypeOperator('array', [Integer_array])


# NOTE(izzy): the semantics of these functions are defined with currying.
#
#     Not curried: fn (x, y) => z
#
#     Curried: fn x => (fn y => z)
#
# I did this because the structure of the type-checker assumes curried
# functions, and I wanted the structure of the evalution to match.
# At present, I'm not sure what impact this will have on search perormance,
# but we might want to move away from currying in the future. This will
# require changes to the evaluation, and to the language definition.
# I'm not sure how easy it will be to type-check non-curried functions,
# so we might want write a tool that curries an AST


make("pred",
    lambda x: x - 1,
    Function(Integer, Integer))

make("plus",
    lambda x: lambda y: x + y,
    curried_type(Integer, Integer, Integer))

make("times",
    lambda x: lambda y: x * y,
    curried_type(Integer, Integer, Integer))

make("eq",
    lambda x: lambda y: x == y,
    curried_type(T0, T0, Bool))

make("index",
    lambda a: lambda i: a[i],
    curried_type(T0_array, Integer, T0))

make("trans",
    lambda a: a.T,
    Function(T0_array_2, T0_array_2))

# NOTE(izzy): here we run into a minor problem with the current type system,
# because of the way we're representing 2D arrays as array(array(T)).
# Numpy's zeros_like function works on 2D or 1D arrays. Ideally the type
# of this function would be something like array(T) -> array(int).
# If we did that, imagine calling zeros_like on array(array(T)) --
# for consistency that would have to return an array(int), so it
# would have dropped a dimension from the input 2D array
make("zeros_like",
    lambda a: np.zeros_like(a, dtype=int),
    Function(T0_array, Integer_array))

make("cond",
    lambda pred: lambda x: lambda y: x if pred else y,
    curried_type(Bool, T0, T0, T0))

# NOTE(izzy): higher order functions (ones that take a func as an arg)
# may need to use use a diffent means of evaluation. Instead of
#
#     f(x)
#
# we might need
#
#     Apply(f, x)
#
# This might cause a circular dependency because we are importing from ast

T_map = Function(T0, T1)
make("map",
    lambda f: lambda a: np.array([f(x) for x in a]),
    curried_type(T_map, T0_array, T1_array))

T_filter = Function(T0, Bool)
make("filter",
    lambda f: lambda a: np.array([x for x in a if f(x)]),
    curried_type(T_filter, T0_array, T0_array))


if __name__ == "__main__":
    for k, v in type_env.items():
        print(f"{k}:\t{v}")
