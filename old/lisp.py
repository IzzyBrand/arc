"""6.009 Lab 8: carlae Interpreter Part 2"""

# REPLACE THIS FILE WITH YOUR lab.py FROM LAB 7, WHICH SHOULD BE THE STARTING
# POINT FOR THIS LAB.  YOU SHOULD ALSO ADD: import sys


import doctest
import sys


class EvaluationError(Exception):
    """
    Exception to be raised if there is an error during evaluation other than a
    NameError.
    """
    pass

class Fun:
    """
    Class for functions
    """

    def __init__(self, parameters, env, expression):
        self.parameters = parameters
        self.env = env
        self.expression = expression

    def get_params(self):
        return list(self.parameters)

    def get_body(self):
        return list(self.expression)

    def fooCall(self, args):
        #raise error if incorrect number of arguments passed
        if len(args) != len(self.parameters):
            raise EvaluationError
        #create new environment and set parents to current environment
        newEnv = Environment()
        newEnv.set_parents(self.env)

        #set parameters in new environmen equal to arguments
        for i in range(len(args)):
            newEnv[self.parameters[i]] = args[i]

        return evaluate(self.expression, newEnv)




class Environment:
    """
    class for environments
    """

    def __init__(self, values = {}):
        self.values = dict(values)
        self.parent = None

    def __contains__(self, name):
        if type(name) != str: return False #if invalid type
        #if it's in this, return true
        if name in self.values.keys():
            return True
        #look in parent environments
        if self.parent is not None:
            return self.parent.__contains__(name)
        #otherwise it's false
        return False

    def define(self, name, value):
        if type(name) != str: raise NameError

        self.values[name] = value

    def __setitem__(self, name, value):
        if type(name) != str: raise NameError

        self.values[name] = value

    def set_parents(self, parent):
        self.parent = parent

    def __getitem__(self, name):
        #check for value in current environment
        if name in self.values.keys():
            return self.values[name]
        #otherwise check parent environment
        if self.parent is not None:
            return self.parent.__getitem__(name)
        #if we still haven't found anything, raise a name error
        raise NameError

    def set(self, name, value):
        #set's variable with name to value if variable already exists
        if name in self.values.keys():
            self.values[name] = value
            return value

        if self.parent is not None:
            return self.parent.set(name, value)
        raise NameError


class Pair:
#class to represent cons cells
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def get_car(self):
        return self.car

    def get_cdr(self):
        return self.cdr



def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a carlae
                      expression
    """
    tokens = []
    comm = False
    exp = ''

    for c in source:
        #if we're currently reading comment
        if comm:
            #check for end of line
            if c == '\n':
                comm = False
            continue
        #otherwise if we're in an expression
        elif exp:
            #if we're at a special character marking end of expression, add expression but DON'T continue
            if c == '(' or c == ')' or c == '\n' or c == ';' or c == ' ':
                tokens.append(exp)
                exp = ''
            #otherwise add character to expression
            else:
                exp += c
                continue
        #add parentheses
        if c == '(' or c == ')':
            tokens.append(c)
            continue
        #start of comment
        if c == ';':
            comm = True
            continue
        #start of expression
        if not c == '\n' and not c == ' ':
            exp += c
    #if we have an unadded expression, add it
    if exp:
        tokens.append(exp)

    return tokens

def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    def parse_expression(index):
        """ Parses the expression in tokens with the given index
        """
        item = tokens[index]
        #return None marking end of parentheses
        if item == ')':
            return None, index + 1
        #if we have '(' we have new expression marked by list
        if item == '(':
            express = []
            #get next element
            nextExp, nextI = parse_expression(index + 1)
            le = len(tokens)
            #while we don't have a ')' and we haven't reached end...
            while(nextExp is not None and nextI < le):
                express.append(nextExp)
                nextExp, nextI = parse_expression(nextI)

            #if we didn't encounter a ')' but we stopped because we reached end, parentheses don't match
            if nextExp is not None: raise SyntaxError

            return express, nextI
        #checks if item is a number
        item = check(item)

        return item, index + 1


    parsedExp, nextInd = parse_expression(0)
    #if we have too many closed parentheses, raise an error
    if nextInd < len(tokens): raise SyntaxError
    return parsedExp

def check(inp):
    """Checks if input (which is a string) is a number
    """
    #try converting input to a number, otherwise keep it a string
    try:
        num = float(inp)
        if num % 1 == 0:
            num = int(num)
        return num

    except:
        return inp

carlae_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    '*': lambda args: prod(args),
    '/': lambda args: div(args),
    "#f": False,
    "#t": True,
    "not": lambda args: not args[0],
    "cons": lambda args: Pair(args[0], args[1]),
    "car": lambda args: args[0].get_car() if type(args[0]) == Pair else evalError(),
    "cdr": lambda args: args[0].get_cdr() if type(args[0]) == Pair else evalError(),
    "nil": None,
    "list": lambda args: nList(args),
    "length": lambda args: leng(args[0]),
    "elt-at-index": lambda args: find_item(args[0], args[1]),
    "concat": lambda args: concat(args),
    "map": lambda args: mapp(args[0], args[1]),
    "filter": lambda args: filt(args[0], args[1]),
    "reduce": lambda args: reduce(args[0], args[1], args[2]),
    "begin": lambda args: args[-1],
}

condits = {"=?": lambda a,b: a == b,
           "<": lambda a,b: a < b,
           ">": lambda a,b: a > b,
           "<=": lambda a,b: a <= b,
           ">=": lambda a,b: a >= b}



builtins = Environment(values = {**carlae_builtins, **condits})
globe = Environment()
globe.set_parents(builtins)

def reduce(fun, lis, init):
    if lis is None:
        return init

    if not type(lis) == Pair:
        raise EvaluationError

    return reduce(fun, lis.get_cdr(), call_fun(fun, [init, lis.get_car()]))


def filt(fun, lis):
    if lis is None:
        return None

    if not type(lis) == Pair:
        raise EvaluationError

    v = call_fun(fun, [lis.get_car()])
    if v:
        return Pair(lis.get_car(), filt(fun, lis.get_cdr()))

    return filt(fun, lis.get_cdr())

def mapp(fun, lis):

    if lis is None:
        return None

    if not type(lis) == Pair:
        raise EvaluationError

    return Pair(call_fun(fun, [lis.get_car()]), mapp(fun, lis.get_cdr()))

def call_fun(foo, args):
    if foo in carlae_builtins.values():
        return foo(args)

    return foo.fooCall(args)

def concat(args):

    if args == []:
        return None

    if args[0] is None:
        return concat(args[1:])

    if not type(args[0]) == Pair:
        raise EvaluationError

    if args[0].get_cdr() is None:
        return Pair(args[0].get_car(), concat(args[1:]))

    return Pair(args[0].get_car(), concat([args[0].get_cdr()] + args[1:]))



def find_item(Lis, ind):

    if not type(Lis) == Pair or ind < 0:
        raise EvaluationError

    if ind == 0:
        return Lis.get_car()

    return find_item(Lis.get_cdr(), ind - 1)

def leng(args):

    if args is None:
        return 0

    if not type(args) == Pair:
        raise EvaluationError

    return 1 + leng(args.get_cdr())


def nList(args):

    if len(args) == 0:
        return None

    return Pair(args[0], nList(args[1:]))

def evalError():
    raise EvaluationError

def prod(nums):

    val = nums[0]
    for num in nums[1:]:
        val *= num

    return val

def div(nums):

    val = nums[0]
    for num in nums[1:]:
        val /= num

    return val


def evaluate(tree, env = None):
    """
    Evaluate the given syntax tree according to the rules of the carlae
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    if tree is None or type(tree) is Pair:
        return tree

    #set env
    if env is None:
        env = Environment()
        env.set_parents(builtins)

    #if tree isn't a list, return it if it's an int or float.
    if type(tree) in (int, float):
        return tree
    #if it's a string, return it's value
    if type(tree) == str:

        return env[tree]

    if tree == []:
        return []

    #if the first element is keyword define
    if tree[0] == "define":
        #make sure it's correct length
        if len(tree) > 3:
            raise EvaluationError
        #if we have a special function definition, reorganize it
        if type(tree[1]) == list:
            params = tree[1][1:]
            name = tree[1][0]
            tree[1] = name
            definition = ["lambda", list(params), list(tree[2])]
            tree[2] = list(definition)

        val = tree[2]
        if type(val) not in (float, int):
            val = evaluate(val, env)
       #define it in environment
        env[tree[1]] = val
        return val

    #if keyword lambda, make function object
    if tree[0] == "lambda":
        return Fun(list(tree[1]), env, tree[2])

    #if it's an and/or
    if tree[0] in ("and", "or"):
        #go through each conditional and check it
        for cond in tree[1:]:
            v = evaluate(cond, env)
            if tree[0] == "and":
                if not v: return False
            elif tree[0] == "or":
                if v: return True
        #if and and all expressions were true
        if tree[0] == "and":
            return True
        #if or and all expressions were False
        return False

    #if statement
    if tree[0] == "if":
        if evaluate(tree[1], env):
            return evaluate(tree[2], env)
        return evaluate(tree[3], env)

    #let
    if tree[0] == "let":
        pars = dict()

        for exp in tree[1]:
            pars[exp[0]] = evaluate(exp[1], env)

        newEnv = Environment(values = dict(pars))
        newEnv.set_parents(env)

        return evaluate(tree[2], newEnv)

    #set BANG!
    if tree[0] == "set!":
        val = evaluate(tree[2], env)
        return env.set(tree[1], val)


    new = []
    #if we're here, we have a function call, so we want to evaluate each element
    for el in tree:
        new.append(evaluate(el,env))

    element = new[0]

    if type(element) in (float, int):
        raise EvaluationError

    #if it's a conditional
    if element in condits.values():
        #go through each element and evaluate conditional expression
        for i in range(1, len(new) - 1):
            if not element(new[i], new[i + 1]):
                return False
        return True

    #if it's a builtin
    if element in carlae_builtins.values():
        return element(new[1:])

    #otherwise evaluate function
    if type(element) == Fun:

        args = [evaluate(i, env) if type(i) != Fun else i for i in new[1:]]
        return element.fooCall(args)



def REPL():
    """REPL for user interaction
    """
    #get input
    inp = input("in> ")
    #while not QUIT
    while(inp != "QUIT"):

        try:
            #tokenize, parse, and evaluate input then print output
            t = tokenize(inp)
            p = parse(t)
            out = evaluate(p, globe)
            print("out>",out)

        except ValueError:
            print("ValueError")

        except NameError:
            print("NameError")

        except EvaluationError:
            print("EvaluationError")

        except TypeError:
            print("TypeError")

        except:
            print("Error in computing last line")

        inp = input("in> ")

def result_and_env(tree, env = None):
    if env is None:
        env = Environment()
        env.set_parents(builtins)
    res = evaluate(tree, env)

    return res, env

def evaluate_file(file, env = None):
    """Returns result of evaluating a file in Carlae
    """
    f = open(file, "r")
    toStr = f.read()
    t = tokenize(toStr)
    p = parse(t)
    return evaluate(p, env)



if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()

    for file in sys.argv[1:]:
        evaluate_file(file, globe)

   # evaluate_file("checkoff.txt", globe)

    REPL() 
