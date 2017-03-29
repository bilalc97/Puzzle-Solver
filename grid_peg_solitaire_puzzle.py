from puzzle import Puzzle


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    # implement __eq__, __str__ methods
    # __repr__ is up to you
    def __str__(self):
        """
        Return a human-readable string representation of GridPegSolitaire self.

        @type self: GridPegSolitairePuzzle
        @rtype: str

        >>> grid1 = [["#", "*", "*", "*", "#"]]
        >>> grid1 += [["#", "*", "*", "*", "#"]]
        >>> grid1 += [["*", "*", ".", "*", "*"]]
        >>> grid1 += [["*", "*", ".", "*", "*"]]
        >>> grid1 += [["#", "*", "*", "*", "#"]]
        >>> grid1 += [["#", "*", "*", "*", "#"]]
        >>> p1 = GridPegSolitairePuzzle(grid1, {"#", "*", "."})
        >>> print(p1)
        # * * * #
        # * * * #
        * * . * *
        * * . * *
        # * * * #
        # * * * #
        >>> grid2 = [[".", "*", "*", ".", "."]]
        >>> grid2 += [[".", ".", ".", ".", "."]]
        >>> grid2 += [[".", ".", ".", ".", "."]]
        >>> grid2 += [[".", ".", ".", ".", "."]]
        >>> grid2 += [[".", ".", ".", ".", "."]]
        >>> p2 = GridPegSolitairePuzzle(grid2, {"*", ".", "#"})
        >>> print(p2)
        . * * . .
        . . . . .
        . . . . .
        . . . . .
        . . . . .
        """
        board = ''
        for row in self._marker:
            for symbol in row:
                board += symbol + " "
            board = board.strip() + "\n"
        return board.strip()

    def __eq__(self, other):
        """
        Return whether GridPegSolitaire self is equivalent to other

        @type self: GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @rtype: bool

        >>> grid1 = [["#", "*", "*", "*", "#"]]
        >>> grid1 += [["#", "*", "*", "*", "#"]]
        >>> grid1 += [["*", "*", ".", "*", "*"]]
        >>> grid1 += [["*", "*", ".", "*", "*"]]
        >>> grid1 += [["#", "*", "*", "*", "#"]]
        >>> grid1 += [["#", "*", "*", "*", "#"]]

        >>> grid2 = [["#", "*", "*", "*", "#"]]
        >>> grid2 += [["#", "*", "*", "*", "#"]]
        >>> grid2 += [["*", "*", ".", "*", "*"]]
        >>> grid2 += [["*", "*", ".", "*", "*"]]
        >>> grid2 += [["#", "*", "*", "*", "#"]]
        >>> grid2 += [["#", "*", "*", "*", "#"]]

        >>> grid3 = [[".", "*", "*", "*", "."]]
        >>> grid3 += [[".", "*", "*", "*", "."]]
        >>> grid3 += [["*", "*", ".", "*", "*"]]
        >>> grid3 += [["*", "*", ".", "*", "*"]]
        >>> grid3 += [[".", "*", "*", "*", "."]]
        >>> grid3 += [[".", "*", "*", "*", "."]]

        >>> p1 = GridPegSolitairePuzzle(grid1, {"#", "*", "."})
        >>> p2 = GridPegSolitairePuzzle(grid2, {"#", "*", "."})
        >>> p3 = GridPegSolitairePuzzle(grid3, {"#", "*", "."})

        >>> p1 == p2
        True
        >>> p1 == p3
        False
        """
        return (type(self) == type(other) and
                self._marker == other._marker and
                self._marker_set == other._marker_set)

    # override extensions
    # legal extensions consist of all configurations that can be reached by
    # making a single jump from this configuration
    def extensions(self):
        """
        Return list of legal extensions of GridPegSolitaire self.

        @type self: GridPegSolitairePuzzle
        @rtype: list[GridPegSolitaire]

        >>> grid1 = [["*", "*", "*", "*", "*"]]
        >>> grid1 += [["*", "*", ".", "*", "."]]
        >>> grid1 += [["*", "*", "*", "*", "*"]]
        >>> p = GridPegSolitairePuzzle(grid1, {"#", "*", "."})
        >>> extensions = p.extensions()
        >>> len(extensions)
        1
        >>> print(extensions[0])
        * * * * *
        . . * * .
        * * * * *
        >>> grid2 = [[".", ".", ".", ".", "."]]
        >>> grid2 += [[".", ".", ".", ".", "."]]
        >>> grid2 += [[".", ".", "*", ".", "."]]
        >>> grid2 += [[".", ".", ".", ".", "."]]
        >>> grid2 += [[".", ".", ".", ".", "."]]
        >>> p2 = GridPegSolitairePuzzle(grid2,{"*", ".", "#"})
        >>> len(p2.extensions()) == 0
        True
        """
        ext_lst = []
        orig = self._marker

        for i in range(len(orig)):
            for j in range(len(orig[i])):
                # Nested loop checks every single position in orig for an empty
                # spot. If a peg can make a legal jump to an empty spot, a
                # puzzle configuration following that jump is added to ext_lst.
                if orig[i][j] == ".":
                    # Jump from above
                    if i - 2 >= 0 and orig[i-2][j] == "*" \
                            and orig[i-1][j] == "*":
                        marker = [list(lst) for lst in orig]
                        marker[i-2][j] = "."
                        marker[i-1][j] = "."
                        marker[i][j] = "*"
                        ext_lst.append(GridPegSolitairePuzzle(marker,
                                                              self._marker_set))
                    # Jump from below
                    if i + 2 < len(orig) and orig[i+2][j] == "*" \
                            and orig[i+1][j] == "*":
                        marker = [list(lst) for lst in orig]
                        marker[i+2][j] = "."
                        marker[i+1][j] = "."
                        marker[i][j] = "*"
                        ext_lst.append(GridPegSolitairePuzzle(marker,
                                                              self._marker_set))
                    # Jump from left
                    if j - 2 >= 0 and orig[i][j-2] == "*" \
                            and orig[i][j-1] == "*":
                        marker = [list(lst) for lst in orig]
                        marker[i][j-2] = "."
                        marker[i][j-1] = "."
                        marker[i][j] = "*"
                        ext_lst.append(GridPegSolitairePuzzle(marker,
                                                              self._marker_set))
                    # Jump from right
                    if j + 2 < len(orig[i]) and orig[i][j+2] == "*" \
                            and orig[i][j+1] == "*":
                        marker = [list(lst) for lst in orig]
                        marker[i][j+2] = "."
                        marker[i][j+1] = "."
                        marker[i][j] = "*"
                        ext_lst.append(GridPegSolitairePuzzle(marker,
                                                              self._marker_set))
        return ext_lst

    # override is_solved
    # A configuration is solved when there is exactly one "*" left
    def is_solved(self):
        """
        Return whether GridPegSolitaire self is solved.

        @type self: GridPegSolitairePuzzle
        @rtype: bool

        >>> grid1 = [[".", ".", ".", ".", "."]]
        >>> grid1 += [[".", ".", "*", ".", "."]]
        >>> grid1 += [[".", ".", ".", ".", "."]]
        >>> p1 = GridPegSolitairePuzzle(grid1, {"#", "*", "."})
        >>> p1.is_solved()
        True
        >>> grid2 = [["#", "*", "*", "*", "#"]]
        >>> grid2 += [["#", "*", "*", "*", "#"]]
        >>> grid2 += [["*", "*", ".", "*", "*"]]
        >>> grid2 += [["*", "*", ".", "*", "*"]]
        >>> grid2 += [["#", "*", "*", "*", "#"]]
        >>> grid2 += [["#", "*", "*", "*", "#"]]
        >>> p2 = GridPegSolitairePuzzle(grid2, {"#", "*", "."})
        >>> p2.is_solved()
        False
        """
        count = 0
        for row in self._marker:
            count += row.count("*")
        return count == 1


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
