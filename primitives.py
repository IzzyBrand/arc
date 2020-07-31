""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""

import numpy as np
from util import *
# a list of all the primitives
language = set()

class Primitive:
    def __init__(self, func, *my_type):
        self.func = func
        assert func.__name__.startswith('func'), 'Primitive naming convention violation'
        self.name = func.__name__.strip('func')
        self.my_type = my_type
        self.type_check = lambda: True
        language.add(self)

    def eval(self, x):
        return self.func(x)

def Int_p(i):
    assert isinstance(i, int)
    def tempFunc(args):
        return i
    tempFunc.__name__ = f'funcInt_{i}'
    return Primitive(tempFunc, 'Int')

def Color_p(i):
    assert isinstance(i, int)
    assert i >= 0 and i <= 10
    def tempFunc(args):
        return i
    tempFunc.__name__ = f'funcColor_{i}'
    return Primitive(tempFunc, 'Color')

def SizeOneGrid_p(i):
    assert isinstance(i, int)
    assert i >= 0 and i <= 10
    def tempFunc(args):
        return np.array([[i]])
    tempFunc.__name__ = f'funcSizeOneGrid_{i}'
    return Primitive(tempFunc, 'Grid')

###############################################################################
# Primitive Definitions
###############################################################################

# these four primitives are the identity
def funcPassGrid(args):
    return args
PassGrid = Primitive(funcPassGrid, 'Grid', 'Grid')

def funcPassInt(args):
    return args
PassInt = Primitive(funcPassInt, 'Int', 'Int')

def funcPassMask(args):
    return args
PassMask = Primitive(funcPassMask, 'Mask', 'Mask')

def funcPassColor(args):
    return args
PassColor = Primitive(funcPassColor, 'Color', 'Color')

# primtiives which operate on grids, masks and shapes
def funcVFlip(args):
    grid, = args
    return np.flip(grid, axis=0)
VFlip = Primitive(funcVFlip, 'Grid', 'Grid')

def funcHFlip(args):
    grid, = args
    return np.flip(grid, axis=1)
HFlip = Primitive(funcHFlip, 'Grid', 'Grid')

def funcEqualGrid(args):
    grid1, grid2 = args
    return grid1 == grid2
EqualGrid = Primitive(funcEqualGrid, 'Grid', 'Grid', 'Mask')

def funcInvertMask(args):
    mask, = args
    return (1 - mask).astype(bool)
InvertMask = Primitive(funcInvertMask, 'Mask', 'Mask')

def funcTile(args):
    grid, x, y
    return np.tile(grid, (y, x))
Tile = Primitive(funcTile, 'Grid', 'Int', 'Int', 'Grid')

def funcExtractPatch(args):
    grid, x, y, w, h = args
    # TODO(izzy): at some point we'll have to be smarter about selecting
    # indices and dimensions. for the minute, we'll just pretend the function
    # is a no-op if dimensions are invalie
    try:
        return grid[y:y+h, x:x+w]
    except IndexError:
        return grid
ExtractPatch = Primitive(funcExtractPatch, 'Grid', 'Int', 'Int', 'Int', 'Int', 'Grid')

def funcCreatePatch(args):
    w, h, color = args
    return np.ones([h,w]) * color
CreatePatch = Primitive(funcCreatePatch, 'Int', 'Int', 'Color', 'Grid')

def funcMaskFromColor(args):
    grid, color = args
    return grid == np.ones_like(grid)*color
MaskFromColor = Primitive(funcMaskFromColor, 'Grid', 'Color', 'Mask')

def funcCreateGridFromMask(args):
    mask, color = args
    return mask*color
CreateGridFromMask = Primitive(funcCreateGridFromMask, 'Mask', 'Color', 'Grid')

def funcColorGridWithMask(args):
    grid, mask, color = args
    return grid*(1-mask) + mask*color
ColorGridWithMask = Primitive(funcColorGridWithMask, 'Grid', 'Mask', 'Color', 'Grid')

def funcMaskedOverlay(args):
    grid1, grid2, mask = args
    return grid1*(1-mask) + grid2*mask
MaskedOverlay = Primitive(funcMaskedOverlay, 'Grid', 'Grid', 'Mask', 'Grid')

def funcCountColor(args):
    grid, color = args
    return (grid == color).sum()
CountColor = Primitive(funcCountColor, 'Grid', 'Color', 'Int')

def funcMostFrequentColor(args):
    grid, = args
    color_matches = grid.ravel()[:, None] == np.arange(10)[None,:]
    color_counts = color_matches.sum(axis=0)
    return np.argmax(color_counts).astype(int)
MostFrequentColor = Primitive(funcMostFrequentColor, 'Grid', 'Color')

def funcMostFrequentColorWithMask(args):
    grid, mask = args
    selected_colors = grid.ravel()[mask.ravel()]
    color_matches = selected_colors[:, None] == np.arange(10)[None,:]
    color_counts = color_matches.sum(axis=0)
    return np.argmax(color_counts).astype(int)
MostFrequentColorWithMask = Primitive(funcMostFrequentColorWithMask, 'Grid', 'Mask', 'Color')

def funcContractToMask(args):
    grid, mask = args
    h, w = mask.shape
    v_idxs = np.arange(h)[mask.sum(axis=1) > 0]
    h_idxs = np.arange(w)[mask.sum(axis=0) > 0]
    v_min, v_max = np.min(v_idxs), np.max(v_idxs)
    h_min, h_max = np.min(h_idxs), np.max(h_idxs)
    return grid[v_min:v_max+1, h_min:h_max+1]
ContractToMask = Primitive(funcContractToMask, 'Grid', 'Mask', 'Grid')

def funcHasBlackCell(args):
    grid, = args
    return (grid == np.zeros_like(grid)).any()
HasBlackCell = Primitive(funcHasBlackCell, 'Grid', 'Bool')

###############################################################################
# Higher Order Primitive Definitions
###############################################################################
def funcIfGridToGrid(args):
    state, predicate, if_true, if_false = args
    if predicate(state):
        if_true(state)
    else:
        if_false(state)
IfGridToGrid = Primitive(funcIfGridToGrid, 'Grid', ('Grid', 'Bool'), ('Grid', 'Grid'), ('Grid', 'Grid'), 'Grid')


if __name__ == '__main__':
    for p in language:
        print(p.name)
        print(str_type(p.my_type))