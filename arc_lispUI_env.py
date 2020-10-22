import numpy as np

def make_grid(task_name, index = 0, subset = 'train'):
	try:
		with open(f'/ARC/data/training/{task_name}.json') as f:
			j = json.load(f)

		return j[subset][index]['input']
	except:
		print("TypeError: invalid parameters for make_grid()")
		print("task: " + str(task_name) + "\tindex: " + str(index) + "\tsubset: " + str(subset))
		print("types: " + type(task_name))

UI_env = {
	'make_grid': make_grid,
}

print(make_grid("0a938d79"))
