# Java Approach

This folder contains the Java programs that can be used to generate tuples for any values of $m$ and $d$, as well as the output files for these data.

## Legend

### `src`:

- `ShiodaTupleGenerator.java` is a program that is used to generate indecomposable tuples using Lemma 5.5 from Shioda's paper. 
- `TupleGenerator.java` is a program that is used to generate tuples via brute force.
- `CustomException.java` is a small custom exception class used throughout the other programs.
- `FileHelper.java` contains helper functions used to assist with maintaining folder structure.
- `Tuple.java` is a custom integer tuple class with a bunch of helper functions used in the tuple generator programs.

### `outputs`:

- `indecomposable_csvs` contains indecomposable tuples for each $m,d$, where $m=p^2$.
- `modified_csvs` contains selected and modified indecomposable tuple(s) as stated in **Remark 3.23**.
- `modified_max_csvs` contains the absolute max value of the modified tuple(s) in `modified_csvs`.
- `modified_without_max_csvs` contains the sub-tuple(s) without the absolute value of the modified tuple(s).
- `relation_csvs` contains the relation(s) for each $m,d$ similar to **Example 3.27**.