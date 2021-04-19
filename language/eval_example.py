from language.eval import eval
from language.ast import Identifier, Apply, Lambda, Let, Letrec

my_env = {"pred": lambda x: x - 1,
          "zero": lambda x: x == 0,
          "plus": lambda x: lambda y: x + y,
          "times": lambda x: lambda y: x * y,
          "eq": lambda x: lambda y: x == y,
          "cond": lambda pred: lambda x: lambda y: x if pred else y
}

one_plus_one = Apply(Apply(Identifier("plus"), Identifier("1")), Identifier("1"))

factorial_program = Letrec("factorial",  # letrec factorial =
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
    Apply(Identifier("factorial"), Identifier("5")))

# fact_body = Apply(
#               Apply(  # cond (zero n) 1
#                   Apply(Identifier("cond"),  # cond (zero n)
#                         Apply(Identifier("zero"), Identifier("0"))),
#                   Identifier("11")),
#               Identifier("10")
#           )

# print(one_plus_one)
# print(eval(one_plus_one, my_env))

print(factorial_program)
try:
    print(eval(factorial_program, my_env))
except Exception:
    print("blyat")
