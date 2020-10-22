""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""
import numpy as np
import os
import json

from lis import eval, lispstr, global_env
from lisp_annotations import test as lisp_test
from search.heuristics import score as heuristic_score
from search.modify import modify
from util import match, vis

def run_program_on_task(task_fname, prog, subset='train', score_func=match):
    with open(f'ARC/data/training/{task_fname}') as f:
        j = json.load(f)

    scores = []
    for i, t in enumerate(j[subset]):
        input_grid = np.array(t['input'])
        prog_with_input = ['define', 'grid', input_grid, prog]
        try:
            pred = eval(prog_with_input)
            target = np.array(t['output'])
            scores.append(score_func(pred, target))
        except Exception as e:
            # print(f'lisp_score: failed to evaluate program on {task_fname}', e)
            # print(lispstr(prog))
            scores.append(0)

    return np.mean(scores)

def prog_len(prog):
    if isinstance(prog, List):
        return np.sum([prog_len(p) for p in prog])
    else:
        return 1

def modify_pool(task_fname, pool, max_pool_size=100):
    prog = np.random.choice(pool)
    new_prog = modify(prog)
    if new_prog is None: return # in this case we haven't made any changes
    new_score = run_program_on_task(task_fname, prog, score_func=heuristic_score)

    # if we haven't reached the max pool size, add the program
    if len(pool) < max_pool_size:
        pool.append(new_prog)
    # if we have reached the max pool size, replace a program that the new
    # program outperforms. pick which program to replace randomly
    else:
        scores = np.array([run_program_on_task(task_fname, prog, score_func=heuristic_score)\
            for prog in pool])
        new_prog_is_better = new_score >= scores
        if new_prog_is_better.any():
            idx = np.random.choice(np.where(new_prog_is_better)[0])
            pool[idx] = new_prog

task_fname = np.random.choice(os.listdir('ARC/data/training'))
print(f'Working on task: {task_fname}')
# with open(f'ARC/data/training/{task_fname}') as f:
#     j = json.load(f)
#     vis(np.array(j['train'][0]['input']), block=False)
pool = ['grid']
high_score = 0
for i in range(10000):
    print(f'Iteration {i}\thigh score: {high_score}')
    modify_pool(task_fname, pool)

    # print if we've increased the high score
    scores = np.array([run_program_on_task(task_fname, prog, score_func=heuristic_score)\
        for prog in pool])
    best_score_idx = np.argmax(scores)
    if scores[best_score_idx] > high_score:
        high_score = scores[best_score_idx]
        print(f'New high score! {high_score}')
        print(lispstr(pool[best_score_idx]))