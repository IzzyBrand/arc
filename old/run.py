""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""
import json
import numpy as np
import os

from search import search_for_simple_sequential_program

# the Learning agent capable of training on and evaluating ARC tasks
class Solver:

    def train(self, train_data):
        self.best_program = search_for_simple_sequential_program(train_data)

    def eval(self, task_input):
        grid = np.array(task_input, dtype=int)
        return self.best_program(grid)


def test(solver, test_data):
    """ Evaluate a trained solver on a task

    Returns true if at least one of the outputs was correct

    Arguments:
        solver {Solver} -- A trained instance of a Solver
        test_data {List(Dict)} -- The test list of an ARC task

    Returns:
        Bool -- At least one output was correct
    """
    num_correct = 0

    for t in test_data:
        output = solver.eval(t['input'])
        target = np.array(t['output'], dtype=int)
        correct  = (target.shape == output.shape) and (output == target).all()
        num_correct += correct

    return num_correct > 0


if __name__ == '__main__':
    score = 0

    task_dir = 'ARC/data/training'
    task_fnames = os.listdir(task_dir)
    for task_num, task_fname in enumerate(task_fnames):
        print(task_num, task_fname)
        with open(task_dir + '/' + task_fname) as f:
            task = json.load(f)

        s = Solver()
        s.train(task['train'])
        correct = test(s, task['test'])
        score += correct
        if correct:
            print('WOOOHOOO')

    print(f'{score} out of {len(task_fnames)} correct')
