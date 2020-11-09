import operator as op
from ast import AST
###############################################################################
# Types
###############################################################################

class Type:
    """ Base type for things like numbers and arrays
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
       

class ArrayType(Type):
    """ Describes the type of an array or list of items.

    Extends:
        Type
    """
    def __init__(self, T):
        super(ArrayType, self).__init__(T)

    def __str__(self):
        return f"ArrayOf{str(self.T)}"

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

Int_T = Type("Int")
Color_T = Type("Color")
Bool_T = Type("Bool")


###############################################################################
# type_check
###############################################################################

def type_check(prog, env):
    """ Computes the type of this tree and all of it's children.
    
    Returns:
        bool -- False if typecheck fails in this tree or the children. 
                True otherwise.
    """

    # NOTE(izzy):
    # * might need to add an environment which gets passed around during typecheck?
    # * We might need to allow things other than FuncType to have children to allow 
    #   array and tuple slicing

    print('[type_check]', prog)

    # look up in the environment if it's a string
    if isinstance(prog, str):
        dereferenced_prog = env.find(prog)[prog]
        return type_check(dereferenced_prog, env)

    # primitives always pass the type check
    elif isinstance(prog, Primitive):
        return True

    elif isinstance(prog, AST):
        # type check the node and the children. fail if they fail
        for child in prog:
            if not type_check(child, env): return False

        # if there are no children, then the node is the type of this tree:
        if len(prog[1:]) == 0:
            prog.T = prog[0].T
            return True

        # if we have chilren, then they are the arguments to the node
        
        # check that the node is a FuncType, and error if not
        if not isinstance(prog[0].T, FuncType):
            print(f'{str(prog[0].T)} does not accept arguments. Given:')
            for c in prog[1:]:
                print(f'\t{str(c.T)}')
            return False

        # check that we have the correct number of arguments
        if len(prog[1:]) != len(prog[0].T[0]):
            print(f'Incorrect number of arguments to {str(prog[0].T)}. Received:')
            for c in prog[1:]:
                print(f'\t{str(c.T)}')
            return False
        
        # and check that each argument is of the correct type
        for i, (arg_type, given) in enumerate(zip(prog[0].T[1], prog[1:])):
            if arg_type != given.T:
                print(f'Incorrect argument #{i} to f{str(prog[0].T)}.')
                print(f'\tExpected {str(arg_type)}. Received {str(given.T)}')
                return False

        # if we pass all of those checks, then this subtree returns the return type
        # of the node
        prog.T = prog[0].T[1]
        return True

    else:
        print('[type_check] failed for program', prog)


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

class FuncConstructor(Primitive):
    def __init__(self, name, T, f):
        self.name = name
        self.T = T
        self.f = f

    def __call__(self, *args):
        return self.f(*args)

class IntConstructor(Primitive):
    def __init__(self, val):
        self.name = str(val)
        self.val = int(val)
        self.T = Int_T

    def __call__(self):
        return self.val

typed_env = {
   '+': FuncConstructor('+', FuncType((Int_T, Int_T), Int_T), op.add),
   '-': FuncConstructor('-', FuncType((Int_T, Int_T), Int_T), op.sub)
}

###############################################################################
# Example
###############################################################################


if __name__ == '__main__':
    colorarray_T = ArrayType(Color_T)
    l_t = Type("List")

    # example of a function that counts the number of pixels of a certain color
    colorcount_T = FuncType((colorarray_T, Color_T), Int_T)
    print("colorcount:", colorcount_T)

    # example of the type of map using a template type
    T1 = TemplateType(1)
    T2 = TemplateType(2)
    input_type = (ArrayType(T1), FuncType(T1, T2))
    output_type = ArrayType(T2)
    map_T = FuncType(input_type, output_type)
    print("map:", map_T)
