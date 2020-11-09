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
