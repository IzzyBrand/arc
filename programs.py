""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""

from primitives import *

def item(x):
    if isinstance(x, (list, tuple)) and len(x) == 1:
        return x[0]
    else:
        return x


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

        self.output_type = 'Unknown'
        self.input_type = 'Unknown'

    def type_check(self):
        # if this is an empty program, it type checks w/ NoneType
        if self.parent is None:
            self.output_type = None
            self.input_type = None
            return True
        # if this is a length-1 program, it type checks with the
        # type of the parent (which is assumed to be a primitive)
        elif not self.children:
            self.output_type = self.parent.output_type
            self.input_type = self.parent.input_type
            return True
        # if there are children, then we need to recursively type check
        else:
            self.output_type = self.parent.output_type
            for c in self.children:
                # type_check recursively
                if isinstance(c, TreeStructuredProgram) and not c.type_check():
                        return False

            # aggregate the types of the children
            children_input_type = [c.input_type for c in self.children if c.input_type is not None]
            children_output_type = [c.output_type for c in self.children]

            # make sure the child output matches the input of the parent
            if item(children_output_type) != self.parent.input_type:
                print(f'{self.parent.name} expects input of type {self.parent.input_type}. Got {item(children_output_type)}.')
                return False

            # if any children accept inputs, they should all accept the same
            # input type. And that input type becomes the input type of the
            # entire program
            if children_input_type:
                all_children_input_types_equal = True
                type_0 = children_input_type[0]
                for type_i in children_input_type:
                    all_children_input_types_equal &= (type_0 == type_i)

                if all_children_input_types_equal:
                    self.input_type = type_0
                else:
                    print(f'All children must have the same input type. {[str(c) if isinstance(c, TreeStructuredProgram) else c.name for c in self.children]} have different input types.')
                    return False
            else:
                self.input_type = None

            return True

    def eval(self, x):
        # if there is no parent operation, then this is the identity
        if self.parent is None:
            return x
        # if there are child operations, evaluate them
        if self.children:
            x = [child.eval(x) for child in self.children]
        # evaluate the parent operation
        return self.parent.eval(x)

    def __str__(self):
        if self.parent is None:
            return 'None'
        else:
            if self.children:
                args = ', '.join([str(c) if isinstance(c, TreeStructuredProgram) \
                    else c.name for c in self.children])
                return f'{self.parent.name}({args})'
            else:
                if self.parent.input_type is None:
                    return self.parent.name
                else:
                    return f'{self.parent.name}(_)'


if __name__ == '__main__':
    good_spec = (HFlip, (VFlip, VFlip))
    P = TreeStructuredProgram(good_spec)
    print(P)
    print('Type check:', P.type_check())
    print(f'{P.input_type} -> {P.output_type}')
    print()

    bad_spec = (HFlip, VFlip, VFlip)
    P = TreeStructuredProgram(bad_spec)
    print(P)
    print('Type check:', P.type_check())
    print(f'{P.input_type} -> {P.output_type}')
    print()

    bad_spec = (GridEqual, VFlip, HFlip)
    P = TreeStructuredProgram(bad_spec)
    print(P)
    print('Type check:', P.type_check())
    print(f'{P.input_type} -> {P.output_type}')
    print()

    bad_spec = (GridEqual, VFlip, PatchCreate)
    P = TreeStructuredProgram(bad_spec)
    print(P)
    print('Type check:', P.type_check())
    print(f'{P.input_type} -> {P.output_type}')
    print()

    good_spec = (PatchExtract, )
    P = TreeStructuredProgram(good_spec)
    print(P)
    print('Type check:', P.type_check())
    print(f'{P.input_type} -> {P.output_type}')
    print()

    good_spec = (PatchExtract, HFlip, Int_p(1), Int_p(1), Int_p(1), Int_p(1))
    P = TreeStructuredProgram(good_spec)
    print(P)
    print('Type check:', P.type_check())
    print(f'{P.input_type} -> {P.output_type}')
    print()
