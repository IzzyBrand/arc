from copy import deepcopy
import numpy as np

from lis import global_env

choose = lambda x: np.random.choice(list(x))

def wrap_with_random_func(prog):
    func = choose(global_env.values())
    return [func, prog]

def replace_primitive(prog):
    new_func = choose(list(global_env.values()))
    if isinstance(prog, list):
        return [new_func] + prog[1:]
    else:
        return new_func

def add_arg(prog):
    if isinstance(prog, list):
        idx_to_add = np.random.randint(1, len(prog)+1)
        what_to_add = choose(['color', 'grid', 'number', 'None'])
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


def prog_len(prog):
    if isinstance(prog, list):
        return np.sum([prog_len(p) for p in prog])
    else:
        return 1

def modify(prog):
    # We don't want to always modify the top-level program, so we need to
    # recur down the program tree until we reach a subtree that we want to
    # modify.

    # NOTE(izzy): ideally the probability of changing a subtree should be
    # inversely proportional to its size as a fraction of the total program
    # size.
    if isinstance(prog, list):
        subtree_sizes = [prog_len(p) for p in prog]
        total_size = np.sum(subtree_sizes)
        # include the size of the total tree as the (n+1)th subtree, so
        #that if we pick the last element we'll just modify the whole tree
        subtree_sizes.append(total_size)
        p = total_size/np.array(subtree_sizes)
        i = np.random.choice(len(prog) + 1, p=p/p.sum())

        if i < len(prog):
            new_sub_prog = modify(prog[i])
            if new_sub_prog is None:
                return None # we failed to modify
            else:
                new_prog = deepcopy(prog)
                new_prog[i] = new_sub_prog
                return new_prog

    what_to_do = choose([wrap_with_random_func,
                         remove_arg,
                         add_arg,
                         replace_primitive])
    return what_to_do(prog)