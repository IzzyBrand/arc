import numpy as np

from environment import typed_env
from lis import Env, parse
from type_check import type_check
from type_system import Type


test_programs = []
return_types = []

test_programs.append("0")
test_programs.append("(0)")
test_programs.append("grid")
test_programs.append("bool_grid")
test_programs.append("row")
test_programs.append("(+ 1 1)")
test_programs.append("(+ grid 1)")
test_programs.append("(+ 1 grid)")
test_programs.append("(+ grid grid)")
test_programs.append("(== 1 1)")
test_programs.append("(== grid 1)")
test_programs.append("(== 1 grid)")
test_programs.append("(== grid grid)")
test_programs.append("make_slice")
test_programs.append("(make_slice 1 -1)")
test_programs.append("(index grid (make_slice 1 -1))")
test_programs.append("(index grid 1)")

# test_programs.append("(+ 1 1 1)")
# test_programs.append("(== 1 +)")
# test_programs.append("(== 1 (== 1 1))")


def test_a_real_lisp_annotation():
    test_program = """
    (define row_mask (logical_and
            (== (index (transpose grid) 0) (index (transpose grid) 1))
            (== (index (transpose grid) 1) (index (transpose grid) 2)))
        (array_assign (zeros_like grid) (array_to_slice row_mask) 5)
    )
    """
    with open('ARC/data/training/25d8a9c8.json') as f:
        j = json.load(f)

    env = Env(typed_env)
    env.update({'grid': np.array(j['train'][0]['input'])})

    x = parse(test_program)
    pass_type_check, return_type, _ = type_check(x, env, False)
    print(f'Pass: {pass_type_check}\t Type: {str(return_type)}')

    pred = eval(x, env=env)


if __name__ == '__main__':
    env = Env(typed_env)
    env.update({'grid': np.random.randint(10, size=(3,3))})
    env.update({'row': np.random.randint(10, size=3)})
    env.update({'bool_grid': np.random.randint(1, size=(3,3), dtype=bool)})

    for test_program in test_programs:
        x = parse(test_program)
        pass_type_check, return_type, _ = type_check(x, env, False)
        print(f'Pass: {pass_type_check}\t Type: {str(return_type)}')
