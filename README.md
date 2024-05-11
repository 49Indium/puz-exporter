# puz-exporter
A python library to export crossword .puz files to TeX and HTML formats. Uses the [puzpy library](https://github.com/alexdej/puzpy) to read crosswords in the .puz format. When exporting to $\TeX$, the [cwpuzzle](http://www.gerd-neugebauer.de/software/TeX/cwpuzzle/en/) is used. When exporting to HTML, a table layout is generated. See the images below, [this basic HTML version from the examples folder](https://isaacbeh.net/projects/crossword-example/crossword.html), [this more polished HTML version](https://isaacbeh.net/blog/cs-crossword.html) or [this $\TeX$ PDF](https://isaacbeh.net/blog/cs-crossword/cs-crossword.pdf).

# Basic Usage
Load a puzzle using the puzpy library:
```python
import puz
import puzexporter
p = puz.read("example/cs-crossword.puz")
```
Print the entire puzzle (grid and clues) in $\TeX$ or HTML format:
```python
print(puzexporter.puzzle_to_latex(p))
print(puzexporter.puzzle_to_html(p))
```
Print the puzzle grid in $\TeX$ or HTML format:
```python
print(puzexporter.puzzle_grid_to_latex(p))
print(puzexporter.puzzle_grid_to_html(p))
```
Print the solutions in HTML (in $\TeX$ the solutions are already part of the file and can be toggled by including `\PuzzleSolution` before the puzzle):
```python
print
print(puzexporter.puzzle_grid_to_html(p, solved = True))
```
Print just the clues in $\TeX$ or HTML:
```python
print(puzexporter.puzzle_clues_to_latex(p))
print(puzexporter.puzzle_clues_to_html(p))
```
You can also format the puzzle grid into other formats with custom functions by using `format_puzzle_grid`:
```python
# Produce a solution to a puzzle where all the letters are next to each other in a grid
print(format_puzzle_grid(
  p,
  collate_rows = "\n".join,
  collate_cells = "".join,
  create_cell = lambda is_solid, number, solution_letter: "█" if is_solid else solution_letter
))
```
