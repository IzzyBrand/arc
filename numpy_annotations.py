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


demo_programs = {
    '25d8a9c8': [func1_25d8a9c8],
    '8d510a79': [func1_8d510a79],
    '253bf280': [func1_253bf280],
    '99b1bc43': [func1_99b1bc43],
    'beb8660c': [func1_beb8660c]
}

def test(task_name, func, subset='train'):
    with open(f'ARC/data/training/{task_name}.json') as f:
        j = json.load(f)

    correct = True
    for i, t in enumerate(j[subset]):
        input_grid = np.array(t['input'])
        pred = func(input_grid)
        # vis(pred)
        target = np.array(t['output'])
        correct &= match(pred, target)

    return correct


if __name__ == '__main__':
    for task_name in demo_programs:
        for func in demo_programs[task_name]:
            train_correct = test(task_name, func, 'train')
            test_correct = test(task_name, func, 'test')
            print(f'{func.__name__}:\t Train: {train_correct}\tTrain: {test_correct}')
