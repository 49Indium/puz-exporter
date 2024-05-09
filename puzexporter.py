import puz

def _get_clue_numbers(puzzle: puz.Puzzle) -> dict[int, int]:
    # Get a dictionary of all cell numbers that start words, mapping to their clue number
    clue_numbers: dict[int, int] = {}
    for clue_set in [puzzle.clue_numbering().across, puzzle.clue_numbering().down]:
        for clue in clue_set:
            clue_numbers[clue["cell"]] = clue["num"]
    return clue_numbers

def grid_to_latex(self: puz.Puzzle):
    result = f"\\begin{{Puzzle}}{{{self.width}}}{{{self.height}}}\n"

    clue_numbers = _get_clue_numbers(self)
    for row in range(self.height):
        for column in range(self.width):
            cell = row*self.width + column
            result += "|"

            if cell in clue_numbers:
                result += f"[{clue_numbers[cell]}]"
            
            if self.fill[cell] == self.blacksquare():
                result += "* "
            else:
                result += self.solution[cell] + " "

        result += "|.\n"
    result += "\\end{Puzzle}"
    return result

# Update the puzzle object
puz.Puzzle.grid_to_latex = grid_to_latex
