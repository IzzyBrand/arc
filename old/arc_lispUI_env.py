import numpy as np
import json

def make_grid(task_name, index = 0, subset = 'train'):
	#try:
	with open(f'ARC/data/training/{task_name}.json') as f:
		j = json.load(f)

	return np.array(j[subset][index]['input'])
	# except:
	# 	print("TypeError: invalid parameters for make_grid()")
	# 	print("task: " + str(task_name) + "\tindex: " + str(index) + "\tsubset: " + str(subset))
	# 	print("types: " + str(type(task_name)))

UI_env = {
	'make_grid': make_grid,
	'ndarray': lambda *x: np.ndarray(list(x)),
}
