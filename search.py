""" Massachusetts Institute of Technology

Izzy Brand, 2020
"""

def heursitic_evaluation(pred, label):
	score = 0

	# same shapes
	if pred.shape == label.shape:
		score += 1

		# same structure (only valid if shapes same)
		if (pred > 0) == (label > 0).all():
			score += 1

	# same colors
	if set(pred.ravel()) == set(label.ravel())
		score += 1

	return score
