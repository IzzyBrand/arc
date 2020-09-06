from primitives import *
from programs import Program
from util import *

demo_programs = {
    'ff805c23.json':
        (ContractToMask,
            (HFlip,
                VFlip),
            (MaskFromColor,
                PassGrid,
                Color_p(1))),
    '9ecd008a.json':
        (ContractToMask,
            (HFlip,
                VFlip),
            (MaskFromColor,
                PassGrid,
                Color_p(0))),
    '445eab21.json':
        (CreatePatch,
            Int_p(2),
            Int_p(2),
            (MostFrequentColorWithMask,
                PassGrid,
                (InvertMask,
                    (MaskFromColor,
                        PassGrid,
                        Color_p(0))))),
    # TODO(izzy): I misunderstood the rule when I glanced at the problem.
    # We don't have th primitives for this one yet
    'b548a754.json':
        (ColorGridWithMask,
            PassGrid,
            (MaskFromColor,
                PassGrid,
                Color_p(8)),
            Color_p(0)),
    # this one is a good exapmle of the value of for-loops, variables, and also
    # of recognizing the boarders of the grid. Notice all the repeated structure.
    'bc1d5164.json':
    (MaskedOverlay,
        (MaskedOverlay,
            (MaskedOverlay,
                (ExtractPatch,
                    PassGrid, Int_p(0), Int_p(0), Int_p(3), Int_p(3)),
                (ExtractPatch,
                    PassGrid, Int_p(0), Int_p(2), Int_p(3), Int_p(3)),
                (InvertMask,
                    (MaskFromColor,
                        (ExtractPatch,
                            PassGrid, Int_p(0), Int_p(2), Int_p(3), Int_p(3)),
                        Color_p(0)))),
            (ExtractPatch,
                PassGrid, Int_p(4), Int_p(0), Int_p(3), Int_p(3)),
            (InvertMask,
                (MaskFromColor,
                    (ExtractPatch,
                        PassGrid, Int_p(4), Int_p(0), Int_p(3), Int_p(3)),
                    Color_p(0)))),
        (ExtractPatch,
                PassGrid, Int_p(4), Int_p(2), Int_p(3), Int_p(3)),
        (InvertMask,
            (MaskFromColor,
                (ExtractPatch,
                    PassGrid, Int_p(4), Int_p(2), Int_p(3), Int_p(3)),
                Color_p(0))))
}


if __name__ == '__main__':
    for task_name in demo_programs:
        spec = demo_programs[task_name]
        P = Program(spec)
        if not P.type_check():
            print(f'The program for {task_name} failed type_check')
        print(f'{task_name}:\t{run_program_on_task_train(P, task_name)}')
