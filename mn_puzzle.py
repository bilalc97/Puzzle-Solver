from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    # TODO
    # implement __eq__ and __str__
    # __repr__ is up to you
    def __eq__(self, other):
        """
        Return whether MNPuzzle self is equivalent to other.

        @type self: MNPuzzle
        @type other: MNPuzzle | Any
        @rtype: bool

        >>> start_grid1 = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid1 = (("1", "2", "3"), ("4", "5", "*"))
        >>> puzzle1 = MNPuzzle(start_grid1, target_grid1)
        >>> puzzle2 = MNPuzzle(start_grid1, target_grid1)
        >>> puzzle1 == puzzle2
        True

        >>> start_grid2 = (("2", "3", "*"), ("1", "4", "5"))
        >>> puzzle3 = MNPuzzle(start_grid2, target_grid1)
        >>> puzzle1 == puzzle3
        False
        """
        return (type(self) == type(other) and
                self.from_grid == other.from_grid and
                self.to_grid == other.to_grid)

    def __str__(self):
        """
        Return a human-readable string representation of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: str

        >>> start_grid1 = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid1 = (("1", "2", "3"), ("4", "5", "*"))
        >>> puzzle1 = MNPuzzle(start_grid1, target_grid1)
        >>> print(puzzle1)
        *23
        145

        >>> start_grid2 = (("1", "2", "3"), ("4", "5", "6"), ("7", "8", "*"))
        >>> target_grid2 = (("1", "2", "3"), ("4", "5", "6"), ("7", "8", "*"))
        >>> puzzle2 = MNPuzzle(start_grid2, target_grid2)
        >>> print(puzzle2)
        123
        456
        78*
        """
        game_board = ""
        for row in self.from_grid:
            for symbol in row:
                game_board = game_board + symbol
            game_board += '\n'
        return game_board.strip()

    # override extensions
    # legal extensions are configurations that can be reached by swapping one
    # symbol to the left, right, above, or below "*" with "*"
    def extensions(self):
        """
        Return list of extensions of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: list[MNPuzzle]

        >>> start_grid1 = (("*", "4", "5"), ("1", "3", "2"))
        >>> target_grid1 = (("1", "2", "3"), ("4", "5", "*"))
        >>> m1 = MNPuzzle(start_grid1, target_grid1)
        >>> L1 = m1.extensions()
        >>> len(L1) == 2
        True
        >>> L1[0].from_grid == (("4", "*", "5"), ("1", "3", "2"))
        True
        >>> L1[1].from_grid == (('1', '4', '5'), ('*', '3', '2'))
        True

        >>> start_grid2 = (("1", "*", "4"), ("3", "2", "5"))
        >>> target_grid2 = (("1", "2", "3"), ("4", "5", "*"))
        >>> m2 = MNPuzzle(start_grid2, target_grid2)
        >>> L2 = m2.extensions()
        >>> len(L2) == 3
        True
        >>> L2[2].from_grid == (('1', '2', '4'), ('3', '*', '5'))
        True
        """
        extensions = []
        from_grid, to_grid = self.from_grid, self.to_grid

        row = 0
        col = 0
        for i in range(len(from_grid)):
            for j in range(len(from_grid[i])):
                if from_grid[i][j] == "*":
                    row = i
                    col = j
                    # A break statement is used as the empty position has
                    # already been found.
                    break

        # If the move is possible, a list copy of from_grid is produced as
        # lists are mutable. Then the modified list is type cast into a tuple,
        # so that a puzzle can be produced and appended to extensions.

        # To the left.
        if col - 1 >= 0:
            lst_grid = [list(tup) for tup in from_grid]
            lst_grid[row][col-1], lst_grid[row][col] = (lst_grid[row][col],
                                                        lst_grid[row][col-1])

            new_grid = [tuple(row) for row in lst_grid]
            extensions.append(MNPuzzle(tuple(new_grid), to_grid))

        # To the right.
        if col + 1 < len(from_grid[row]):
            lst_grid = [list(tup) for tup in from_grid]
            lst_grid[row][col+1], lst_grid[row][col] = (lst_grid[row][col],
                                                        lst_grid[row][col+1])

            new_grid = [tuple(row) for row in lst_grid]
            extensions.append(MNPuzzle(tuple(new_grid), to_grid))

        # Up.
        if row - 1 >= 0:
            lst_grid = [list(tup) for tup in from_grid]
            lst_grid[row-1][col], lst_grid[row][col] = (lst_grid[row][col],
                                                        lst_grid[row-1][col])

            new_grid = [tuple(row) for row in lst_grid]
            extensions.append(MNPuzzle(tuple(new_grid), to_grid))

        # Down.
        if row + 1 < len(from_grid):
            lst_grid = [list(tup) for tup in from_grid]
            lst_grid[row+1][col], lst_grid[row][col] = (lst_grid[row][col],
                                                        lst_grid[row+1][col])

            new_grid = [tuple(row) for row in lst_grid]
            extensions.append(MNPuzzle(tuple(new_grid), to_grid))

        return extensions

    # override is_solved
    # a configuration is solved when from_grid is the same as to_grid
    def is_solved(self):
        """
        Return whether MNPuzzle self is solved.

        @type self: MNPuzzle
        @rtype: bool

        >>> start_grid1 = (("*", "2", "3"), ("1", "4", "5"))
        >>> target_grid1 = (("1", "2", "3"), ("4", "5", "*"))
        >>> puzzle1 = MNPuzzle(start_grid1, target_grid1)
        >>> puzzle1.is_solved()
        False

        >>> start_grid2 = (("1", "2", "3"), ("4", "5", "6"), ("7", "8", "*"))
        >>> target_grid2 = (("1", "2", "3"), ("4", "5", "6"), ("7", "8", "*"))
        >>> puzzle2 = MNPuzzle(start_grid2, target_grid2)
        >>> puzzle2.is_solved()
        True
        """
        return self.from_grid == self.to_grid


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
       solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
