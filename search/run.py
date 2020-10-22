""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""
import numpy as np
import os
import json

from lis import eval, lispstr, global_env
from lisp_annotations import test as lisp_test
from search.heuristics import score as heuristic_score
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

def wrap_with_random_func(prog):
    func = np.random.choice(list(global_env.values()))
    return [func, prog]

def add_arg(prog):
    if isinstance(prog, list):
        idx_to_add = np.random.randint(1, len(prog)+1)
        what_to_add = np.random.choice(['color', 'grid', 'number', 'None'])
        if what_to_add == 'color':
            new_thing = np.random.randint(10)
        elif what_to_add == 'grid':
            new_thing = 'grid'
        elif what_to_add == 'number':
            new_thing = np.random.geometric(0.5)
        elif what_to_add == 'None':
            new_thing = None
        return prog[:idx_to_add] + [new_thing] + prog[idx_to_add:]
    else:
        return None

def remove_arg(prog):
    if isinstance(prog, list) and len(prog) > 1:
        idx_to_remove = np.random.randint(1, len(prog))
        return [p for i, p in enumerate(prog) if i != idx_to_remove]
    else:
        return None

def modify(prog):
    what_to_do = np.random.choice([wrap_with_random_func, remove_arg, add_arg])
    return what_to_do(prog)


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

task_fnames = os.listdir('ARC/data/training')
for task_fname in task_fnames:
    print(f'Working on task: {task_fname}')
    with open(f'ARC/data/training/{task_fname}') as f:
        j = json.load(f)
        vis(np.array(j['train'][0]['input']), block=False)
    pool = ['grid']
    for _ in range(10000):
        modify_pool(task_fname, pool)