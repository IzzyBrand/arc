""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""

import numpy as np

# a list of all the primitives
language = []

# a default init function for new primitives that save the input arguments
# to a params list
def default_init(self, *args):
    self.params = args

# meta function for creating new primitives. Constructs a primitive from the
# given description and add the new primitive to the language
def create_primitive(name, input_type, output_type, param_type,
    func, init_func=default_init):
    new_primitive =  type(name, (),
        {
            "name": name,
            "input_type": input_type,
            "output_type": output_type,
            "param_type": param_type,
            "__init__": init_func,
            "__call__": func
        })
    language.append(new_primitive)
    return(new_primitive)

###############################################################################
# Primitive Definitions
###############################################################################

# pull a patch out from a grid at the specified coordinates
def patch_extract_func(self, input_grid):
    x, y, w, h = self.params
    return input_grid[y:y+h, x:x+w]

PatchExtract = create_primitive(
    name = 'PatchExtract',
    input_type = ['Grid'],
    output_type = ['Grid'],
    param_type = ['Int', 'Int', 'Int', 'Int'],
    func = patch_extract_func
    )

# mask the grid by a set color
def color_mask_func(self, input_grid):
    c, = self.params
    return (input_grid == c).astype(int)

ColorMask = create_primitive(
    name = 'ColorMask',
    input_type = ['Grid'],
    output_type = ['Grid'],
    param_type = ['Int'],
    func = color_mask_func
    )

Add = create_primitive(
    name = 'Add',
    input_type = ['Int', 'Int'],
    output_type = ['Int'],
    param_type = [],
    func = np.add
    )

Mul = create_primitive(
    name = 'Mul',
    input_type = ['Int', 'Int'],
    output_type = ['Int'],
    param_type = [],
    func = np.multiply
    )

VFlip = create_primitive(
    name = 'Mul',
    input_type = ['Grid'],
    output_type = ['Grid'],
    param_type = [],
    func = lambda x: np.flip(x, axis=0)
    )

HFlip = create_primitive(
    name = 'Mul',
    input_type = ['Grid'],
    output_type = ['Grid'],
    param_type = [],
    func = lambda x: np.flip(x, axis=1)
    )
