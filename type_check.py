from type_system import *

def type_check(x, env, print_type_error=True):
    """ Type check the program in the environment, and compute the return type.

    Arguments:
        x {any} -- the program (abstract syntax tree) to be typechecked
        env {Env} -- the environment in which the program is evaluated

    Returns:
        Bool -- True or False, does the program typecheck
        Type -- The return type of running the program. None if fail
        List -- A nested list of types with the same structure as the AST
    """

    # look up in the environment if it's a string
    if isinstance(x, str):
        try:
            dereferenced_x = env.find(x)[x]
        except:
            return False, None, []
        return type_check(dereferenced_x, env, print_type_error)
    # if it's a primitive
    elif isinstance(x, Primitive):
        return True, x.T, x.T
    # if it's none of the above and not a list, then it's an "unwrapped primitive."
    elif not isinstance(x, list):
        return True, object_to_type(x), []

    # if it's a list, then we have been given an abstract syntax tree for a
    # for a program, so we need to type-check recursively
    else:
        # first we type check the elements of the list. fail if they fail
        child_types = []
        type_tree = []
        for child in x:
            passed_type_check, child_type, child_type_tree =\
                type_check(child, env, print_type_error)
            if passed_type_check:
                child_types.append(child_type)
                type_tree.append(child_type_tree)
            else:
                return False, None, []

        proc_type = child_types[0]
        arg_types = child_types[1:]

        # if there are no children, then proc_type is the type of this tree
        if len(arg_types) == 0:
            return True, proc_type, proc_type

        # NOTE(izzy) We might need to allow things other than FuncType to have
        # children to allow array and tuple slicing?

        # if proc_type is a function, then we need to check if the given
        # arguments match the input type of the function
        elif isinstance(proc_type, FuncType):
            check_arguments_to_procedure(x[0], proc_type, arg_types)

        # if the proc_type has multiple type options, we need to check if the
        # arguments are consistent with any of those options
        elif isinstance(proc_type, OptionType):
            for possible_proc_type in proc_type.T:
                if isinstance(possible_proc_type, FuncType):
                    passed_type_check, return_type =\
                        check_arguments_to_procedure(x[0],
                            possible_proc_type, arg_types, print_type_error=True)

                    if passed_type_check:
                        return True, return_type, type_tree

        # if proc_type is not an OptionType or a FuncType, then it does not
        # accept any arguments
        else:
            if print_type_error:
                print(f'{str(proc_type)} does not accept arguments. Given:')
                for t in arg_types:
                    print('\t', t)

    # End of function.
    return False, None, []

def check_arguments_to_procedure(proc, proc_type, arg_types, print_type_error=True):
    """ Check if the arg_types given to proc are valid

    Arguments:
        proc {Primitive} -- a function object (only used for printing purposes)
        proc_type {FuncType or OptionType} -- the Type of proc
        arg_types {tuple(Type)} -- Type for each argument to the procedure

    Keyword Arguments:
        print_type_error {bool} -- constrols debug printing (default: {True})

    Returns:
        bool -- True if these are valid arguments to the procedure
    """
    def debug_print(*s):
        if print_type_error: print(*s)
        else: pass

    # get a tuple of the arguments types of the procedure
    if isinstance(proc_type.T_in, TupleType):
        proc_arg_types = proc_type.T_in
    else:
        proc_arg_types = (proc_type.T_in,)

    # check that we have the correct number of arguments
    correct_num_args = len(proc_arg_types)
    given_num_args = len(arg_types)
    if correct_num_args != given_num_args:
        debug_print(f'Incorrect number of arguments to {proc}: {str(proc_type)}. Received:')
        for t in arg_types:
            debug_print('\t', t)

        return False, None

    # the local type environment stores a dict {TemplateType: Type} so that
    # when we find out what type each TemplateType should be, we can save it
    # in the dictionary and make sure it is consistent everywhere
    local_type_env = {}

    # and check that each of the arguments match up
    for i, (required_arg_type, given_arg_type) in enumerate(zip(proc_arg_types, arg_types)):

        # if the procedure has template type
        if isinstance(required_arg_type, TemplateType):


            # first we check if the TemplateType has already been set
            # by one of the previous arguments. if so, type check normally
            if required_arg_type in local_type_env:
                required_arg_type = local_type_env[required_arg_type]
            # if the template type has not been set in the local type env,
            # then we can set it now.
            else:
                # if the TemplateType specifies a set of options, we need
                # to make sure that the given type is one of those options
                if isinstance(required_arg_type, OptionTemplateType):
                    if required_arg_type.accepts(given_arg_type):
                        debug_print(f'Incorrect argument #{i} to {proc}: {str(proc_type)}')
                        debug_print(f'\tExpected {str(required_arg_type)}')
                        debug_print(f'\tReceived {str(given_arg_type)}')
                        return False, None

                # set the type in the environment
                local_type_env[required_arg_type] = given_arg_type
                continue

        if required_arg_type.accepts(given_arg_type):
            debug_print(f'Incorrect argument #{i} to {proc}: {str(proc_type)}')
            debug_print(f'\tExpected {str(required_arg_type)}')
            debug_print(f'\tReceived {str(given_arg_type)}')
            return False, None

    # look up the return type in the local type env if needed
    if isinstance(proc_type.T_out, TemplateType):
        if proc_type.T_out in local_type_env:
            return_type = local_type_env[proc_type.T_out]
        else:
            debug_print(f'Unspecified TemplateType {str(proc_type.T_out)} returned from {str(proc_type)}.')
            return False, None

    # otherwise, it's simply specified by the function
    else:
        return_type = proc_type.T_out
    return True, return_type


int_types = ['numpy.'+t for t in dir(np) if 'int' in t] + ['int']
bool_types = ['numpy.'+t for t in dir(np) if 'bool' in t] + ['bool']

def object_to_typestring(x):
    """ generate the typestring using the builtin python "type" (note lowercase)
    """
    return str(type(x))[8:-2]

def object_to_type(x):
    """ take a python object and create a Type object for that object

    Arguments:
        x {anything other than Primitive} -- a python object

    Returns:
        Type -- Type corresponding to x
    """

    if isinstance(x, np.ndarray):
        # if we have an array, we use a specifal constructor (below)
        return array_to_type(x)
    else:
        # get a typestring for the object x
        typestring = object_to_typestring(x)
        print(typestring, bool_types)
        # The uppercase "Type" function wraps this typestring in a Type object
        if typestring in int_types: return Type('int')
        elif typestring in bool_types: return Type('bool')
        else: return Type(typestring)


def array_to_type(x):
    """ take a numpy array and create a Type object for that object


    Arguments:
        x {np.ndarray} -- a numpy array

    Returns:
        ArrayType -- ArrayType corresponding to x
    """
    # get the type of an element of the array
    element_type = object_to_type(x.ravel()[0])

    # NOTE(izzy): if we have access to an array constructor in the DSL, it
    # might become necessary to recursively typecheck the entries of x. That
    # would involve adding an env argumement to this function and recursively
    # checking the entries of x to make sure all the types match up
    #
    # x_type[i] = type_check(x[i], env, print_type_error=False)

    if x.ndim == 1:
        return Array1DType(element_type)
    elif x.ndim == 2:
        return Array2DType(element_type)
    else:
        return ArrayType(element_type)
