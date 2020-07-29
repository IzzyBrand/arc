""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""

from primitives import *

class SimpleSequentialProgram:
    def __init__(self, primitives):
        self.primitives = primitives
        assert len(primitives) > 0
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

    def __call__(self, x):
        # execute the program on the given input
        for primitive in self.primitives:
            x = primitive(x)

        return x

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
