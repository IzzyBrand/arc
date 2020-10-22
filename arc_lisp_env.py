import numpy as np

def array_assign(*args):
	A = np.copy(args[0])
	A[tuple(args[1:-1])] = args[-1]
	return A


extended_env = {
	'zeros_like': np.zeros_like,
	'logical_and': np.logical_and,
	'ndarray': lambda *x: np.ndarray(list(x)),
	'where': np.where,
	'array_assign': array_assign,
	':': slice(None),
	'slice': slice,
	'None': None,
	'map': map,
	'max': max,
	'set': set,

}
