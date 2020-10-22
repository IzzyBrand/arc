################ Lispy: Scheme Interpreter in Python

## (c) Peter Norvig, 2010-16; See http://norvig.com/lispy.html

from __future__ import division
import operator as op
import numpy as np
from arc_lisp_env import extended_env
from arc_lispUI_env import UI_env

################ Types

Symbol = str          # A Lisp Symbol is implemented as a Python str
List   = list         # A Lisp List is implemented as a Python list
Number = (int, float) # A Lisp Number is implemented as a Python int or float

################ Parsing: parse, tokenize, and read_from_tokens

def parse(program):
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))

def tokenize(s):
    "Convert a string into a list of tokens."
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from_tokens(tokens):
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    "Numbers become numbers; every other token is a ."
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

################ Environments

def standard_env():
    "An environment with some Scheme standard procedures."
    env = Env()
    # NOTE(izzy): keep the top-level env small
    # env.update(vars(math)) # sin, cos, sqrt, pi, ...
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv,
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '==':op.eq,

        # NOTE(izzy): keep the language small. we can add these as needed
        # 'abs':     abs,
        # 'append':  op.add,
        # 'apply':   apply,
        # 'begin':   lambda *x: x[-1],
        # 'car':     lambda x: x[0],
        # 'cdr':     lambda x: x[1:],
        # 'cons':    lambda x,y: [x] + y,
        # 'eq?':     op.is_,
        # 'equal?':  op.eq,
        # 'length':  len,
        # 'list':    lambda *x: list(x),
        # 'list?':   lambda x: isinstance(x,list),
        # 'map':     map,
        # 'max':     max,
        # 'min':     min,
        # 'not':     op.not_,
        # 'null?':   lambda x: x == [],
        # 'number?': lambda x: isinstance(x, Number),
        # 'procedure?': callable,
        # 'round':   round,
        # 'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        "Find the innermost Env where var appears."
        return self if (var in self) else self.outer.find(var)

    def get(self, var):
        return self[var] if (var in self) else (self.outer.get(var) if self.outer is not None else var)

global_env = standard_env()
global_env.update(extended_env)
global_env.update(UI_env)

################ Interaction: A REPL

def repl(prompt='lis.py> '):
    "A prompt-read-eval-print loop."
    while True:
        inp = input(prompt)
        if inp == "quit":
            break
        val = eval(parse(inp))
        if val is not None:
            print(lispstr(val))

def lispstr(exp):
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, List):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)

################ Procedures

class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args):
        return eval(self.body, Env(self.parms, args, self.env))

################ eval

def eval(x, env=global_env):
    "Evaluate an expression in an environment."
    # NOTE(izzy): all good
    if isinstance(x, Symbol):      # variable reference
        return env.get(x)

    # NOTE(izzy): all good
    elif not isinstance(x, List):  # constant literal
        return x

    # NOTE(izzy): no need for quotations
    # elif x[0] == 'quote':          # (quote exp)
    #     (_, exp) = x
    #     return exp

    # NOTE(izzy): all good
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env)

    # NOTE(izzy): Previously, define mutated the toplevel environment
    # I think we might want to change define to define a variable in a
    # local scope. For reference here is the old version
    #
    elif x[0] == 'define':         # (define var exp)
        (_, var, exp) = x
        env[var] = eval(exp, env)
        return(eval(var, env))
    #
    # and here is the new version
    # elif x[0] == 'define':         # (define var exp body)
    #
    #     (_, var, exp) = x[:3]
    #     new_env = Env([var], [eval(exp, env)], outer=env)
    #     if len(x) == 3:
    #         body = parse(input('inp body> '))
    #     elif len(x) == 4:
    #         body = x[3]
    #     return eval(body, env=new_env)

    # NOTE(izzy): no mutable variables
    # elif x[0] == 'set!':           # (set! var exp)
    #     (_, var, exp) = x
    #     env.find(var)[var] = eval(exp, env)

    # NOTE(izzy): all good
    elif x[0] == 'lambda':         # (lambda (var...) body)
        (_, parms, body) = x
        return Procedure(parms, body, env)

    # NOTE(izzy): all good, but I added a case to allow array indexing
    else:                          # (proc arg...)
        proc = eval(x[0], env)
        args = [eval(exp, env) for exp in x[1:]]
        if isinstance(proc, (np.ndarray, tuple)): return np.copy(proc[tuple(args)])
        else: return proc(*args)

if __name__ == '__main__':
    repl()
