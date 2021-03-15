""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""
import numpy as np


def same_colors(g1, g2):
    return set(g1.ravel()) == set(g2.ravel())

def same_background(g1, g2):
    return np.median(g1) == np.median(g2)

def same_shape(g1, g2):
    return g1.shape == g2.shape

def same_structure(g1, g2):
    return ((g1 > 0) * (g2 > 0)).all()

def overlap(g1, g2):
    return (g1 == g2).mean()


def score(g1, g2):
    score = 0.

    if same_shape(g1, g2):
        score += 1
        score += same_structure(g1, g2)
        score += overlap(g1, g2)

    score += same_colors(g1, g2)
    score += same_background(g1,g2)

    return score
