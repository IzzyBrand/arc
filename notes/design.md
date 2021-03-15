# Design Doc


## Structures To Implement:

 * **Types**: represent the type of a symbol
 * **Symbols**: are the individual words or primitives in a program
 * **Trees**: programs are tree-structured collection of symbols
 * **Environment**: A mapping from names of variables to their symbols

## Types

### Overview
At the base-level, a type is a unique string identifier, like `"Int"` or `"Color"`.

**Functions** also have types, denoted `"input_type -> output_type"`. By design, functions only have on input and one output, so to pass or return multiple arguments those arguments must be wrapped in a tuple.

**Tuples** have a type. A tuple `(1, False)` has the typle `"(Int, Bool)"`

**Arrays** TODO

**Template Types** TODO

### The `Type` Class

We could simply pass around the string representation of a type, but for type checking (when we want to ensure that the types of a program are consistent), we would have to parse the string representation of higher-order types.

For this reason we implement the `Type` class with the following functionality.

 * `Type.__str__(self)` always eturns the string representation the type.
 * `FuncType`, `TupleType`, `ArrayType`, `TemplateType` all subclass `Type`
 * The `Type.T` attribute stores type information.
 	* `Type.T` just stores the string representation
 	* `FuncType.T` is a tuple `(input_type, output_type)`. Where both are instances of `Type`
 	* `TupleType.T` is a tuple of `Type`
 	* `ArrayType.T` stores the type of an element of the array

## Symbols

### Overview

Symbols are the base-level item of a program. `1`, `x`, `if`, `max`, `lambda` are all instances of symbols.

### The `Symbol` Class

Symbols have the following attributes:

 * `Symbol.name` a string representation of the symbol
 * `Symbol.type` the `Type` of the symbol

Symbols provide the following functions:
 
 * `Symbol.eval(self, args)` 
 * `Symbol.type_check(self)` always returns True (this is a base-case of type-check on trees)

## Trees

### Overview

Trees store the structure of a program. 

### The `Tree` Class

A `Tree` has two attributes:

 * `Tree.node` is a Tree or a Symbol
 * `Tree.children` is a (potentially empty) list of Trees or Symbols

**eval** To evaluate the program represented by the tree, use `Tree.eval(env)`

We don't need to pass any arguments to a tree, because it is assumed that any arguments to the node are stored in the children. However, the children or the node may be Symbols which need to be looked up in the environment.


## Environment

