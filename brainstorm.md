## Types

 * Grid: 2d array of colors
 * Mask: 2d array of boools
 * Shape: A grid and a mask (to allow transparency)
 * Int: what it sounds like
 * Pos: 2 Ints
 * Set(T): A higher-order container of T

## Primitives to implement

 * **PatchExtract**: Grid, Pos -> Grid
 * **PatchInsert**: Grid, Grid, Pos -> Grid
 * **ShapeExtract**: Grid, Pos -> Shape
 * **ShapeInsert**: Grid, Pos, Shape -> Grid
 * **CountOccurences**: Grid, Shape -> Int
 * **BackgroundColor**: Grid -> Color
 * **MaskAnd**: Mask, Mask -> Mask
 * **MaskOr**: Mask, Mask -> Mask

## Program Synthesis Ideas

 * Insert one program into another
 	* Have **Identity** be a program and let it implicitly run between every pair
 	of primtives
 	* With **Identity**, this operation could be adding, replacing, or deleting
