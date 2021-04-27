from copy import deepcopy
import numpy as np

from language.ast import Identifier, Apply, Lambda, Let, Letrec
from language.util import is_integer_literal, is_color_literal, ParseError


def get_identifier(name, env):
    """get the value of an identifier"""

    val = env.get(name)
    if val != None:
        return val
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
            return None

    def get(self, var):
        env = self.find(var)
        if env is None:
            return None
        else:
            return env[var]

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
    def __init__(self, param, body, env):
        self.param, self.body, self.env = param, body, env

    def __call__(self, arg):
        # create a new environment with the argument bound to input
        new_env = NestedEnv({self.param: arg}, outer=self.env)
        # and evaluate the procedure in the new environment
        return eval(self.body, new_env)

    def __str__(self):
        return f"(fn {self.param} => {self.body})"

def eval_cond(x, env):
    """handles AST with Apply(Identifier('cond'), ...) at the root

    we need to handle this outside of the default eval Apply because we only
    want to compute the selected branch of an if statement (lazy eval). If we
    don't do this, we can't use cond to terminate a recursive function.
    """
    try:
        pred, x, y = x.args
    except ValueError:
        raise ParseError(f"Wrong number of arguments to cond:\n{str(x)}")
    return eval(x, env) if eval(pred, env) else eval(y, env)


def get_special_eval(x):
    """non-standard evaluation (particularly for higher order functions"""
    if isinstance(x, Apply) and isinstance(x.fn, Identifier) and x.fn.name == "cond":
        return eval_cond
    else:
        return None


def eval(x, env):
    # if the environment is a regular dictionary, wrap it in a class
    # which supports nested dictionaries (for local scoping)
    if not isinstance(env, NestedEnv): env = NestedEnv(env)

    # some higher-order-functions require a special evaluation structure
    special_eval = get_special_eval(x)
    if special_eval is not None:
        return special_eval(x, env)

    elif isinstance(x, Identifier):
        return get_identifier(x.name, env)

    elif isinstance(x, Apply):
        proc = eval(x.fn, env)
        args = [eval(a, env) for a in x.args]
        return proc(*args)

    elif isinstance(x, Lambda):
        return Procedure(x.v, x.body, env)

    elif isinstance(x, Let):
        # NOTE(izzy): this implementation is more efficient the Letrec, because
        # it doesn't copy the environment, but it doesn't support recursion.
        # The reason recursion won't work is because to create the new
        # environment which we pass to the body, we need to `exp`, the
        # variable to be bound in the new environment. In the case where we are
        # defining a recursive function, exp needs access to itself
        var = x.v
        val = eval(x.defn, env)
        new_env = NestedEnv({var: val}, outer=env)
        return eval(x.body, env=new_env)

    elif isinstance(x, Letrec):
        # NOTE(izzy): this implementation does support recursion, but it copies
        # the environment every time which isn't great
        new_env = deepcopy(env)
        var = x.v
        val = eval(x.defn, new_env)
        new_env[var] = val
        return eval(x.body, env=new_env)
