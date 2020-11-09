import operator as op
###############################################################################
# Types
###############################################################################
# NOTE(izzy): We could simply pass around the string representation of a type,
# but for type_check (when we want to ensure that the types of a program are
# consistent, ie. that the output type of a function matches the input type of
# the next function), we would have to parse the string representation of
# higher-order types. For this reason we implement the `Type` class

class Type:
    """ Base type
    """
    def __init__(self, T):
        self.T = T

    def __str__(self):
        return self.T

class TupleType(Type):
    """ Describes the type of a tuple of items

    Extends:
        Type
    """
    def __init__(self, *args):
        super(TupleType, self).__init__(args)

    def __str__(self):
        return f"({', '.join(str(t) for t in self.T)})"

    # make sure length and indexing still work
    def __len__(self):
        return len(self.T)
    def __getitem__(self, item):
        return tuple.__getitem__(self.T, item)

class FuncType(Type):
    """ Describes the type of a function. Functions with multiple inputs or
    multiples outputs use the TupleType to wrap the inputs and outputs

    Extends:
        Type
    """
    def __init__(self, T_in, T_out):

        # convert types to tuples as needed
        if isinstance(T_in, tuple): T_in = TupleType(*T_in)
        if isinstance(T_out, tuple): T_out = TupleType(*T_out)
        super(FuncType, self).__init__((T_in, T_out))
        self.T_in = T_in
        self.T_out = T_out

    def __str__(self):
        return f"{str(self.T_in)} -> {str(self.T_out)}"

class ArrayType(Type):
    """ Describes the type of an array or list of items.

    Extends:
        Type
    """
    def __init__(self, T):
        super(ArrayType, self).__init__(T)

    def __str__(self):
        return f"ArrayOf{str(self.T)}"

class TemplateType(Type):
    """ Some functions can handle multiple types. For example map has a return
    type which depends on the function being mapped. This template type is for
    that purpose

    Extends:
        Type
    """
    def __init__(self, T):
        super(TemplateType, self).__init__(T)

    def __str__(self):
        return f"<{self.T}>"

###############################################################################
# type_check
###############################################################################
def type_check(x, env):
    """ Type check the program in the environment, and compute the return type.

    Arguments:
        x {any} -- the program (abstract syntax tree) to be typechecked
        env {Env} -- the environment in which the program is evaluated

    Returns:
        Bool -- True or False, does the program typecheck
        Type -- The return type of running the program. None if fail
        List -- A nested list of types with the same structure as the AST
    """

    # NOTE(izzy) We might need to allow things other than FuncType to have
    # children to allow array and tuple slicing?

    # look up in the environment if it's a string
    if isinstance(x, str):
        dereferenced_x = env.find(x)[x]
        return type_check(dereferenced_x, env)
    # if it's a primitive
    elif isinstance(x, Primitive):
        return True, x.T, x.T
    # if it's none of the above and not a list, then it's an "unwrapped primitive."
    elif not isinstance(x, list):
        return True, type(x), type(x)
    # if it's a list, then we have to recur, and check that the arguments
    # match up to the function call
    else:
        # type check the node and the children. fail if they fail
        child_types = []
        type_tree = []
        for child in x:
            passed_type_check, child_type, child_type_tree = type_check(child, env)
            if passed_type_check:
                child_types.append(child_type)
                type_tree.append(child_type_tree)
            else:
                return False, None, []

        func_type = child_types[0]
        arg_types = child_types[1:]
        # if there are no children, then the node is the type of this tree:
        if len(arg_types) == 0:
            return True, func_type, func_type

        # if we have children, then they are the arguments to the node

        # check that the node is a FuncType, and error if not
        if not isinstance(func_type, FuncType):
            print(f'{str(func_type)} does not accept arguments. Given:')
            for t in arg_types:
                print('\t', t)
            return False, None, []

        # check that we have the correct arguments if there are multiple
        if isinstance(func_type.T_in, TupleType):
            correct_num_args = len(func_type.T_in)
            given_num_args = len(arg_types)
            if correct_num_args != given_num_args:
                print(f'Incorrect number of arguments to {x[0]}: {str(func_type)}. Received:')
                for t in arg_types:
                    print('\t', t)

                return False, None, []

            for i in range(correct_num_args):
                if func_type.T_in[i] != arg_types[i]:
                    print(f'Incorrect argument #{i} to {x[0]}: {str(func_type)}')
                    print(f'\tExpected {str(func_type.T_in[i])}')
                    print(f'\tReceived {str(arg_types[i])}')
                    return False, None, []
        # if it's a single argument, check that it matches
        else:
            if len(arg_types) != 1:
                print(f'Incorrect number of arguments to {str(func_type)}. Received:')
                for t in arg_types:
                    print('\t', t)

                return False, []
            if func_type.T_in != arg_types[0]:
                    print(f'Incorrect argument to {x[0]}: {str(func_type)}')
                    print(f'\tExpected {str(func_type.T_in)}')
                    print(f'\tReceived {str(arg_types[0])}')
                    return False, None, []

        return_type = func_type.T_out
        return True, return_type, type_tree




###############################################################################
# Primitives and Environment
###############################################################################

class Primitive:
    def __init__(self, name, T):
        self.name = name
        self.T = T

    def __call__(self):
        return self

    def __str__(self):
        return self.name

typed_env = {}

class FuncCreator(Primitive):
    def __init__(self, name, T, f, env=typed_env):
        self.name = name
        self.T = T
        self.f = f

        if env is not None:
            env[self.name] = self

    def __call__(self, *args):
        return self.f(*args)

# create the default environment by adding symbols using FuncCreator
FuncCreator('+', FuncType((int, int), int), op.add)
FuncCreator('-', FuncType((int, int), int), op.sub)
FuncCreator('*', FuncType((int, int), int), op.mul)
FuncCreator('>', FuncType((int, int), bool), op.gt)
FuncCreator('>=', FuncType((int, int), bool), op.ge)
FuncCreator('==', FuncType((int, int), bool), op.eq)


###############################################################################
# Example
###############################################################################

if __name__ == '__main__':
    Color_T = Type("Color")
    colorarray_T = ArrayType(Color_T)

    # example of a function that counts the number of pixels of a certain color
    colorcount_T = FuncType((colorarray_T, Color_T), int)
    print("colorcount:", colorcount_T)

    # example of the type of map using a template type
    T1 = TemplateType(1)
    T2 = TemplateType(2)
    input_type = (ArrayType(T1), FuncType(T1, T2))
    output_type = ArrayType(T2)
    map_T = FuncType(input_type, output_type)
    print("map:", map_T)
