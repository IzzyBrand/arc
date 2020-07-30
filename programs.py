""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""

from primitives import *

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
    def __init__(self, root=None, children=[]):
        self.parent = parent
        self.children = children
        self.type_check()

    def type_check(self):
        # if this is an empty program, it type checks w/ NoneType
        if self.parent is None:
            self.output_type = None
            self.input_type = None
            return True
        # if this is a length-1 program, it type checks with the
        # type of the parent (which is assumed to be a primitive)
        elif not self.children:
            assert isinstance(self.parent, Primitive)
            self.output_type = self.parent.output_type
            self.input_type = self.parent.input_type
            return True
        # if there are children, then we need to recursively type check
        else:
            assert isinstance(self.parent, Primitive)
            self.output_type = self.parent.output_type

            for c in self.children:
                # type_check recursively
                if isinstance(c, TreeStructuredProgram) and not c.type_check():
                        return False

            # aggregate the types of the children
            children_input_type = [c.input_type for c in self.children if c.input_type is not None]
            children_output_type = [c.output_type for c in self.children]

            # make sure the child output matches the input of the parent
            if children_output_type != self.parent.input_type:
                return False

            # if any children accept inputs, they should all accept the same
            # input type. And that input type becomes the input type of the
            # entire program
            if children_input_type:
                if len(set(children_input_type)) == 1:
                    self.input_type = children_input_type[0]
                else:
                    return False
            else:
                self.input_type = None

            return True

    def __str__(self):
        args = ', '.join([str(c) for c in self.children])
        return f'{str(self.root)}({args})'

    def __call__(self, x):
        # if there is no root operation, then this is the identity
        if self.root is None:
            return x
        # if there are child operations, evaluate them
        if self.children:
            x = [child(x) for child in self.children]
        # evaluate the root operation
        return self.root(x)


if __name__ == '__main__':
    P = SimpleSequentialProgram([PatchExtract, HFlip])
    print(P.get_param_list())

    param_list = [[0,0,0,0],[]]
    P.compile(param_list)
    print(P.get_param_list())

    param_list = [[0,0,1,1],[]]
    P.compile(param_list)
    print(P.get_param_list())

    P.decompile()
    print(P.get_param_list())
