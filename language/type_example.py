from language.ast import *
from language.types import *
from language.type_inference import *


var1 = TypeVariable()
var2 = TypeVariable()
var3 = TypeVariable()

pair_type = TypeOperator("*", (var1, var2))

HOLE = TypeVariable()


my_env = {"pair": Function(var1, Function(var2, pair_type)),
          "true": Bool,
          "cond": Function(Bool, Function(var3, Function(var3, var3))),
          "zero": Function(Integer, Bool),
          "pred": Function(Integer, Integer),
          "times": Function(Integer, Function(Integer, Integer)),
          "plus": Function(Integer, Function(Integer, Integer)),
          "HOLE": HOLE}

pair = Apply(Apply(Identifier("pair"),
                   Apply(Identifier("f"),
                         Identifier("4"))),
             Apply(Identifier("f"),
                   Identifier("true")))

examples = [
    # factorial
    Letrec("factorial",  # letrec factorial =
           Lambda("n",  # fn n =>
                  Apply(
                      Apply(  # cond (zero n) 1
                          Apply(Identifier("cond"),  # cond (zero n)
                                Apply(Identifier("zero"), Identifier("n"))),
                          Identifier("1")),
                      Apply(  # times n
                          Apply(Identifier("times"), Identifier("n")),
                          Apply(Identifier("factorial"),
                                Apply(Identifier("pred"), Identifier("n")))
                      )
                  )
                  ),  # in
           Apply(Identifier("factorial"), Identifier("5"))
           ),

    # Should fail:
    # fn x => (pair(x(3) (x(true)))
    Lambda("x",
           Apply(
               Apply(Identifier("pair"),
                     Apply(Identifier("x"), Identifier("3"))),
               Apply(Identifier("x"), Identifier("true")))),

    # Should fail:
    Lambda("x",
        Let("y", Identifier("x"),
           Apply(
               Apply(Identifier("pair"),
                     Apply(Identifier("y"), Identifier("3"))),
               Apply(Identifier("y"), Identifier("true"))))),

    # Should fail
    Lambda("x",
        Let("y", Lambda("z", Apply(Identifier("x"), Identifier("z"))),
           Apply(
               Apply(Identifier("pair"),
                     Apply(Identifier("y"), Identifier("3"))),
               Apply(Identifier("y"), Identifier("true"))))),

    # pair(f(3), f(true))
    Apply(
        Apply(Identifier("pair"), Apply(Identifier("f"), Identifier("4"))),
        Apply(Identifier("f"), Identifier("true"))),

    # let f = (fn x => x) in ((pair (f 4)) (f true))
    Let("f", Lambda("x", Identifier("x")), pair),

    # fn f => f f (fail)
    Lambda("f", Apply(Identifier("f"), Identifier("f"))),

    # let g = fn f => 5 in g g
    Let("g",
        Lambda("f", Identifier("5")),
        Apply(Identifier("g"), Identifier("g"))),

    # example that demonstrates generic and non-generic variables:
    # fn g => let f = fn x => g in pair (f 3, f true)
    Lambda("g",
           Let("f",
               Lambda("x", Identifier("g")),
               Apply(
                   Apply(Identifier("pair"),
                         Apply(Identifier("f"), Identifier("3"))
                         ),
                   Apply(Identifier("f"), Identifier("true"))))),

    # Function composition
    # fn f (fn g (fn arg (f g arg)))
    Lambda("f", Lambda("g", Lambda("arg", Apply(Identifier("g"), Apply(Identifier("f"), Identifier("arg")))))),

    Letrec("fib",  # letrec factorial =
           Lambda("n",  # fn n =>
                  Apply(
                      Apply(  # cond (zero n) 1
                          Apply(Identifier("cond"),  # cond (zero n)
                                Apply(Identifier("zero"), Identifier("n"))),
                          Identifier("1")),
                      Apply(  # times n
                          Apply(Identifier("plus"), Apply(Identifier("fib"),
                                Apply(Identifier("pred"), Identifier("n")))),
                          Apply(Identifier("fib"),
                                Apply(Identifier("pred"),
                                    Apply(Identifier("pred"), Identifier("n"))))
                      )
                  )
                  ),  # in
           Apply(Identifier("fib"), Identifier("5"))
           ),

    # tictoc (mutual recursion)
    Letrec("tic",  # letrec tic =
           Lambda("n",  # fn n =>
                  Apply(Apply(Apply(
                    Identifier("cond"), Apply(Identifier("zero"), Identifier("n"))),
                    Identifier("0")),
                     Letrec("toc",  # letrec tic =
                       Lambda("n",  # fn n =>
                              Apply(Apply(Apply(
                                Identifier("cond"), Apply(Identifier("zero"), Identifier("n"))),
                                Identifier("1")),
                                Apply(Identifier("tic"), Apply(Identifier("pred"), Identifier("n")))
                              )
                              ),  # in
                       Apply(Identifier("tic"), Identifier("5"))
                       )
                  )
                  ),  # in
           Apply(Identifier("tic"), Identifier("5"))
           ),
]

# here's the program for factorial
factorial_program = examples[0]

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


def test_holes():
    # run type inference on the first program. this will return the type of the
    # program, (t), and a dict I've decided to call smush, which is a mapping from
    # type-variables to types. Look up (recursively) the type of the program in
    # the smush via lookup(t, smush)
    print(factorial_program)
    t, smush = analyse(factorial_program, my_env)
    for k,v in smush.items():
        print(f"{k} : {v}")
    print(f"Result: type variable {t} has type {lookup(t, smush)}")

    # the reason we return the smush, is so we can look up the type of other type
    # variables as well. In this case we'll look up the type of HOLE
    print(factorial_program_with_hole)
    t, smush = analyse(factorial_program_with_hole, my_env)
    for k,v in smush.items():
        print(f"{k} : {v}")
    print(f"Result: type variable {t} has type {lookup(t, smush)}")
    print(f"HOLE: type variable {HOLE} has type {lookup(HOLE, smush)}")


def run_examples():
    """The main example program.

    Sets up some predefined types using the type constructors TypeVariable,
    TypeOperator and Function.  Creates a list of example expressions to be
    evaluated. Evaluates the expressions, printing the type or errors arising
    from each.

    Returns:
        None
    """

    for example in examples:

        print(str(example) + " : ", end=' ')
        try:
            t, smush = analyse(example, my_env)
            print(lookup(t, smush))
            # print("Smush")
            # for k,v in smush.items():
            #     print(f"\t{k} : {v}")
        except (ParseError, InferenceError) as e:
            print(e)


if __name__ == '__main__':
    run_examples()
    test_holes()
