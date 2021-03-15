# Notes on Search

## Overview

Task:
	Train: (x1, y1) (x2, y2)
	Test: x1, x2, x3

Goal: find a program P, such that P(x) = y

Language: l in L

## Search

We'll need a function to "expand" a node. In other words, go from program P1 -> P2. There are many possible next programs -- use your score function to pick the best one(s). (see `old_search/modify`)

So what do we do? Perform a random modification of P1.

* wrap the entire program in a new function
* replace a function/argument somewhere in the program
* add/remove an argument

``` def expand(P1) -> P2```

we'll need a function to check if program valid (for now try-except. in future: typecheck)
```def valid(P) -> bool```

we'll need a function to "score" that program (see `old_search/heuristics`)
```def score(P, train) -> float```

 * how short is the program
 * how many of the train tasks does it get right
 * is the output grid the right shape

we'll need a goal-checker see if that program fits the training data
```def goal(P, train) -> bool```

we'll need a function that "runs" the whole search
``` def search(train) -> P ```


### Considerations

Look up A-star and look up Beam-search.

 * Some programs might be "dead-ends." Consider throwing them out with some heuristic (#times we've epanded). look up [UCB](https://towardsdatascience.com/the-upper-confidence-bound-ucb-bandit-algorithm-c05c2bf4c13f)
 * Might want to make custom, easy tasks to test out search. look up other people working on ARC to see if you can get there hand-made tasks
 * 