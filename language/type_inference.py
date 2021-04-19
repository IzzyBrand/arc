""" Massachusetts Institute of Technology

Izzy Brand, 2021

Based on an implementation by Robert Smallshire
https://github.com/rob-smallshire/hindley-milner-python
"""


from language.ast import Identifier, Apply, Lambda, Let, Letrec
from language.types import *
from language.util import is_integer_literal, is_color_literal, InferenceError, ParseError


def analyse(node, env, non_generic=set(), parent_smush={}):
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
        return get_type(node.name, env, non_generic, parent_smush)

    elif isinstance(node, Apply):
        fun_type, fun_smush = analyse(node.fn, env, non_generic, parent_smush)
        arg_type, arg_smush = analyse(node.arg, env, non_generic, parent_smush)
        result_type = TypeVariable()
        res_smush = unify(Function(arg_type, result_type), fun_type, combine(fun_smush, arg_smush))
        return result_type, res_smush

    elif isinstance(node, Lambda):
        arg_type = TypeVariable()
        new_env = env.copy()
        new_env[node.v] = arg_type
        new_non_generic = non_generic.copy()
        new_non_generic.add(arg_type)
        result_type, body_smush = analyse(node.body, new_env, new_non_generic, parent_smush)
        return Function(arg_type, result_type), body_smush

    elif isinstance(node, Let):
        defn_type, defn_smush = analyse(node.defn, env, non_generic, parent_smush)
        new_env = env.copy()
        new_env[node.v] = defn_type
        body_type, body_smush = analyse(node.body, new_env, non_generic, parent_smush)
        return body_type, combine(defn_smush, body_smush)

    elif isinstance(node, Letrec):
        new_type = TypeVariable()
        new_env = env.copy()
        new_env[node.v] = new_type
        new_non_generic = non_generic.copy()
        new_non_generic.add(new_type)
        defn_type, defn_smush = analyse(node.defn, new_env, new_non_generic, parent_smush)
        new_defn_smush = unify(new_type, defn_type, defn_smush)
        body_type, body_smush = analyse(node.body, new_env, non_generic, combine(parent_smush, new_defn_smush))
        return body_type, combine(new_defn_smush, body_smush)

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
        # return lookup(env[name], smush)
        return fresh(env[name], non_generic, smush)
    elif is_integer_literal(name):
        return Integer, {}
    elif is_color_literal(name):
        return Color, {}
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
    new_smush = {}  # A mapping of TypeVariables to TypeVariables

    def freshrec(tp):
        p = lookup(tp, smush)
        if isinstance(p, TypeVariable):
            if occurs_in(p, non_generic, smush):
                # NOTE(izzy): non_generic type variables are ones that might be
                # defined recurslively. If p is being defined recursively, we do
                # not let it have multiple types within the defintion
                return p
            elif p not in new_smush:
                # NOTE(izzy): see http://lucacardelli.name/Papers/BasicTypechecking.pdf
                # bottom of page 10 for an explanation of why we do this. in short, if
                # p is a polymorphic type, we want to allow p to take on diffent types
                # in different contexts, so we give it a new typevariable
                new_smush[p] = TypeVariable()

            return new_smush[p]

        elif isinstance(p, TypeOperator):
            return TypeOperator(p.name, [freshrec(x) for x in p.types])

    return freshrec(t), new_smush


def unify(t1, t2, smush):
    """Unify the two types t1 and t2.

    Makes the types t1 and t2 the same.

    Args:
        t1: The first type to be made equivalent
        t2: The second type to be be equivalent

    Returns:
        smush

    Raises:
        InferenceError: Raised if the types cannot be unified.
    """

    a = lookup(t1, smush)
    b = lookup(t2, smush)
    new_smush = smush.copy()
    if isinstance(a, TypeVariable):
        if a != b:
            if occurs_in_type(a, b, new_smush):
                raise InferenceError("recursive unification")
            else: new_smush[a] = b
        return new_smush
    elif isinstance(a, TypeOperator) and isinstance(b, TypeVariable):
        return unify(b, a, new_smush)
    elif isinstance(a, TypeOperator) and isinstance(b, TypeOperator):
        if a.name != b.name or len(a.types) != len(b.types):
            raise InferenceError(f"Type mismatch: {a} != {b}")
        for p, q in zip(a.types, b.types):
            new_smush = unify(p, q, new_smush)
        return new_smush
    else:
        assert 0, "Not unified"


def combine(*smushes):
    new_smush = {}
    for smush in smushes:
        for k, v in smush.items():
            new_smush = unify(k, v, new_smush)
    return new_smush


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
