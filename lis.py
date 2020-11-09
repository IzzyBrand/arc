""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""
## Inspired by Peter Norvig, 2010-16; See http://norvig.com/lispy.html

from __future__ import division
from copy import deepcopy
import numpy as np
import sys
from arc_lisp_env import extended_env
from type_system import typed_env, type_check

################ Parsing: parse, tokenize, and read_from_tokens

def parse(program):
    # Read a Scheme expression from a string.
    return read_from_tokens(tokenize(program))

def tokenize(s):
    # Convert a string into a list of tokens.
    return s.replace('(',' ( ').replace(')',' ) ').split()

def read_from_tokens(tokens):
    # Read an expression from a sequence of tokens.
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
    try: return int(token)
    except ValueError: return token

################ Environments

class Env(dict):
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

    def get(self, var):
        return self[var] if (var in self) else (self.outer.get(var) if self.outer is not None else var)

    # def __str__(self):
    #     return str([(str(k), str(v)) for k,v in zip(self.keys(), self.values())])


global_env = Env(extended_env)


################ Interaction: A REPL

def repl(prompt='lis.py> ', env=global_env):
    "A prompt-read-eval-print loop."

    for file in sys.argv[1:]:
        eval_file(file, repl = True, display = False)

    while True:
        inp = input(prompt)
        if inp == "quit":
            break
        x = parse(inp)

        pass_type_check, return_type, type_tree = type_check(x, env)
        print(f'Type check? {pass_type_check}\tType {return_type}')

        if pass_type_check:
            val = eval(x, repl=False, env=env)
            if val is not None:
                print(lispstr(val))

def lispstr(exp):
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)

################ Procedures

class Procedure(object):
    "A user-defined Scheme procedure."
    def __init__(self, parms, body, env, func_string=None):
        self.func_string=func_string
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args):
        new_env = Env(zip(self.parms, args), outer=self.env)
        return eval(self.body, new_env)
    def __str__(self):
        return self.func_string

################ eval

def eval(x, env=global_env, repl=False):
    "Evaluate an expression in an environment."

    # print('Eval', x)
    # NOTE(izzy): all good
    if isinstance(x, str):      # variable reference
        if repl: ans =  env.get(x)
        else: ans =  env.find(x)[x]
        return ans

    # NOTE(izzy): all good
    elif not isinstance(x, list):  # constant literal
        return x

    # NOTE(izzy): no need for quotations
    # elif x[0] == 'quote':          # (quote exp)
    #     (_, exp) = x
    #     return exp

    # NOTE(izzy): all good
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return eval(exp, env, repl = repl)

    # NOTE(izzy): Previously, define mutated the toplevel environment
    # I think we might want to change define to define a variable in a
    # local scope.
    elif x[0] == 'define':         # (define var exp body)

        # NOTE(izzy): this implementation is more efficient, because it doesn't
        # but doesn't copy the environment, but it doesn't support recursion.
        # The reason recursion won't work, is because to create the new
        # environment which we pass to the body, we need to evaluate `exp`, the
        # variable to be bound in the new environment. In the case where we are
        # defining a recursive function, exp needs access to itself
        # (_, var, exp, body) = x
        # new_env = Env([var], [eval(exp, env, repl = repl)], outer=env)
        # return eval(body, env=new_env, repl = repl)

        # NOTE(izzy): this implementation does support recursion, but it copies
        # the environment every time which isn't great
        (_, var, exp, body) = x
        new_env = deepcopy(env)
        new_env[var] = eval(exp, new_env, repl = repl)

        return eval(body, env=new_env, repl = repl)

    # NOTE(izzy): only used the REPL. Modifies the environment
    elif x[0] == 'ordain':         # (ordain var exp)
        (_, var, exp) = x
        env[var] = eval(exp, env, repl = repl)
        return(eval(var, env, repl = repl))

    # NOTE(izzy): all good
    elif x[0] == 'lambda':         # (lambda (var...) body)
        (_, parms, body) = x
        return Procedure(parms, body, env, func_string=str(x))

    # NOTE(izzy): all good, but I added a case to allow array indexing
    else:                          # (proc arg...)
        try:
            proc = eval(x[0], env, repl = repl)
            args = [eval(exp, env, repl = repl) for exp in x[1:]]
            if isinstance(proc, np.ndarray): return np.copy(proc[tuple(args)])
            elif isinstance(proc, tuple): return proc[args[0]]
            elif isinstance(proc, (int, str)): return proc
            else: return proc(*args)

        except Exception as E:
            print(E, '\n')
            # for debug purposes, if we get an error recur up the environment
            # and dump the contents to the terminal before exiting
            env_counter = 0
            while env is not None:
                print('Environment', env_counter, env)
                env = env.outer
                env_counter += 1

            sys.exit(1)


def eval_file(filename, env=global_env, repl = False, display = False):
    f = open(filename, 'r')
    for line in f:
        if line[0] == "(":
            try:
                val = eval(parse(line), env = env, repl = repl)
                if print: print(val)
            except:
                print("Error on line: " + line)

if __name__ == '__main__':
    env = Env(typed_env)

    repl(env=env)
