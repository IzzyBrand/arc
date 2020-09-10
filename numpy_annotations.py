""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""

import json
import numpy as np
from util import match

def func1_25d8a9c8(grid):
    return grid

def func2_25d8a9c8(grid):
    return grid

demo_programs = {
    '25d8a9c8': [func1_25d8a9c8, func2_25d8a9c8],

}

def test(task_name, func, subset='train'):
    with open(f'ARC/data/training/{task_name}.json') as f:
        j = json.load(f)

    correct = True
    for i, t in enumerate(j[subset]):
        input_grid = np.array(t['input'])
        pred = func(input_grid)
        target = np.array(t['output'])
        correct &= match(pred, target)

    return correct

if __name__ == '__main__':
    for task_name in demo_programs:
        for func in demo_programs[task_name]:
            train_correct = test(task_name, func, 'train')
            test_correct = test(task_name, func, 'test')
            print(f'{func.__name__}:\t Train: {train_correct}\tTrain: {test_correct}')