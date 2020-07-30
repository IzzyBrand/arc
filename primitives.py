""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""

import numpy as np

# a list of all the primitives
language = []

def create_primitive(func, input_type, output_type):
    func.name = func.__name__
    func.input_type = input_type
    func.output_type = output_type
    language.append(func)

def Int_p(i):
    def f(args):
        return i
    f.name = f'Int_{i}'
    f.input_type = None
    f.output_type = 'Int'
    return f

def Color_p(i):
    assert i >= 0 and i <= 10
    def f(args):
        return i
    f.name = f'Color_{i}'
    f.input_type = None
    f.output_type = 'Color'
    return f

###############################################################################
# Primitive Definitions
###############################################################################

def VFlip(args):
    grid, = args
    return np.flip(grid, axis=0)

def HFlip(args):
    grid, = args
    return np.flip(grid, axis=1)

def GridEqual(args):
    grid1, grid2 = args
    return grid1 == grid2

def ColorMask(args):
    grid, color = args
    return grid == color

def ColorCount(args):
    grid, color = args
    return (grid == color).sum()

def PatchExtract(args):
    grid, x, y, w, h = args
    # TODO(izzy): at some point we'll have to be smarter about selecting
    # indices and dimensions. for the minute, we'll just pretend the function
    # is a no-op if dimensions are invalie
    try:
        return grid[y:y+h, x:x+w]
    except IndexError:
        return grid

def PatchCreate(args):
    w, h, color = args
    return np.ones([h,w]) * color

create_primitive(VFlip, 'Grid', 'Grid')
create_primitive(HFlip, 'Grid', 'Grid')
create_primitive(GridEqual, ['Grid', 'Grid'], 'Mask')
create_primitive(ColorMask, ['Grid', 'Color'], 'Mask')
create_primitive(ColorCount, ['Grid', 'Color'], 'Int')
create_primitive(PatchExtract, ['Grid', 'Int', 'Int', 'Int', 'Int'], 'Grid')
create_primitive(PatchCreate, ['Int', 'Int', 'Color'], 'Grid')


if __name__ == '__main__':
    print([p.name for p in language])