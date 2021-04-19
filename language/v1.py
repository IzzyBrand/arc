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


make("pred",
    lambda x: x - 1,
    Function(Integer, Integer))

make("plus",
    lambda x, y: x + y,
    curried_function(Integer, Integer, Integer))

make("times",
    lambda x, y: x * y,
    curried_function(Integer, Integer, Integer))

make("eq",
    lambda x, y: x == y,
    curried_function(T0, T0, Bool))

make("index",
    lambda a, i: a[i],
    curried_function(T0_array, Integer, T0))

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
    lambda pred, x, y: x if pred else y,
    curried_function(Bool, T0, T0, T0))

T_map = Function(T0, T1)
make("map",
    lambda f, a: np.array([f(x) for x in a]),
    curried_function(T_map, T0_array, T1_array))

T_filter = Function(T0, Bool)
make("filter",
    lambda f, a: np.array([x for x in a if f(x)]),
    curried_function(T_filter, T0_array, T0_array))

if __name__ == "__main__":
    for k, v in type_env.items():
        print(f"{k}:\t{v}")
