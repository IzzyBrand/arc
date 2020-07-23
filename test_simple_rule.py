import json
import numpy as np
import os

class Solver:
    def train(self, task_data):
        pass

    def eval(self, task_input):
        return np.zeros([1,1])


def test(solver, task_data):
    """ Evaluate a trained solver on a task
    
    Returns true if at least one of the outputs was correct
    
    Arguments:
        solver {Solver} -- A trained instance of a Solver
        task_data {List(Dict)} -- The test list of an ARC task
    
    Returns:
        Bool -- At least one output was correct
    """
    num_correct = 0
    for t in task_data:
        label = np.array(t['output'], dtype=int)
        output = solver.eval(t['input'])
        correct  = (label.shape == output.shape) and (output == label).all()
        num_correct += correct

    return num_correct > 0


if __name__ == '__main__':
    score = 0

    task_dir = 'ARC/data/training'
    task_fnames = os.listdir(task_dir)
    for task_fname in task_fnames:
        with open(task_dir + '/' + task_fname) as f: 
            task = json.load(f)

        s = Solver()
        s.train(task['train'])
        correct = test(s, task['test'])
        score += correct
        if correct:
            print(task_fname)

    print(f'{score} out of {len(task_fnames)} correct')
        