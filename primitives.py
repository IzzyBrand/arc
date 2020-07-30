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

# these four primitives are the identity
def PassGrid(args):
    return args
create_primitive(PassGrid, 'Grid', 'Grid')

def PassInt(args):
    return args
create_primitive(PassInt, 'Int', 'Int')

def PassMask(args):
    return args
create_primitive(PassMask, 'Mask', 'Mask')

def PassColor(args):
    return args
create_primitive(PassColor, 'Color', 'Color')

# primtiives which operate on grids, masks and shapes
def VFlip(args):
    grid, = args
    return np.flip(grid, axis=0)
create_primitive(VFlip, 'Grid', 'Grid')

def HFlip(args):
    grid, = args
    return np.flip(grid, axis=1)
create_primitive(HFlip, 'Grid', 'Grid')

def EqualGrid(args):
    grid1, grid2 = args
    return grid1 == grid2
create_primitive(EqualGrid, ['Grid', 'Grid'], 'Mask')

def InvertMask(args):
    mask, = args
    return 1 - mask
create_primitive(InvertMask, 'Mask', 'Mask')

def Tile(args):
    grid, x, y
    return np.tile(grid, (y, x))
create_primitive(Tile, ['Grid', 'Int', 'Int'], 'Grid')

def ExtractPatch(args):
    grid, x, y, w, h = args
    # TODO(izzy): at some point we'll have to be smarter about selecting
    # indices and dimensions. for the minute, we'll just pretend the function
    # is a no-op if dimensions are invalie
    try:
        return grid[y:y+h, x:x+w]
    except IndexError:
        return grid
create_primitive(ExtractPatch, ['Grid', 'Int', 'Int', 'Int', 'Int'], 'Grid')

def CreatePatch(args):
    w, h, color = args
    return np.ones([h,w]) * color
create_primitive(CreatePatch, ['Int', 'Int', 'Color'], 'Grid')

def ColorMask(args):
    grid, color = args
    return grid == np.ones_like(grid)*color
create_primitive(ColorMask, ['Grid', 'Color'], 'Mask')

def CountColor(args):
    grid, color = args
    return (grid == color).sum()
create_primitive(CountColor, ['Grid', 'Color'], 'Int')

def Contract(args):
    grid, mask = args
    h, w = mask.shape
    v_idxs = np.arange(h)[mask.sum(axis=1) > 0]
    h_idxs = np.arange(w)[mask.sum(axis=0) > 0]
    v_min, v_max = np.min(v_idxs), np.max(v_idxs)
    h_min, h_max = np.min(h_idxs), np.max(h_idxs)
    return grid[v_min:v_max+1, h_min:h_max+1]
create_primitive(Contract, ['Grid', 'Mask'], 'Grid')


if __name__ == '__main__':
    for p in language:
        print(f'{p.name}:\t{p.input_type} -> {p.output_type}')