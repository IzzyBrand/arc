from type_inference import *

# make some type variables
var1 = TypeVariable()
HOLE = TypeVariable()

# define a type-environment
env = {
    "true": Bool,
    "cond": Function(Bool, Function(var1, Function(var1, var1))),
    "zero": Function(Integer, Bool),
    "pred": Function(Integer, Integer),
    "times": Function(Integer, Function(Integer, Integer)),
    "HOLE": HOLE,
}

# here's the program for factorial
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

# and here is the same program, but with "times" replaced by hole
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
                Apply(Identifier("HOLE"), Identifier("n")),
                Apply(
                    Identifier("factorial"), Apply(Identifier("pred"), Identifier("n"))
                ),
            ),
        ),
    ),  # in
    Apply(Identifier("factorial"), Identifier("5")),
)


# run type inference on the first program. this will return the type of the
# program, (t), aand dict I've decided to call smush, which is a mapping from
# type-variables to types. Look up (recursively) the type of the program in
# the smush via lookup(t, smush)
print(factorial_program)
t, smush = analyse(factorial_program, env)
for k,v in smush.items():
    print(f"{k} : {v}")
print(f"Result: type variable {t} has type {lookup(t, smush)}")

# the reason we return the smush, is so we can look up the type of other type
# variables as well. In this case we'll look up the type of HOLE
print(factorial_program_with_hole)
t, smush = analyse(factorial_program_with_hole, env)
for k,v in smush.items():
    print(f"{k} : {v}")
print(f"Result: type variable {t} has type {lookup(t, smush)}")
print(f"HOLE: type variable {HOLE} has type {lookup(HOLE, smush)}")

