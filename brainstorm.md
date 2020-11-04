# Overview

This is a meta-learning task, so for each instance we are given a few input-output pairs as training data, and then 3 test inputs for which we have to produce the correct output at least once.

The dataset has 400 train tasks, 400 validation tasks, and 200 help out test tasks.

## TODO
 * Finish the task with moving the blocks (Noah)
 * implement a few more lisp annotations -- ideally with recursion or map (Noah)
 * Add heuristics to the score function (Both)
 * Think about how to add types (izzy for now)
 	* types will be used for the following capabilities
 		* check if a program is valid
 		* get the type of a subtree
 		* we may have to infer the type of arguments to a lambda
 		* for templated types, we may have to consider sets of valid types
 * implement assignment from tuples (izzy)

## Thoughts

 * Program synthesis is the way to go
 * we should use all three guesses -> three different "correct" programs (see [Principle of Multiple Explanations](http://guillefix.me/cosmos/static/Principle%2520of%2520multiple%2520explanations.html))
 * weight programs by correctness, then occams razor (see [Solomanoff Induction](https://en.wikipedia.org/wiki/Solomonoff%27s_theory_of_inductive_inference))
 * Program synthesis should neurally guided to reduce search time
 * We should synthesize new primtives using the train dataset (see [Kevin Ellis: "Growing Libraries of Subroutines with Wake/Sleep Bayesian Program Learning"](https://www.youtube.com/watch?v=_oyGF1YqdJc))

## Strategy

1. Implement bare-bones of language (partially complete. need lambda)
2. Start trying to solve puzzles. Implement necessary primitives to code solutions in language
3. Implement program-sampler that efficiently samples programs which type-check
4. Better program synthesis
	* Traces
	* Curriculum learning (start w/ simple puzzles)
	*

### Types

Hinlee Milner for Type-inference.

 * Grid: 2d array of colors
 * Mask: 2d array of boools
 * Shape: A grid and a mask (to allow transparency)
 * Int: what it sounds like
 * Pos: 2 Ints
 * Set(T): A higher-order container of T

### Primitives to implement

 * **PatchExtract**: Grid, Pos -> Grid
 * **PatchInsert**: Grid, Grid, Pos -> Grid
 * **ShapeExtract**: Grid, Pos -> Shape
 * **ShapeInsert**: Grid, Pos, Shape -> Grid
 * **CountOccurences**: Grid, Shape -> Int
 * **BackgroundColor**: Grid -> Color
 * **MaskAnd**: Mask, Mask -> Mask
 * **MaskOr**: Mask, Mask -> Mask

### Program Synthesis Concepts

 * Insert one program into another
 	* Have **Identity** be a program and let it implicitly run between every pair
 	of primtives
 	* With **Identity**, this operation could be adding, replacing, or deleting
 * Find a program that generates each grid from scratch (regardless of the mapping)
 	* Then reason about mapping between programs instead of between grids




### Features
In order to accelerate program synthesis, we may want to use neurally guided search (neural network ingests training examples and outputs probability distribution over programs). We may need to learn input features for this netowrk, but we can implement them ourselves fairly easily. Some features that may be worth hardcoding are

 * symmetric input (or near symmetric)
 * repeated objects
 * background color detector
 * colors to ignore
 * obvious grid shape features (ie. "output always 1x1" or "shape unchanged")
