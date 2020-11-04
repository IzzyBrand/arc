from types import *

# NOTE(izzy):
# * might need to add an environment which gets passed around during typecheck?
# * We might need to allow things other than FuncType to have children to allow 
#   array and tuple slicing

class Tree:
    """ This Tree class serves as an alternative to the typical nested-
    lists representation of LISP's abstract syntax tree.

    The advantage of implementing this with classes is that we can provide a
    typechecking function that stores the result of the typechecking
    computation for each subtree.
    """
    def __init__(self, node, children):
        # the node is the symbols stored at this point in the tree. This
        # symbol could be a primitive (like an Int), or it could be a function.
        self.node = node
        # if there are children, then node must be a function, and the children
        # are the arguments to node.
        self.children = children

    def type_check(self):
        """ Computes the type of this tree and all of it's children.
        
        Returns:
            bool -- False if typecheck fails in this tree or the children. 
                    True otherwise.
        """

        # type check the node and the children. fail if they fail
        if not self.node.type_check():
            return False
        for child in self.children:
            if not child.type_check():
                return False

        # if there are no children, then the node is the type of this tree:
        if len(self.children) == 0:
            self.type = self.node.type
            return True

        # if we have chilren, then they are the arguments to the node
        
        # check that the node is a FuncType, and error if not
        if not isinstance(self.node.type, FuncType):
            print(f'{str(self.node.type)} does not accept arguments. Given:')
            for c in self.children:
                print(f'\t{str(c.type)}')
            return False

        # check that we have the correct number of arguments
        if len(self.children) != len(self.node.type[0]):
            print(f'Incorrect number of arguments to {str(self.node.type)}. Received:')
            for c in self.children:
                print(f'\t{str(c.type)}')
            return False
        
        # and check that each argument is of the correct type
        for i, (arg_type, given) in enumerate(zip(self.node.type[1], self.children)):
            if arg_type != given.type:
                print(f'Incorrect argument #{i} to f{str(self.node.type)}.')
                print(f'\tExpected {str(arg_type)}. Received {str(given.type)}')
                return False

        # if we pass all of those checks, then this subtree returns the return type
        # of the node
        self.type = self.node.type[1]
        return True
                
