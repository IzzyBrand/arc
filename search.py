""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""
import numpy as np
from random import choices as sample_with_replacement

from primitives import language
from programs import SimpleSequentialProgram
from util import *

def eval(program, train_data):
    num_correct = 0
    score = 0

    for t in train_data:
        grid = np.array(t['input'], dtype=int)
        target = np.array(t['output'], dtype=int)
        pred = program(grid)

        num_correct += match(pred, target)
        score += heursitic_score(pred, target)

    return num_correct, score

def heursitic_score(pred, target):
    score = 0

    # same shapes
    if pred.shape == target.shape:
        score += 1

        # same structure (only valid if shapes same)
        if ((pred > 0) * (target > 0)).all():
            score += 1

    # same colors
    if set(pred.ravel()) == set(target.ravel()):
        score += 1

    return score

def sample_simple_sequential_program():
    # sample a program. Use rejection sampling to get a program
    # that type-checks successfully
    program_length = np.random.geometric(0.5)

    for _ in range(100):
        primitives = sample_with_replacement(language, k=program_length)
        program = SimpleSequentialProgram(primitives)
        if program.type_check():
            return program

    return None

def sample_params(param_types):
    if type(param_types) == list:
        return [sample_params(pt) for pt in param_types]
    elif param_types == 'Int':
        return np.random.geometric(0.5)
    elif param_types == 'Color':
        return np.random.randint(10)

def fit_params_simple_sequential_program(program, train_data):
    num_training_examples = len(train_data)
    # get the types of params for all the primitive in the program
    types = program.param_types
    # if the program doesn't already have param assignments, sample
    if not program.compiled:
        params = sample_params(types)
        program.compile(params)

    # sample random params, saving the best one until we get
    # a perfect fit
    best_score = 0
    best_params = params
    for _ in range(100):
        num_correct, score = eval(program, train_data)

        # if we've found params that work, we're done
        if num_correct == num_training_examples: break

        if score > best_score:
            best_score = score
            best_params = params

        params = sample_params(types)
        program.compile(params)

    return num_correct, score


def search_for_simple_sequential_program(train_data):
    candidate_programs = []
    correct_programs = []
    num_training_examples = len(train_data)

    for _ in range(100):
        # TODO(izzy): right now I'm just sampling a brand new program
        # every time and then fitting params every time and then leaving that
        # old program in the candidate_programs list. Really I should trade off
        # explore and exploit by revisiting and modifyig programs in the candidate
        # programs list. See brainstorming.md
        program = sample_simple_sequential_program()
        if program is None: continue

        num_correct, score = \
            fit_params_simple_sequential_program(program, train_data)

        candidate_programs.append((program, score))

        if num_correct == num_training_examples:
            print('Got One!')
            correct_programs.append(program)

    if len(correct_programs) > 0:
        correct_program_lengths = [len(P.primitives) for P in correct_programs]
        shortest_idx = np.argmin(correct_program_lengths)
        return correct_programs[shortest_idx]
    else:
        scores = [c[1] for c in candidate_programs]
        print('Best Score:', max(scores))
        best_idx = np.argmax(scores)
        return candidate_programs[best_idx][0]

