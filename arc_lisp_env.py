""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""
import numpy as np
import json
import os

def array_assign(*args):
    A = np.copy(args[0])
    A[tuple(args[1:-1])] = args[-1]
    return A

def make_grid(task_name, index=0, subset='train'):
	try:
		with open(f'ARC/data/training/{task_name}.json') as f:
			j = json.load(f)

		return np.array(j[subset][index]['input'])
	except:
		print("TypeError: invalid parameters for make_grid()")

extended_env = {
    'zeros_like': np.zeros_like,
    'logical_and': np.logical_and,
    'where': np.where,
	'array': lambda *x: np.array(list(x)),
    'array_assign': array_assign,
	'concat': lambda *x: np.concatenate(x[:-1], x[-1]) if type(x[-1]) is int else np.concatenate(x),
	'shape': np.shape,
    ':': slice(None),
    'slice': slice,
    'None': None,
    'map': map,
	'npmap': lambda foo, iter: np.array(list(map(foo, iter))),
	'min': min,
    'max': max,
    'set': set,
	'len': len,
    'make_grid': make_grid,
	'tuple': tuple,
}
