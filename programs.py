""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""

class SimpleSequentialProgram:
    def __init__(self, primitives):
        self.primitives = primitives
        assert len(primitives) > 0
        self.type_check()
        self.type_set()

    def type_check(self):
        # make sure the types of the primitives are consistent
        types_consistent = True

        for i in range(len(self.primitives)-1):
            types_consistent &=
            	(primitives[i].output_type == primitives[i+1].input_type)

        return types_consistent

     def type_set(self):
        # get the types from all the primitives
     	self.input_type = self.primitives[0].input_type
     	self.output_type = self.primitives[-1].output_type
     	self.param_types = [p.param_type for p in self.primitives]

 	def compile(self, param_list):
        # apply the supplied parameters to each primitive
 		for primitive, params in zip(self.primitives, param_list):
 			primitive.__init__(*params)

    def __call__(self, x):
        # execute the program on the given input
        for primitive in self.primitives:
            x = primitive(x)

        return x
