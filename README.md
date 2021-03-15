# arc
Taking a stab at The Abstraction and Reasoning Corpus


## Setup

```
git clone git@github.com:IzzyBrand/arc.git
cd arc
git submodule init
git submodule update
```

## Looking at examples

On OSX

```
open ARC/apps/testing_interface.html
```

On linux

```
google-chrome ARC/apps/testing_interface.html
```

## The repo

 * **primitives.py** implements language primitivess like **add(x1, x2)**
 * **programs.py** implements the program structure, including a parser and type-checker
 * **demos.py** solves some selected ARC tasks in using primitives and programs
 * **search.py** implements a very naive version of program synthesis (rejection sampling over programs)
 * **run.py** is a script which executes search on each of the tasks in the dataset
 
