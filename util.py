import json
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

# I grabbed this colormap from the CSS on the ARC website.
cmap = ListedColormap([
    "#000000",
    "#0074D9",
    "#FF4136",
    "#2ECC40",
    "#FFDC00",
    "#AAAAAA",
    "#F012BE",
    "#FF851B",
    "#7FDBFF",
    "#870C25"])

imshow_kwargs = {
    'cmap': cmap,
    'interpolation': 'nearest',
    'vmin': 0,
    'vmax': 9
}



def item(x):
    if isinstance(x, (list, tuple)) and len(x) == 1:
        return x[0]
    else:
        return x

def str_type(my_type, input_only=False):
    if isinstance(my_type, (list, tuple)):
        if len(my_type) == 1:
            return my_type[0]
        if input_only:
            return '('+', '.join([str_type(x) for x in my_type])+')'
        else:
            return '(' + ', '.join([str_type(x) for x in my_type[:-1]]) + ' -> ' + str_type(my_type[-1]) + ')'
    else:
        return my_type

def match(pred, target):
    return pred.shape == target.shape and (pred == target).all()

def str_primitive_or_program(p):
    if hasattr(p, 'name'): return p.name
    else: return str(p)

def eval_primitive_or_program(p, x):
    if hasattr(p, 'eval'): return p.eval(x)
    else: return p(x)

def run_program_on_task_train(program, task_name, vis=True):
    with open(f'ARC/data/training/{task_name}') as f:
        j = json.load(f)

    score = 0
    if vis:
        n = len(j['train'])
        fig, axarr = plt.subplots(n,3)

    for i, t in enumerate(j['train']):
        input_grid = np.array(t['input'])
        pred = program.eval(input_grid)
        target = np.array(t['output'])
        score += match(pred, target)
        if vis:
            axarr[i,0].imshow(input_grid, **imshow_kwargs)
            axarr[i,1].imshow(pred, **imshow_kwargs)
            axarr[i,2].imshow(target, **imshow_kwargs)

    if vis: plt.show()

    return float(score)/len(j['train'])
