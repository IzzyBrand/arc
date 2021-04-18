from type_inference import *

var1 = TypeVariable()
var2 = TypeVariable()
var3 = TypeVariable()
HOLE = TypeVariable()

env = {
    "true": Bool,
    "cond": Function(Bool, Function(var3, Function(var3, var3))),
    "zero": Function(Integer, Bool),
    "pred": Function(Integer, Integer),
    "times": Function(Integer, Function(Integer, Integer)),
    "HOLE": HOLE,
}


factorial_program = Letrec(
    "factorial",  # letrec factorial =
    Lambda(
        "n",  # fn n =>
        Apply(
            Apply(  # cond (zero n) 1
                Apply(
                    Identifier("cond"),  # cond (zero n)
                    Apply(Identifier("zero"), Identifier("n")),
                ),
                Identifier("1"),
            ),
            Apply(  # times n
                Apply(Identifier("times"), Identifier("n")),
                Apply(
                    Identifier("factorial"), Apply(Identifier("pred"), Identifier("n"))
                ),
            ),
        ),
    ),  # in
    Apply(Identifier("factorial"), Identifier("5")),
)


factorial_program_with_hole = Letrec(
    "factorial",  # letrec factorial =
    Lambda(
        "n",  # fn n =>
        Apply(
            Apply(  # cond (zero n) 1
                Apply(
                    Identifier("cond"),  # cond (zero n)
                    Apply(Identifier("zero"), Identifier("n")),
                ),
                Identifier("1"),
            ),
            Apply(  # times n. note that we've replaces times with HOLE
                Apply(Identifier("times"), Identifier("n")),
                Apply(
                    Identifier("factorial"), Apply(Identifier("pred"), Identifier("n"))
                ),
            ),
        ),
    ),  # in
    Apply(Identifier("factorial"), Identifier("5")),
)

print(factorial_program)
t, smush = analyse(factorial_program, env)
for k,v in smush.items():
    print(f"{k} : {v}")
print(f"Result: type variable {t} has type {lookup(t, smush)}")


print(factorial_program_with_hole)
t, smush = analyse(factorial_program, env)
for k,v in smush.items():
    print(f"{k} : {v}")
print(f"Result: type variable {t} has type {lookup(t, smush)}")
print(f"HOLE: type variable {HOLE} has type {lookup(HOLE, smush)}")

