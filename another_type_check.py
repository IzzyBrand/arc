from ast import AST
from type_system import Primitive, FuncType, TupleType

def type_check(prog, env):
    """ Computes the type of this tree and all of it's children.
    
    Returns:
        bool -- False if typecheck fails in this tree or the children. 
                True otherwise.
    """

    # NOTE(izzy) We might need to allow things other than FuncType to have
    # children to allow array and tuple slicing?

    # look up in the environment if it's a string
    if isinstance(prog, str):
        dereferenced_prog = env.find(prog)[prog]
        return type_check(dereferenced_prog, env)

    # primitives always pass the type check, and have a type T
    elif isinstance(prog, Primitive):
        return True, prog.T

    elif isinstance(prog, AST):
        # type check the node and the children. fail if they fail
        child_types = []
        for child in prog:
            passed_type_check, child_type = type_check(child, env)
            if passed_type_check:
                child_types.append(child_type)
            else:
                return False, []

        func_type = child_types[0]
        arg_types = child_types[1:]
        # if there are no children, then the node is the type of this tree:
        if len(arg_types) == 0:
            return True, func_type

        # if we have children, then they are the arguments to the node
        
        # check that the node is a FuncType, and error if not
        if not isinstance(func_type, FuncType):
            print(f'{str(func_type)} does not accept arguments. Given:')
            for t in arg_types:
                print('\t', t)
            return False, []

        # check that we have the correct arguments if there are multiple
        if isinstance(func_type.T_in, TupleType):
            correct_num_args = len(func_type.T_in)
            given_num_args = len(arg_types)
            if correct_num_args != given_num_args:
                print(f'Incorrect number of arguments to {str(func_type)}. Received:')
                for t in arg_types:
                    print('\t', t)

                return False, []

            for i in range(correct_num_args):
                if func_type.T_in[i] != arg_types[i]:
                    print(f'Incorrect argument #{i} to {str(func_type)}.')
                    print(f'\tExpected {str(func_type.T_in[i])}. Received {str(arg_types[i])}')
                    return False, []
        # if it's a single argument, check that it matches
        else:
            if len(arg_types) != 1:
                print(f'Incorrect number of arguments to {(func_type)}. Received:')
                for t in arg_types:
                    print('\t', t)

                return False, []
            if func_type.T_in != arg_types[0]:
                    print(f'Incorrect argument to {str(func_type)}.')
                    print(f'\tExpected {str(func_type.T_in)}. Received {str(arg_types[0])}')
                    return False, []

        #     if len(arg_types) != len(func_type.T_in.T):
        #         print(f'Incorrect number of arguments to {(func_type.T)}. Received:')
        #         for t in arg_types:
        #             print('\t', t)
        #         return False, []
        #     else:
        #         if 
        
        # # and check that each argument is of the correct type
        # for i, (required_arg_type, given_arg_type) in enumerate(zip(func_type.T_in.T, arg_types)):
        #     if required_arg_type != given_arg_type:
        #         print(f'Incorrect argument #{i} to {str(func_type)}.')
        #         print(f'\tExpected {str(required_arg_type)}. Received {str(given_arg_type)}')
        #         return False, []

        # if we pass all of those checks, then this subtree returns the return type
        # of the node
        return_type = func_type.T_out
        return True, [return_type, child_types]