""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""

import numpy as np
from util import *
# a list of all the primitives
language = []

class Primitive:
    def __init__(self, func, *my_type):
        self.func = func
        self.name = func.__name__
        self.my_type = my_type
        self.type_check = lambda: True
        language.append(self)

    def __call__(self, x):
        return self.func(x)

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
Primitive(PassGrid, 'Grid', 'Grid')

def PassInt(args):
    return args
Primitive(PassInt, 'Int', 'Int')

def PassMask(args):
    return args
Primitive(PassMask, 'Mask', 'Mask')

def PassColor(args):
    return args
Primitive(PassColor, 'Color', 'Color')

# primtiives which operate on grids, masks and shapes
def VFlip(args):
    grid, = args
    return np.flip(grid, axis=0)
Primitive(VFlip, 'Grid', 'Grid')

def HFlip(args):
    grid, = args
    return np.flip(grid, axis=1)
Primitive(HFlip, 'Grid', 'Grid')

def EqualGrid(args):
    grid1, grid2 = args
    return grid1 == grid2
Primitive(EqualGrid, 'Grid', 'Grid', 'Mask')

def InvertMask(args):
    mask, = args
    return (1 - mask).astype(bool)
Primitive(InvertMask, 'Mask', 'Mask')

def Tile(args):
    grid, x, y
    return np.tile(grid, (y, x))
Primitive(Tile, 'Grid', 'Int', 'Int', 'Grid')

def ExtractPatch(args):
    grid, x, y, w, h = args
    # TODO(izzy): at some point we'll have to be smarter about selecting
    # indices and dimensions. for the minute, we'll just pretend the function
    # is a no-op if dimensions are invalie
    try:
        return grid[y:y+h, x:x+w]
    except IndexError:
        return grid
Primitive(ExtractPatch, 'Grid', 'Int', 'Int', 'Int', 'Int', 'Grid')

def CreatePatch(args):
    w, h, color = args
    return np.ones([h,w]) * color
Primitive(CreatePatch, 'Int', 'Int', 'Color', 'Grid')

def MaskFromColor(args):
    grid, color = args
    return grid == np.ones_like(grid)*color
Primitive(MaskFromColor, 'Grid', 'Color', 'Mask')

def CreateGridFromMask(args):
    mask, color = args
    return mask*color
Primitive(CreateGridFromMask, 'Mask', 'Color', 'Grid')

def ColorGridWithMask(args):
    grid, mask, color = args
    return grid*(1-mask) + mask*color
Primitive(ColorGridWithMask, 'Grid', 'Mask', 'Color', 'Grid')

def MaskedOverlay(args):
    grid1, grid2, mask = args
    return grid1*(1-mask) + grid2*mask
Primitive(MaskedOverlay, 'Grid', 'Grid', 'Mask', 'Grid')

def CountColor(args):
    grid, color = args
    return (grid == color).sum()
Primitive(CountColor, 'Grid', 'Color', 'Int')

def MostFrequentColor(args):
    grid, = args
    color_matches = grid.ravel()[:, None] == np.arange(10)[None,:]
    color_counts = color_matches.sum(axis=0)
    return np.argmax(color_counts).astype(int)
Primitive(MostFrequentColor, 'Grid', 'Color')

def MostFrequentColorWithMask(args):
    grid, mask = args
    selected_colors = grid.ravel()[mask.ravel()]
    color_matches = selected_colors[:, None] == np.arange(10)[None,:]
    color_counts = color_matches.sum(axis=0)
    return np.argmax(color_counts).astype(int)
Primitive(MostFrequentColorWithMask, 'Grid', 'Mask', 'Color')

def ContractToMask(args):
    grid, mask = args
    h, w = mask.shape
    v_idxs = np.arange(h)[mask.sum(axis=1) > 0]
    h_idxs = np.arange(w)[mask.sum(axis=0) > 0]
    v_min, v_max = np.min(v_idxs), np.max(v_idxs)
    h_min, h_max = np.min(h_idxs), np.max(h_idxs)
    return grid[v_min:v_max+1, h_min:h_max+1]
Primitive(ContractToMask, 'Grid', 'Mask', 'Grid')

def HasBlackCell(args):
    grid, = args
    return (grid == np.zeros_like(grid)).any()
Primitive(HasBlackCell, 'Grid', 'Bool')

###############################################################################
# Higher Order Primitive Definitions
###############################################################################
def IfGridToGrid(args):
    state, predicate, if_true, if_false = args
    if predicate(state):
        if_true(state)
    else:
        if_false(state)
Primitive(IfGridToGrid, 'Grid', ['Grid', 'Bool'], ['Grid', 'Grid'], ['Grid', 'Grid'], 'Grid')


if __name__ == '__main__':
    for p in language:
        print(p.name)
        print(print_type(p.my_type))