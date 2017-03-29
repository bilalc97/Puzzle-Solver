"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# uncomment the next two lines on a unix platform, say CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys
sys.setrecursionlimit(10**6)


# TODO
# implement depth_first_solve
# do NOT change the type contract
# you are welcome to create any helper functions
# you like
def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """
    if puzzle.is_solved():
        return PuzzleNode(puzzle)

    # set -> keeps track of visited nodes
    visited = {str(puzzle)}
    # deque -> keeps track of the next nodes to visit.
    stack = deque()

    # Add initial puzzles to visit
    for p in puzzle.extensions():
        stack.append(PuzzleNode(p, parent=PuzzleNode(puzzle)))

    # Continuously visit the left most node in stack until a solution is found,
    # all while ignoring already visited puzzles.
    while len(stack) > 0:
        current = stack.popleft()
        if str(current.puzzle) not in visited:
            visited.add(str(current.puzzle))
            if current.puzzle.is_solved():
                return dfs_path_maker(current)
            for p in current.puzzle.extensions():
                # Appending left is important to maintain deeper searches.
                stack.appendleft(PuzzleNode(p, parent=current))
    return None


def dfs_path_maker(node):
    """
    Return a PuzzleNode that creates a path from the original puzzle to the
    solved puzzle.

    @type node: PuzzleNode
    @rtype: PuzzleNode
    """
    while node.parent is not None:
        child = node
        node = node.parent
        node.children.append(child)
    return node


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode
    """

    p = PuzzleNode(puzzle)
    path = breadth_first_search(p)
    if path:
        return path[0]
    else:
        return None    # Puzzle does not contain a solution.


def breadth_first_search(parent):
    """
    Return the starting/parent node of the path to reach the
    solution to the puzzle.

    @type parent: PuzzleNode
    @rtype: [PuzzleNode]
    """
    que = deque()
    que.append(parent)
    visited = set()

    while len(que) != 0:

        cwn = que.popleft()  # cwn --> current working node
        visited.add(str(cwn.puzzle))
        for ext in cwn.puzzle.extensions():
            if str(ext) not in visited:
                pn = PuzzleNode(ext)
                pn.parent = cwn
                que.append(pn)

        if cwn.puzzle.is_solved():
            snode = cwn
            while snode.parent:
                snode.parent.children = [snode]
                snode = snode.parent
            return [snode]


# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.
class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether PuzzleNode self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
