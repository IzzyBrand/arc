""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""

from primitives import *
from util import *


class SimpleSequentialProgram:
    def __init__(self, primitives):
        self.primitives = primitives
        assert len(primitives) > 0, 'Program must be non-empty (so far)'
        self.type_set()
        self.compiled = False

    def type_check(self):
        # make sure the types of the primitives are consistent
        types_consistent = True

        for i in range(len(self.primitives)-1):
            types_consistent &=\
            (self.primitives[i].output_type == self.primitives[i+1].input_type)

        return types_consistent

    def type_set(self):
        # get the types from all the primitives
        self.input_type = self.primitives[0].input_type
        self.output_type = self.primitives[-1].output_type
        self.param_types = [p.param_type for p in self.primitives]

    def compile(self, param_list):
        # apply the supplied parameters to each primitive
        if self.compiled:
            for p, a in zip(self.primitives, param_list):
                p.__init__(*a)
        else:
            self.primitives = [p(*a) for p, a in zip(self.primitives, param_list)]

        self.compiled = True

    def decompile(self):
        # revert each primitve from an instance to it's class
        # (effectively deletes the parameter assignments for each primitive)
        if self.compiled:
            self.primitives = [p.__class__ for p in self.primitives]

        self.compiled = False

    def get_param_list(self):
        if self.compiled:
            return [p.params for p in self.primitives]
        else:
            return None

    def __str__(self):
        return '\n'.join([f'{i}: {str(p)}' for i, p in enumerate(self.primitives)])

    def __call__(self, x):
        assert self.compiled, 'Program must be compiled to evaluate'
        # print(self)
        # execute the program on the given input
        for primitive in self.primitives:
            x = primitive(x)

        return x


class TreeStructuredProgram:
    def __init__(self, spec):
        if isinstance(spec, (list, tuple)):
            self.parent = spec[0]
            self.children = [TreeStructuredProgram(childspec) for childspec in spec[1:]]
        else:
            self.parent = spec
            self.children = []

        self.my_type = ['Unknown']

    def type_check(self):
        self.my_type = self.parent.my_type

        # if this is a length-1 program, it type checks with the
        # type of the parent (which is assumed to be a primitive)
        if not self.children:
            return True

        # if there are children, then we need to recursively type check
        for c in self.children:
            if not c.type_check():
                return False 

        # aggregate the types of the children
        children_type = tuple(item(c.my_type) for c in self.children)

        # make sure the child output matches the input of the parent
        if children_type != self.parent.my_type[:-1]:
            print(children_type, self.parent.my_type[:-1])
            print(f'{self.parent.name} expects input of type {str_type(self.parent.my_type[:-1], input_only=True)}. Got {str_type(children_type, input_only=True)}.')
            return False


        return True

    def eval(self, x):
        assert self.parent is not None
        # all primitives and programs expect the inputs to be in a list format
        # sometimes the use may pass in a single item at the top level, so we
        # need to detect that and wrap it in a list for them
        if not isinstance(x, (tuple, list)): x = [x]
        # if there are child operations, evaluate them
        # Some may be subtrees and other will be primitives
        if self.children:
            x = [p.eval(x) for p in self.children]
        # evaluate the parent operation (always a primitive)
        return self.parent(x)

    def __str__(self):
        if self.parent is None:
            return 'None'
        if self.children:
            args = ', '.join([str(c) for c in self.children])
            return f'{self.parent.name}({args})'
        else:
            return self.parent.name


if __name__ == '__main__':
    spec = (IfGridToGrid, SizeOneGrid_p(0), HasBlackCell, HFlip, VFlip)
    P = TreeStructuredProgram(spec)
    print(P)
    print('Type check:', P.type_check())
    print(str_type(P.my_type))
    print()

    good_spec = (HFlip, (VFlip, VFlip))
    P = TreeStructuredProgram(good_spec)
    print(P)
    print('Type check:', P.type_check())
    print(str_type(P.my_type))
    print()

    bad_spec = (HFlip, VFlip, VFlip)
    P = TreeStructuredProgram(bad_spec)
    print(P)
    print('Type check:', P.type_check())
    print(str_type(P.my_type))
    print()

    good_spec = (EqualGrid, VFlip, HFlip)
    P = TreeStructuredProgram(good_spec)
    print(P)
    print('Type check:', P.type_check())
    print(str_type(P.my_type))
    print()

    bad_spec = (EqualGrid, VFlip, CreatePatch)
    P = TreeStructuredProgram(bad_spec)
    print(P)
    print('Type check:', P.type_check())
    print(str_type(P.my_type))
    print()

    good_spec = (ExtractPatch, )
    P = TreeStructuredProgram(good_spec)
    print(P)
    print('Type check:', P.type_check())
    print(str_type(P.my_type))
    print()

    good_spec = (ExtractPatch, HFlip, Int_p(1), Int_p(1), Int_p(1), Int_p(1))
    P = TreeStructuredProgram(good_spec)
    print(P)
    print('Type check:', P.type_check())
    print(str_type(P.my_type))
    print()
