import json
import numpy as np
import os


class Program:
    def __init__(self, primitives=[]):
        # TODO(izzy): a program isn't necessarily sequential. This should be
        # replaced with a tree structure.
        self.primitives = []

    def type_check(self):
        is_valid = True

        # check that the spec matches from primitive to primitive
        prev_type = 'Grid'
        for primitive in self.primitives:
            is_valid &= (primitive.type[0] == prev_type)
            prev_type = primitive.type[-1]

        # and check that the output is a grid
        is_valid &= ('Grid' == prev_type)

        return is_valid

    def __call__(self, x):
        for primitive in self.primitives:
            x = primitive(x)

        return x

# a language primitive base class
class Primitive:
    def __init__(self, *args):
        self.params = args
        self.type = (None, None)

    def __call__(self, *args):
        return None

# a simple primitive that extracts patch
class PatchExtract(Primitive):
    def __init__(self, *args):
        self.params = args
        self.type = ('Grid', 'Grid')

    def __call__(self, *args):
        w, h, x, y = self.params
        input_grid = args[0]
        output_grid = input_grid[y:y+h, x:x+w]
        return output_grid


PRIMITIVES = [PatchExtract]


# the Learning agent capable of training on and evaluating ARC tasks
class Solver:

    def train(self, task_data):
        self.best_program = Program()
        self.best_program.primitives.append(PatchExtract(1,1,0,0))
        if not self.best_program.type_check():
            print('Type check failed!')

    def eval(self, task_input):
        grid = np.array(task_input, dtype=int)
        return self.best_program(grid)


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
        output = solver.eval(t['input'])
        label = np.array(t['output'], dtype=int)
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

    print(f'{score} out of {len(task_fnames)} correct')
