import numpy as np

from environment import typed_env
from lis import Env, parse
from type_check import type_check
from type_system import Type


test_programs = []
return_types = []

test_programs.append("0")
test_programs.append("(0)")
test_programs.append("(+ 1 1)")
test_programs.append("(+ grid 1)")
test_programs.append("(+ 1 grid)")
test_programs.append("(+ grid grid)")
test_programs.append("(== 1 1)")
test_programs.append("(== grid 1)")
test_programs.append("(== 1 grid)")
test_programs.append("(== grid grid)")

test_programs.append("(+ 1 1 1)")
test_programs.append("(== 1 +)")
test_programs.append("(== 1 (== 1 1))")


if __name__ == '__main__':
    env = Env(typed_env)
    env.update({'grid': np.random.randint(10, size=(3,3))})

    for test_program in test_programs:
        x = parse(test_program)
        pass_type_check, return_type, _ = type_check(x, env, False)
        print(f'Pass: {pass_type_check}\t Type: {str(return_type)}')
