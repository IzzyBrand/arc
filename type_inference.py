""" Massachusetts Institute of Technology

Izzy Brand, 2021

Based on an implementation by Robert Smallshire
https://github.com/rob-smallshire/hindley-milner-python
"""

# =======================================================#
# Class definitions for the abstract syntax tree nodes
# which comprise the little language for which types
# will be inferred

class Lambda(object):
    """Lambda abstraction"""

    def __init__(self, v, body):
        self.v = v
        self.body = body

    def __str__(self):
        return f"(fn {self.v} => {self.body})"


class Identifier(object):
    """Identifier"""

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Apply(object):
    """Function application"""

    def __init__(self, fn, arg):
        self.fn = fn
        self.arg = arg

    def __str__(self):
        return f"({self.fn} {self.arg})"


class Let(object):
    """Let binding"""

    def __init__(self, v, defn, body):
        self.v = v
        self.defn = defn
        self.body = body

    def __str__(self):
        return f"(let {self.v} = {self.defn} in {self.body})"


class Letrec(object):
    """Letrec binding"""

    def __init__(self, v, defn, body):
        self.v = v
        self.defn = defn
        self.body = body

    def __str__(self):
        return f"(letrec {self.v} = {self.defn} in {self.body})"


# =======================================================#
# Exception types

class InferenceError(Exception):
    """Raised if the type inference algorithm cannot infer types successfully"""

    def __init__(self, message):
        self.__message = message

    message = property(lambda self: self.__message)

    def __str__(self):
        return str(self.message)


class ParseError(Exception):
    """Raised if the type environment supplied for is incomplete"""

    def __init__(self, message):
        self.__message = message

    message = property(lambda self: self.__message)

    def __str__(self):
        return str(self.message)


# =======================================================#
# Types and type constructors

class TypeVariable(object):
    """A type variable standing for an arbitrary type.

    All type variables have a unique id, but names are only assigned lazily,
    when required.
    """

    next_variable_id = 0
    next_variable_name = "T0"

    def __init__(self):
        self.id = TypeVariable.next_variable_id
        TypeVariable.next_variable_id += 1
        self.instance = None
        self.__name = None

    @property
    def name(self):
        """Names are allocated to TypeVariables lazily, so that only TypeVariables
        present after analysis consume names.
        """
        if self.__name is None:
            self.__name = TypeVariable.next_variable_name
            TypeVariable.next_variable_name = "T" +\
                str(int(TypeVariable.next_variable_name[1:]) + 1)

        return self.__name

    def __str__(self):
        if self.instance is not None:
            return str(self.instance)
        else:
            return self.name

    def __repr__(self):
        return f"TypeVariable(id = {self.id})"

    @classmethod
    def reset_counters():
        TypeVariable.next_variable_id = 0
        TypeVariable.next_variable_name = "T0"


class TypeOperator(object):
    """An n-ary type constructor which builds a new type from old"""

    def __init__(self, name, types):
        self.name = name
        self.types = types

    def __str__(self):
        num_types = len(self.types)
        if num_types == 0:
            return self.name
        elif num_types == 2:
            return f"({self.types[0]} {self.name} {self.types[1]})"
        else:
            return f"{self.name} {' '.join(self.types)}"


class Function(TypeOperator):
    """A binary type constructor which builds function types"""

    def __init__(self, from_type, to_type):
        super(Function, self).__init__("->", [from_type, to_type])


# Basic types are constructed with a nullary type constructor
Integer = TypeOperator("int", [])  # Basic integer
Bool = TypeOperator("bool", [])  # Basic bool


# =======================================================#
# Type inference machinery

def analyse(node, env, non_generic=set()):
    """Computes the type of the expression given by node.

    The type of the node is computed in the context of the
    supplied type environment env. Data types can be introduced into the
    language simply by having a predefined set of identifiers in the initial
    environment. environment; this way there is no need to change the syntax or, more
    importantly, the type-checking program when extending the language.

    Args:
        node: The root of the abstract syntax tree.
        env: The type environment is a mapping of expression identifier names
            to type assignments.
            to type assignments.
        non_generic: A set of non-generic variables, or None

    Returns:
        The computed type of the expression.

    Raises:
        InferenceError: The type of the expression could not be inferred, for example
            if it is not possible to unify two types such as Integer and Bool
        ParseError: The abstract syntax tree rooted at node could not be parsed
    """

    if isinstance(node, Identifier):
        return get_type(node.name, env, non_generic, {}), {}

    elif isinstance(node, Apply):
        fun_type, fun_smush = analyse(node.fn, env, non_generic)
        arg_type, arg_smush = analyse(node.arg, env, non_generic)
        result_type = TypeVariable()
        res_smush = unify(Function(arg_type, result_type), fun_type, combine(fun_smush, arg_smush))
        return result_type, res_smush

    elif isinstance(node, Lambda):
        arg_type = TypeVariable()
        new_env = env.copy()
        new_env[node.v] = arg_type
        new_non_generic = non_generic.copy()
        new_non_generic.add(arg_type)
        result_type, body_smush = analyse(node.body, new_env, new_non_generic)
        return Function(arg_type, result_type), body_smush

    elif isinstance(node, Let):
        defn_type, defn_smush = analyse(node.defn, env, non_generic)
        new_env = env.copy()
        new_env[node.v] = defn_type
        body_type, body_smush = analyse(node.body, new_env, non_generic)
        return body_type, combine(defn_smush, body_smush)

    elif isinstance(node, Letrec):
        new_type = TypeVariable()
        new_env = env.copy()
        new_env[node.v] = new_type
        new_non_generic = non_generic.copy()
        new_non_generic.add(new_type)
        defn_type, defn_smush = analyse(node.defn, new_env, new_non_generic)
        defn_smush = unify(new_type, defn_type, defn_smush)
        body_type, body_smush = analyse(node.body, new_env, non_generic)
        return body_type, combine(defn_smush, body_smush)

    assert 0, f"Unhandled syntax node {type(node)}"


def get_type(name, env, non_generic, smush):
    """Get the type of identifier name from the type environment env.

    Args:
        name: The identifier name
        env: The type environment mapping from identifier names to types
        non_generic: A set of non-generic TypeVariables

    Raises:
        ParseError: Raised if name is an undefined symbol in the type
            environment.
    """
    if name in env:
        return fresh(env[name], non_generic, smush)
    elif is_integer_literal(name):
        return Integer
    else:
        raise ParseError(f"Undefined symbol {name}")


def fresh(t, non_generic, smush):
    """Makes a copy of a type expression.

    The type t is copied. The the generic variables are duplicated and the
    non_generic variables are shared.

    Args:
        t: A type to be copied.
        non_generic: A set of non-generic TypeVariables
    """
    mappings = {}  # A mapping of TypeVariables to TypeVariables

    def freshrec(tp):
        p = lookup(tp, smush)
        if isinstance(p, TypeVariable):
            if not occurs_in(p, non_generic, smush):
                if p not in mappings:
                    mappings[p] = TypeVariable()
                return mappings[p]
            else:
                return p
        elif isinstance(p, TypeOperator):
            return TypeOperator(p.name, [freshrec(x) for x in p.types])

    return freshrec(t)


def unify(t1, t2, smush):
    """Unify the two types t1 and t2.

    Makes the types t1 and t2 the same.

    Args:
        t1: The first type to be made equivalent
        t2: The second type to be be equivalent

    Returns:
        None

    Raises:
        InferenceError: Raised if the types cannot be unified.
    """

    a = lookup(t1, smush)
    b = lookup(t2, smush)
    if isinstance(a, TypeVariable):
        if a != b:
            if occurs_in_type(a, b, smush):
                raise InferenceError("recursive unification")
            else: smush[a] = b
        return smush
    elif isinstance(a, TypeOperator) and isinstance(b, TypeVariable):
        return unify(b, a, smush)
    elif isinstance(a, TypeOperator) and isinstance(b, TypeOperator):
        if a.name != b.name or len(a.types) != len(b.types):
            raise InferenceError(f"Type mismatch: {a} != {b}")
        for p, q in zip(a.types, b.types):
            smush = unify(p, q, smush)
        return smush
    else:
        assert 0, "Not unified"


def combine(smush1, smush2):
    for k, v in smush1.items():
        smush2 = unify(k, v, smush2)
    return smush2


def lookup(a, smush):
    """Returns the currently defining instance of t.

    As a side effect, collapses the list of type instances. The function lookup
    is used whenever a type expression has to be inspected: it will always
    return a type expression which is either an uninstantiated type variable or
    a type operator; i.e. it will skip instantiated variables, and will
    actually lookup them from expressions to remove long chains of instantiated
    variables.

    Args:
        a: The type to be lookuped

    Returns:
        An uninstantiated TypeVariable or a TypeOperator
    """
    if isinstance(a, TypeOperator):
        return TypeOperator(a.name, [lookup(b, smush) for b in a.types])
    else:
        try: return lookup(smush[a], smush)
        except KeyError: return a

def occurs_in_type(v, type2, smush):
    """Checks whether a type variable occurs in a type expression.

    Note: Must be called with v pre-lookuped

    Args:
        v:  The TypeVariable to be tested for
        type2: The type in which to search

    Returns:
        True if v occurs in type2, otherwise False
    """
    lookuped_type2 = lookup(type2, smush)
    if lookuped_type2 == v:
        return True
    elif isinstance(lookuped_type2, TypeOperator):
        return occurs_in(v, lookuped_type2.types, smush)
    return False


def occurs_in(t, types, smush):
    """Checks whether a types variable occurs in any other types.

    Args:
        t:  The TypeVariable to be tested for
        types: The sequence of types in which to search

    Returns:
        True if t occurs in any of types, otherwise False
    """
    return any(occurs_in_type(t, t2, smush) for t2 in types)


def is_integer_literal(name):
    """Checks whether name is an integer literal string.

    Args:
        name: The identifier to check

    Returns:
        True if name is an integer literal, otherwise False
    """
    result = True
    try:
        int(name)
    except ValueError:
        result = False
    return result


# ==================================================================#
# Example code to exercise the above


def try_exp(env, node):
    """Try to evaluate a type printing the result or reporting errors.

    Args:
        env: The type environment in which to evaluate the expression.
        node: The root node of the abstract syntax tree of the expression.

    Returns:
        None
    """
    print(str(node) + " : ", end=' ')
    try:
        t, smush = analyse(node, env)
        print(lookup(t, smush))
    except (ParseError, InferenceError) as e:
        print(e)


def main():
    """The main example program.

    Sets up some predefined types using the type constructors TypeVariable,
    TypeOperator and Function.  Creates a list of example expressions to be
    evaluated. Evaluates the expressions, printing the type or errors arising
    from each.

    Returns:
        None
    """

    var1 = TypeVariable()
    var2 = TypeVariable()
    pair_type = TypeOperator("*", (var1, var2))

    var3 = TypeVariable()

    my_env = {"pair": Function(var1, Function(var2, pair_type)),
              "true": Bool,
              "cond": Function(Bool, Function(var3, Function(var3, var3))),
              "zero": Function(Integer, Bool),
              "pred": Function(Integer, Integer),
              "times": Function(Integer, Function(Integer, Integer))}

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
        Lambda("f", Lambda("g", Lambda("arg", Apply(Identifier("g"), Apply(Identifier("f"), Identifier("arg"))))))
    ]

    for example in examples:
        try_exp(my_env, example)


if __name__ == '__main__':
    main()
