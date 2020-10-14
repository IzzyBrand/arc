""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""

import json
import numpy as np
from util import match, vis

def func1_25d8a9c8(grid):
    # create an empty output grid
    output = np.zeros_like(grid)
    # find out which rows are all the same
    row_mask = (grid[:,0] == grid[:,1]) * (grid[:,1] == grid[:,2])
    # and set those rows to be gray
    output[row_mask,:] = 5
    return output

def func1_8d510a79(grid):
    # the index of the first gray row
    gray_index = np.array(np.nonzero(grid == 5))[0,0]
    # get the indices of the red and blue pixels
    red_indices =  np.array(np.nonzero(grid == 2)).T
    blue_indices =  np.array(np.nonzero(grid == 1)).T
    # copy the output from the input
    output = grid
    # set the pixels between the red pixels and the bar to be red
    for i, j in red_indices:
        start_index = min(gray_index, i)
        end_index = max(gray_index, i)
        output[start_index+1:end_index, j] = 2

    # set the pixels between the blue pixels and the edge to be blue
    for i, j in blue_indices:
        start_index = 0 if i < gray_index else i
        end_index = grid.shape[0] if i > gray_index else i
        output[start_index:end_index, j] = 1

    return output

def func1_253bf280(grid):
    output = grid
    blue_indices =  np.array(np.nonzero(grid == 8)).T
    for i1, j1 in blue_indices:
        for i2, j2 in blue_indices:
            if i1 == i2:
                start_index = min(j1, j2) + 1
                end_index = max(j1, j2)
                output[i1,start_index:end_index] = 3
            if j1 == j2:
                start_index = min(i1, i2) + 1
                end_index = max(i1, i2)
                output[start_index:end_index, j1] = 3

    return output


def func1_99b1bc43(grid):
    sum_grid = grid[:4] + grid[-4:]
    mask_grid = (sum_grid > 0) * (sum_grid < 3)
    output = mask_grid * 3
    return output

def func1_beb8660c(grid):
    colors = []
    counts = []
    # go through the rows. if they have a colored stripe,
    # record the color and how many cells are in the stripe
    for row in grid:
        count = (row > 0).sum()
        if count > 0:
            row_color = row[row > 0][0]
            colors.append(row_color)
            counts.append(count)

    # sort the two lists by the counts
    sorted_idx = np.argsort(counts)
    counts = np.array(counts)[sorted_idx]
    colors = np.array(colors)[sorted_idx]
    # make a black output grid
    output = np.zeros_like(grid)
    for i, (count, color) in enumerate(zip(counts, colors)):
        row_idx = i + grid.shape[0] - colors.shape[0]
        output[row_idx, -count:] = color

    return output

def func1_a2fd1cf0(grid):
    green = np.array(np.where(grid == 3))
    red = np.array(np.where(grid == 2))
    print(red.shape)
    print(green)
    output = np.copy(grid)

    #red aboce green
    if green[0,0] > red[0,0]:
        for y in range(red[0,0] + 1, green[0, 0]):
            output[y, green[1,0]] = 8
    #green above red
    elif green[0,0] < red[0,0]:
        for y in range(green[0,0] + 1, red[0,0]):
            output[y, green[1,0]] = 8
    #red right of green
    if red[1,0] > green[1,0]:
        for x in range(green[1,0] + 1, red[1,0]):
            output[red[0,0], x] = 8
    #red left of green
    elif red[1,0] < green[1,0]:
        for x in range(red[1,0] + 1, green[1,0]):
            output[red[0,0], x] = 8
    #if not same column and not same row, add the "connection joint"
    if not red[0,0] == green[0,0] and not red[1,0] == green[1,0]:
        output[red[0,0], green[1,0]] = 8

    return output

def func1_6430c8c4(grid):
    #get top and lower halves, then combine
    grid1 = grid[0:4]
    grid2 = grid[5:]
    comb = grid1+grid2
    #get blank spots, and make resultant blank board
    black = np.array(np.where(comb == 0))
    res = np.zeros_like(comb)
    #fill spots where both grid1 and grid2 have a hole (0s in comb)
    for i in range(len(black[0])):
        res[black[0][i],black[1][i]] = 3

    return res

def func1_6aa20dc0(grid):
    modeTup, vals = get_mode(grid)
    mode = modeTup[0][0]
    edges = []
    filler = int()

    for v in vals.values():
        if len(v) == 2:
            edges = v
            break

    locs0 = np.array(np.where(grid == edges[0]))
    locs1 = np.array(np.where(grid == edges[1]))



def find_nearest(grid, loc, clr):
    '''Returns coordinates of pixel nearest the given location
    that is the given'''
    row, col = loc

    height = len(grid)
    width = len(grid[0])

    inSq = True
    r = 1

    while inSq:

        leftBound = col - r if col >= r else None
        rightBound = col + r if col + r < width else None
        upBound = row - r if row >= r else None
        downBound = row + r if row + r < height else None

        toCheck = [lambda d: i in -d:d+1 if i >= 0 and i < ]


        if leftBound is None and rightBound is None and upBound is None and downBound is None:
            return None

        if




def get_mode(grid):
    '''Gets the background pixel of an image '''
    '''Returns Tuple where first element is tuple of
    ([mode color(s)], frequency) and second element is
    dictionary mapping {frequencies: [color(s)]}'''
    '''Thought it'd be useful to map frequencies to colors
    to make sorting for highest frequency easier'''

    freqs = dict() #maps colors to frequencies

    for c in range(10):
        locs = np.array(np.where(grid == c))
        f = len(locs[0])
        if f in freqs.keys():
            freqs[f].append(c)
        else:
            freqs[f] = [c]

    modeFreq = max(freqs.keys())
    mode = freqs[modeFreq]

    return ((mode, modeFreq), freqs)


demo_programs = {
    # '25d8a9c8': [func1_25d8a9c8],
    # '8d510a79': [func1_8d510a79],
    # '253bf280': [func1_253bf280],
    # '99b1bc43': [func1_99b1bc43],
    # 'beb8660c': [func1_beb8660c],
    #'a2fd1cf0': [func1_a2fd1cf0],
    '6430c8c4': [func1_6430c8c4],
}

def test(task_name, func, subset='train'):
    with open(f'ARC/data/training/{task_name}.json') as f:
        j = json.load(f)

    correct = True
    for i, t in enumerate(j[subset]):
        input_grid = np.array(t['input'])
        pred = func(input_grid)
        vis(pred)
        target = np.array(t['output'])
        correct &= match(pred, target)

    return correct


if __name__ == '__main__':
    for task_name in demo_programs:
        for func in demo_programs[task_name]:
            train_correct = test(task_name, func, 'train')
            test_correct = test(task_name, func, 'test')
            print(f'{func.__name__}:\t Train: {train_correct}\tTrain: {test_correct}')
