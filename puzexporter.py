from puz import Puzzle
from typing import Callable, Optional

def _get_clue_numbers(puzzle: Puzzle) -> dict[int, int]:
    """Get a dictionary of all cell numbers that start words, mapping to their clue number"""
    clue_numbers: dict[int, int] = {}
    for clue_set in [puzzle.clue_numbering().across, puzzle.clue_numbering().down]:
        for clue in clue_set:
            clue_numbers[clue["cell"]] = clue["num"]
    return clue_numbers


def format_puzzle_grid(puzzle: Puzzle, collate_rows: Callable[[list[str]], str], collate_cells: Callable[[list[str]], str], create_cell: Callable[[bool, Optional[int], str], str]) -> str:
    """
    Represent the grid of a puz.Puzzle crossword puzzle into a formatted string
    puzzle: the puzzle to format
    collate_rows: a function that turns a list of rows into a full formatted puzzle
    collate_cells: a function that turns a list of cells into a formatted row
    create_cell: a function that creates a cell given whether it is solid (i.e. not able to be filled with a letter), it's clue number (if it has one), and its intended letter in the solution
    """
    clue_numbers = _get_clue_numbers(puzzle)
    rows = []
    for row in range(puzzle.height):
        cells = []
        for column in range(puzzle.width):
            cell = row*puzzle.width + column
            cells.append(create_cell(puzzle.fill[cell] == puzzle.blacksquare(), clue_numbers.get(cell, None), puzzle.solution[cell]))
        rows.append(collate_cells(cells))
    return collate_rows(rows)


def _collate_latex_cells(cells: list[str]) -> str:
    """Turn LaTeX cells into a row."""
    return " ".join(cells) + " |."

def _create_latex_cell(is_solid: bool, number: Optional[int], intended_letter: str) -> str:
    """Create a cell for a LaTeX crossword"""
    result = "|"
    if number is not None:
        result += f"[{number}]"
    if is_solid:
        result += "*"
    else:
        result += intended_letter
    return result

def puzzle_grid_to_latex(puzzle: Puzzle) -> str:
    """Represent the grid of the crossword as LaTeX (using the cwpuzzle LaTeX library)"""
    result = f"\\begin{{Puzzle}}{{{puzzle.width}}}{{{puzzle.height}}}\n"
    result += format_puzzle_grid(puzzle, "\n".join, _collate_latex_cells, _create_latex_cell)
    return result + "\n\\end{Puzzle}"


def _collate_html_rows(rows: list[str]) -> str:
    """Turn HTML rows into a table"""
    return "<table class=\"crossword\">\n" + "\n".join(rows) + "\n</table>"

def _collate_html_cells(cells: list[str]) -> str:
    """Turn HTML cells into a row"""
    return " "*4 + "<tr>\n" + "\n".join(cells) + "\n" + " "*4 + "</tr>"

def _create_html_cell(is_solid: bool, number: Optional[int], intended_letter: str) -> str:
    """Create a cell for a HTML crossword"""
    if is_solid:
        return " "*8 + "<td class=\"solidsquare\"></td>"
    
    result = " "*8 + "<td>"
    if number is not None:
        result += f"<sup>{number}</sup>"
    return result + "<input type=\"text\" minlength=\"1\" maxlength=\"1\"></td>"

def _create_html_solution_cell(is_solid: bool, number: Optional[int], intended_letter: str) -> str:
    """Create a cell with letter filled in for a HTML crossword"""
    if is_solid:
        return " "*8 + "<td class=\"solidsquare\"></td>"
    
    result = " "*8 + "<td>"
    if number is not None:
        result += f"<sup>{number}</sup>"
    return result + f"<input type=\"text\" minlength=\"1\" maxlength=\"1\" value=\"{intended_letter}\" readonly></td>"

def puzzle_grid_to_html(puzzle: Puzzle, solved: bool = False) -> str:
    """Represent the grid of the crossword as a HTML table"""
    return format_puzzle_grid(puzzle, _collate_html_rows, _collate_html_cells, _create_html_solution_cell if solved else _create_html_cell)
    

def puzzle_clueset_to_latex(clueset: list[dict[str, int]], clues: list[str], clueset_name: str) -> str:
    """Provides the LaTeX form of a clueset (using the cwpuzzle LaTeX library)"""
    result = f"\\begin{{PuzzleClues}}{{\\textbf{{{clueset_name}}}\\\\}}\n"
    clue_strings: list[str] = []
    for clue in clueset:
        clue_strings.append(f"\\Clue{{{clue['num']}}}{{}}{{{clues[clue['clue_index']]}}}")
    result += "\\\\\n".join(clue_strings) + "\n\\end{PuzzleClues}"
    return result

def puzzle_clues_to_latex(puzzle: Puzzle) -> str:
    """Provides the LaTeX form of the clues of a puzzle (using the cwpuzzle LaTeX library)"""
    return puzzle_clueset_to_latex(clueset=puzzle.clue_numbering().across, clues=puzzle.clues, clueset_name="Across") + "\n\n" + puzzle_clueset_to_latex(clueset=puzzle.clue_numbering().down, clues=puzzle.clues, clueset_name="Down")

def puzzle_to_latex(puzzle: Puzzle) -> str:
    """Return the LaTeX equivalent of an entire puzzle (using the cwpuzzle LaTeX library)"""
    return puzzle_grid_to_latex(puzzle) + "\n\n" + puzzle_clues_to_latex(puzzle)


def puzzle_clueset_to_html(clueset: list[dict[str, int]], clues: list[str], clueset_name: str) -> str:
    """Provides the HTML form of a clueset as an ordered list"""
    result = f"<h3 class=\"clueset\">{clueset_name}</h3>\n<ol class=\"clueset\">\n"
    for clue in clueset:
        result += " "*4 + f"<li value=\"{clue['num']}\">{clues[clue['clue_index']]}</li>\n"    
    result += "</ol>"
    return result

def puzzle_clues_to_html(puzzle: Puzzle) -> str:
    """Provides the HTML form of the clues of a puzzle"""
    return puzzle_clueset_to_html(clueset=puzzle.clue_numbering().across, clues=puzzle.clues, clueset_name="Across") + "\n\n" + puzzle_clueset_to_html(clueset=puzzle.clue_numbering().down, clues=puzzle.clues, clueset_name="Down")

def puzzle_to_html(puzzle: Puzzle) -> str:
    """Return the HTML equivalent of an entire puzzle (represented as a table)"""
    return puzzle_grid_to_html(puzzle) + "\n\n" + puzzle_clues_to_html(puzzle)
