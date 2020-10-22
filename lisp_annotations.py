""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""
import json
import numpy as np
from util import match, vis
from lis import parse, eval

func1_25d8a9c8 =\
"""
(define row_mask (logical_and
        (== (grid : 0) (grid : 1))
        (== (grid : 1) (grid : 2)))
    (array_assign (zeros_like grid) row_mask : 5)
)
"""

func1_99b1bc43 =\
"""
(define sum_grid (+
        (grid (slice None 4))
        (grid (slice -4 None)))
(define mask_grid (logical_and
        (> sum_grid 0)
        (< sum_grid 3))
    (* mask_grid 3)
))
"""

func1_5521c0d9 =\
"""
(define blue_indices (where (== grid 1))
    (define blue_height (- (+ 1 (max (blue_indices 0))) (min (blue_indices 0)))
        blue_height
    )
)
"""
# (define red_indices (where (== grid 2))
#     (define yell_indices (where (== grid 4))
#         ()
#     )
# )


demo_programs = {
    #'25d8a9c8': [func1_25d8a9c8],
    #'99b1bc43': [func1_99b1bc43],
    '5521c0d9': [func1_5521c0d9],
}


def test(task_name, func_string, subset='train'):
    with open(f'ARC/data/training/{task_name}.json') as f:
        j = json.load(f)

    prog = parse(func_string)


    correct = True
    for i, t in enumerate(j[subset]):
        input_grid = np.array(t['input'])
        prog_with_input = ['define', 'grid', input_grid, prog]
        pred = eval(prog_with_input)
        print(pred)
        # vis(pred)
        target = np.array(t['output'])
        correct &= match(pred, target)

    return correct


if __name__ == '__main__':
    for task_name in demo_programs:
        for func_string in demo_programs[task_name]:
            train_correct = test(task_name, func_string, 'train')
            test_correct = test(task_name, func_string, 'test')
            print(f'{task_name}:\t Train: {train_correct}\tTrain: {test_correct}')
