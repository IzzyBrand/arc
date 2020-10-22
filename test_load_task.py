""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""
import json
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

with open('ARC/data/training/469497ad.json') as f: 
    j = json.load(f) 

print(j['train'][0])
print(j['test'][0])

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

plt.imshow(j['train'][0]['input'], cmap=cmap, interpolation='nearest')
plt.show()



