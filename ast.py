from base_types import FuncType


class AST(list):
    """ This AST class serves as an alternative to the typical nested-
    lists representation of LISP's abstract syntax tree.

    The advantage of implementing this with classes is that we can provide a
    typechecking function that stores the result of the typechecking
    computation for each subtree.
    """

    # all of this stuff is just necessary to make sure that when we slice an
    # AST, it returns an AST instead of a regular list
    def __getslice__(self,i,j):
        return AST(list.__getslice__(self, i, j))
    def __add__(self,other):
        return AST(list.__add__(self,other))
    def __mul__(self,other):
        return AST(list.__mul__(self,other))
    def __add__(self, rhs):
        return AST(list.__add__(self, rhs))
    def __getitem__(self, item):
        result = list.__getitem__(self, item)
        if isinstance(result, str): return result
        try: return AST(result)
        except TypeError: return result

    def type_check(self):
        """ Computes the type of this tree and all of it's children.
        
        Returns:
            bool -- False if typecheck fails in this tree or the children. 
                    True otherwise.
        """

        # NOTE(izzy):
        # * might need to add an environment which gets passed around during typecheck?
        # * We might need to allow things other than FuncType to have children to allow 
        #   array and tuple slicing

        # type check the node and the children. fail if they fail
        for child in self:
            if not child.type_check():
                return False

        # if there are no children, then the node is the type of this tree:
        if len(self[1:]) == 0:
            self.type = self[0].type
            return True

        # if we have chilren, then they are the arguments to the node
        
        # check that the node is a FuncType, and error if not
        if not isinstance(self[0].type, FuncType):
            print(f'{str(self[0].type)} does not accept arguments. Given:')
            for c in self[1:]:
                print(f'\t{str(c.type)}')
            return False

        # check that we have the correct number of arguments
        if len(self[1:]) != len(self[0].type[0]):
            print(f'Incorrect number of arguments to {str(self[0].type)}. Received:')
            for c in self[1:]:
                print(f'\t{str(c.type)}')
            return False
        
        # and check that each argument is of the correct type
        for i, (arg_type, given) in enumerate(zip(self[0].type[1], self[1:])):
            if arg_type != given.type:
                print(f'Incorrect argument #{i} to f{str(self[0].type)}.')
                print(f'\tExpected {str(arg_type)}. Received {str(given.type)}')
                return False

        # if we pass all of those checks, then this subtree returns the return type
        # of the node
        self.type = self[0].type[1]
        return True

# class Base:

#     def __init__(self, name, type, func=None):
#         self.name = name
#         self.type = type


#     def eval(self, args, env):
#         """ This is the base_case for eval
#         """
#         return self

#     def type_check(self):
#         """ This is the base case for type_check on Tree. Single nodes always pass
#         the typecheck because their are no subtrees that could fail.

#         Note that subtypes of Symbol must specify the self.type field
#         """
#         return True

# class Int(Base):
#     def __init__(self, token):
#         self.val = int(token)
#         self.type = Int_T

#     # def eval(self, args, env):
#     #     return self.val

# class Symbol(Base):
#     def __init__(self, token):
#         self.name = token

#     # def eval(self, args, env):
#     #     return env[self.name]

# class BinaryIntegerOperator(Base):
#     def __init__(self, f):
#         self.f = f
#         self.type = FuncType((Int_T, Int_T), Int_T)

#     def eval(self, args, env):
#         return self.f(*args)

# class BinaryIntegerPredicate(Base):
#     def __init__(self, f):
#         self.f = f
#         self.type = FuncType((Int_T, Int_T), Bool_T)

#     def eval(self, args, env):
#         return self.f(*args)


# test_env = {
#     '+': BinaryIntegerOperator(op.add),
#     '*': BinaryIntegerOperator(op.mul),
#     '/': BinaryIntegerOperator(op.truediv),
#     '-': BinaryIntegerOperator(op.sub),
#     '>': BinaryIntegerPredicate(op.gt),
#     '>=': BinaryIntegerPredicate(op.ge),
#     '==': BinaryIntegerPredicate(op.eq),
# }


                

# def eval(tree, env=global_env, repl=False):
#     "Evaluate an expression in an environment."

#     # print('Eval', x)
#     # NOTE(izzy): all good
#     if isinstance(x, Symbol):      # variable reference
#         return env.find(x)[x]

#     # NOTE(izzy): all good
#     elif not isinstance(x, Tree):  # constant literal
#         return x

#     # NOTE(izzy): no need for quotations
#     # elif x[0] == 'quote':          # (quote exp)
#     #     (_, exp) = x
#     #     return exp

#     # NOTE(izzy): all good
#     elif x[0] == 'if':             # (if test conseq alt)
#         (_, test, conseq, alt) = x
#         exp = (conseq if eval(test, env) else alt)
#         return eval(exp, env, repl = repl)

#     # NOTE(izzy): Previously, define mutated the toplevel environment
#     # I think we might want to change define to define a variable in a
#     # local scope.
#     elif x[0] == 'define':         # (define var exp body)

#         # NOTE(izzy): this implementation is more efficient, because it doesn't
#         # but doesn't copy the environment, but it doesn't support recursion.
#         # The reason recursion won't work, is because to create the new
#         # environment which we pass to the body, we need to evaluate `exp`, the
#         # variable to be bound in the new environment. In the case where we are
#         # defining a recursive function, exp needs access to itself
#         # (_, var, exp, body) = x
#         # new_env = Env([var], [eval(exp, env, repl = repl)], outer=env)
#         # return eval(body, env=new_env, repl = repl)

#         # NOTE(izzy): this implementation does support recursion, but it copies
#         # the environment every time which isn't great
#         (_, var, exp, body) = x
#         new_env = deepcopy(env)
#         new_env[var] = eval(exp, new_env, repl = repl)

#         return eval(body, env=new_env, repl = repl)


#     # NOTE(izzy): all good
#     elif x[0] == 'lambda':         # (lambda (var...) body)
#         (_, parms, body) = x
#         return Procedure(parms, body, env, func_string=str(x))

#     # NOTE(izzy): all good, but I added a case to allow array indexing
#     else:                          # (proc arg...)
#         try:
#             proc = eval(x[0], env, repl = repl)
#             args = [eval(exp, env, repl = repl) for exp in x[1:]]
#             if isinstance(proc, np.ndarray): return np.copy(proc[tuple(args)])
#             elif isinstance(proc, tuple): return proc[args[0]]
#             elif isinstance(proc, (Number, Symbol)): return proc
#             else: return proc(*args)

#         except Exception as E:
#             print(E, '\n')
#             # for debug purposes, if we get an error recur up the environment
#             # and dump the contents to the terminal before exiting
#             env_counter = 0
#             while env is not None:
#                 print('Environment', env_counter, env)
#                 env = env.outer
#                 env_counter += 1

#             sys.exit(1)

# def leaf_from_token(token):
#     try:
#         return Int(token)
#     except ValueError:
#         return Symbol(token)

# def ast_from_tokens(tokens):
#     "Read an expression from a sequence of tokens."
#     if len(tokens) == 0:
#         raise SyntaxError('unexpected EOF while reading')
#     token = tokens.pop(0)
#     if '(' == token:
#         L = AST()
#         while tokens[0] != ')':
#             L.append(ast_from_tokens(tokens))
#         tokens.pop(0) # pop off ')'
#         return L
#     elif ')' == token:
#         raise SyntaxError('unexpected )')
#     else:
#         return atom(token)

# def repl(prompt='lis.py> '):
#     while True:
#         inp = input(prompt)
#         ast = ast_from_tokens(tokenize(inp))
#         val = eval(ast)
#         if val is not None:
#             print(lispstr(val))

# if __name__ == '__main__':
#     repl()
