import numpy as np

from language.ast import Identifier, Apply, Lambda, Let, Letrec
from language.util import is_integer_literal, is_color_literal, ParseError


def get_identifier(name, env):
    """get the value of an identifier"""

    if name in env:
        return env.find(x)[x]
    elif is_integer_literal(name):
        return int(name)
    elif is_color_literal(name):
        return name # NOTE(izzy): decide how to represent colors? probably int
    else:
        raise ParseError(f"Undefined symbol {name}")


class NestedEnv(dict):
    def __init__(self, dictionary, outer=None):
        self.update(dictionary)
        self.outer = outer

    def find(self, var):
        if (var in self):
            return self
        elif self.outer is not None:
            return self.outer.find(var)
        else:
            print(f'Failed to find {var} in {self}')

    def __str__(self):
        return '{'+',\t'.join([f'{str(k)}: {str(v)}' for k,v \
            in zip(self.keys(), self.values())]) + '}'


# NOTE(izzy): the semantics of functions are defined with currying.
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

class Procedure(object):
    """A user-defined Scheme procedure."""
    def __init__(self, param, body, env, func_string=None):
        self.func_string=func_string
        self.param, self.body, self.env = param, body, env

    def __call__(self, arg):
        # create a new environment with the argument bound to input
        new_env = Env({self.param: arg}, outer=self.env)
        # and evaluate the procedure in the new environment
        return eval(self.body, new_env)

    def __str__(self):
        f"(fn {self.param} => {self.body})"


def eval(x, env):
    # if the environment is a regular dictionary, wrap it in a class
    # which supports nested dictionaries (for local scoping)
    if not isinstance(env, NestedEnv): env = NestedEnv(env)

    if isinstance(x, Identifier):
        return get_identifier(name, env)

    elif is instance(x, Apply):
        prog = eval(x.fn, env)
        arg = eval(x.arg, env)
        return proc(arg)

    elif is instance(x, Lambda):
        return Procedure(x.v, x.body)

    elif is instance(x, Let):
        pass

    elif is instance(x, Letrec):
        pass