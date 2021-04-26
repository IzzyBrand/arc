# Meeting Notes


## Infrastructure


 * Search for a program for each task in a set of tasks `run.py`
 	- tries to solve all the tasks in the ARC dataset
 	- prints out [n/800] correct when done
 * Search for a program, given a task `def search`
 	- runs the beam search. uses score/neural-nets/type-checker
 	- input to search
 		+ the task (train/test input/outputs)
 		+ max iterations
 	- output from search:
 		+ the best program
 * An iteration of beam search algorithm `def modify`
 	- a subroutine of search that produces a new set of candidate programs
 	- input:
 		+ beam width
 		+ previous set of programs
 		+ task
 		+ score_fun(prog)
 		+ type_check(prog)
 	- output:
 		+ a new set of programs
 * Run a program, on a task. (load it from arc database, run the lisp program) `util.py`

## Neural Networks (in the future)

Potentially using a neural network as a heuristic during search. How do we get training data? Naively search for solutions -- when you find one, your search "took a good path" -> add to dataset.

### Tricks

**Curriculum Learning** Consider taking baby steps on easier problems.

**Hindsight experience replay**

 1. Generate a random program
 2. Use that program to generate a fake "task" (input, output grids)
 3. Train your neural network to say "if I were trying to do that task, then this is the program"


