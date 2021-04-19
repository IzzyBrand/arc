import numpy as np

from language.ast import Identifier, Apply, Lambda, Let, Letrec
from language.util import is_integer_literal, is_color_literal, ParseError


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


class Procedure(object):
    """A user-defined Scheme procedure."""
    def __init__(self, parms, body, env, func_string=None):
        self.func_string=func_string
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        new_env = Env(zip(self.parms, args), outer=self.env)
        return eval(self.body, new_env)

    def __str__(self):
        return self.func_string

def get_identifier(name, env):
    """get the value of an identifier"""

    if name in env:
        return env.find(x)[x]
    elif is_integer_literal(name):
        return int(name)
    elif is_color_literal(name):
        return name # NOTE(izzy): decide how to represent this? probably int
    else:
        raise ParseError(f"Undefined symbol {name}")

def eval(x, env):
    # if the environment is a regular dictionary, wrap it in a class
    # which supports nested dictionaries (for local scoping)
    if not isinstance(env, NestedEnv): env = NestedEnv(env)

    if isinstance(x, Identifier):
        return get_identifier(name, env)

    elif is instance(x, Apply):
        pass

    elif is instance(x, Lambda):
        pass

    elif is instance(x, Let):
        pass

    elif is instance(x, Letrec):
        pass