from types import *
from lis import Env, Procedure

TypeEnv(Env):
    pass


# NOTE(izzy): this is nowhere near done. just sketching some stuff out.
# feel free to change or improve
def eval_T(x, env_T):
    if isinstance(x, Symbol):      # variable reference
        return env_T.find(x)[x]

    elif not isinstance(x, List):  # constant literal
        return x.T

    elif x[0] == 'if':             # (if test conseq alt)
        # evaluate the types of each subtree of the if expression
        test_T, conseq_T, alt_T = (eval_T(i, env_T for i in x[1:]))
        assert test_T == bool_T, 'test must return a bool'
        assert conseq_T == alt_T, 'two branches must return the same type'
        return conset_T

    elif x[0] == 'define':         # (define var exp body)
        (_, var, exp, body) = x
        new_env_T = deepcopy(env)
        new_env_T[var] = eval_T(exp, new_env_T)
        return eval_T(body, env=new_env_T)

    # NOTE(izzy): all good
    elif x[0] == 'lambda':         # (lambda (var...) body)
        (_, parms, body) = x
        return Procedure(parms, body, env_T, func_string=str(x))

    # NOTE(izzy): all good, but I added a case to allow array indexing
    else:                          # (proc arg...)
        proc = eval_T(x[0], env_T)
        args = [eval_T(exp, env_T) for exp in x[1:]]

        if isinstance(proc, np.ndarray): return np.copy(proc[tuple(args)])
        elif isinstance(proc, tuple): return proc[args[0]]
        elif isinstance(proc, (Number, Symbol)): return proc
        else: return proc(*args)
