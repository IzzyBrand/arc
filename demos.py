from primitives import *
from programs import TreeStructuredProgram
from util import *

demo_programs = {
 "ff805c23.json": 
     (Contract,
        (HFlip, VFlip),
        (ColorMask,
            PassGrid, 
            Color_p(1))
    )
}

if __name__ == '__main__':
    for task_name in demo_programs:
        spec = demo_programs[task_name]
        P = TreeStructuredProgram(spec)
        assert P.type_check(), f'The program for {task_name} failed type_check'
        print(f'{task_name}:\t{run_program_on_task_train(P, task_name)}')