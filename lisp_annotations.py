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
    (define blue_shift (- (min (blue_indices 0)) (+ 1 (max (blue_indices 0))))
        (define ret (zeros_like grid)
            (define ret (array_assign ret (+ blue_shift (blue_indices 0)) (blue_indices 1) 1)

                (define red_indices (where (== grid 2))
                    (define red_shift (- (min (red_indices 0)) (+ 1 (max (red_indices 0))))
                        (define ret (array_assign ret (+ red_shift (red_indices 0)) (red_indices 1) 2)

                            (define yellow_indices (where (== grid 4))
                                (define yellow_shift (- (min (yellow_indices 0)) (+ 1 (max (yellow_indices 0))))
                                    (array_assign ret (+ yellow_shift (yellow_indices 0)) (yellow_indices 1) 4)
)   )   )   )   )   )   )   )   )
"""

func2_5521c0d9 =\
"""
(define update (lambda (board color) (define indices (where (== grid color)) (define shift (- (min (indices 0)) (+ 1 (max (indices 0)))) (array_assign board (+ shift (indices 0)) (indices 1) color))))
    (define ret (zeros_like grid)
        (define ret (update ret 1)
            (define ret (update ret 2)
                (update ret 4)
)   )   )   )
"""

func1_46442a0e =\
"""
(define rotate (lambda (matrix index) (if (== index 1)(array_assign matrix : (- ((shape grid) 1) index) (grid (- index 1)))(rotate (array_assign matrix : (- ((shape grid) 1) index) (grid (- index 1))) (- index 1))))
    (define flip_col (lambda (matrix index) (if (== index 1) (array_assign matrix : (- index 1) ((matrix : (- index 1)) (slice None None -1))) (flip_col (array_assign matrix : (- index 1) ((matrix : (- index 1)) (slice None None -1))) (- index 1))))
        (define flip_row (lambda (matrix index) (if (== index 1) (array_assign matrix (- index 1) ((matrix (- index 1)) (slice None None -1))) (flip_row (array_assign matrix (- index 1) ((matrix (- index 1)) (slice None None -1))) (- index 1))))
            (define rot1 (rotate grid ((shape grid) 1))
                (define top (concat grid rot1 1)
                    (define bott (flip_row (flip_col top ((shape top) 1)) ((shape top) 0))
                        (concat top bott)
                    )
                )
            )
        )
    )
)
"""




demo_programs = {
    # '25d8a9c8': [func1_25d8a9c8],
    # '99b1bc43': [func1_99b1bc43],
    # '5521c0d9': [func1_5521c0d9, func2_5521c0d9],
    '46442a0e': [func1_46442a0e],
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
        #print(pred)
        vis(pred)
        target = np.array(t['output'])
        correct &= match(pred, target)

    return correct


if __name__ == '__main__':
    for task_name in demo_programs:
        for func_string in demo_programs[task_name]:
            train_correct = test(task_name, func_string, 'train')
            test_correct = test(task_name, func_string, 'test')
            print(f'{task_name}:\t Train: {train_correct}\tTest: {test_correct}')
