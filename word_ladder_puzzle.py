from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

    def __eq__(self, other):
        """
        Return whether WordLadderPuzzle self is equivalent to other.

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle | Any
        @rtype: bool

        >>> word_set1 = {'cost', 'cast', 'case', 'cave', 'save'}
        >>> word_ladder1 = WordLadderPuzzle ('cost', 'save', word_set1)
        >>> word_ladder2 = WordLadderPuzzle ('cost', 'save', word_set1)
        >>> word_ladder1 == word_ladder2
        True

        >>> word_set1 = {'cost', 'cast', 'case', 'save'}
        >>> word_ladder3 = WordLadderPuzzle ('cost', 'save', word_set1)
        >>> word_ladder2 == word_ladder3
        False
        """
        return (type(self) == type(other) and
                self._from_word == other._from_word and
                self._to_word == other._to_word and
                self._word_set == other._word_set)

    def __str__(self):
        """
        Return a human-readable string representation of
        WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: str

        >>> word_set1 = {'cost', 'cast', 'case', 'cave', 'save'}
        >>> word_ladder1 = WordLadderPuzzle ('cost', 'save', word_set1)
        >>> print(word_ladder1)
        cost -> save

        >>> word_ladder2 = WordLadderPuzzle ('cost', 'mast', word_set1)
        >>> print(word_ladder2)
        cost -> mast
        """
        return "{} -> {}".format(self._from_word, self._to_word)

    # override extensions
    # legal extensions are WordLadderPuzzles that have a from_word that can
    # be reached from this one by changing a single letter to one of those
    # in self._chars
    def extensions(self):
        """
        Return list of extensions of WordLadderPuzzle self.

        @type self: WordLadderPuzzle
        @rtype: list[WordLadderPuzzle]

        >>> word_set1 = {'cost', 'cast', 'case', 'base', 'save'}
        >>> word_ladder1 = WordLadderPuzzle ('case', 'save', word_set1)
        >>> L1 = word_ladder1.extensions()
        >>> L1[0]._from_word == 'base'
        True
        >>> L1[1]._from_word == 'cast'
        True

        >>> word_ladder2 = WordLadderPuzzle ('mango', 'fruit', word_set1)
        >>> L2 = word_ladder2.extensions()
        >>> len(L2) == 0
        True
        """
        possible_extensions = []
        from_word, to_word, ws, chars = (self._from_word, self._to_word,
                                         self._word_set, self._chars)

        # For each new word that can be created from set of chars that is also
        # in ws, add the word to possible_extensions.
        for i in range(len(from_word)):
            for letter in chars:
                word = from_word[:i] + letter + from_word[i+1:]
                if word in ws and word != from_word:
                    possible_extensions.append(WordLadderPuzzle(word,
                                                                to_word,
                                                                ws))
        return possible_extensions

    # override is_solved
    # this WordLadderPuzzle is solved when _from_word is the same as
    # _to_word
    def is_solved(self):
        """
        Return True iff WordLadderPuzzle self is solved.

        @type self: WordLadderPuzzle
        @rtype: bool

        >>> word_set1 = {'cost', 'cast', 'case', 'cave', 'save'}
        >>> word_ladder1 = WordLadderPuzzle ('cost', 'save', word_set1)
        >>> word_ladder1.is_solved()
        False

        >>> word_ladder2 = WordLadderPuzzle ('cost', 'cost', word_set1)
        >>> word_ladder2.is_solved()
        True
        """
        return self._from_word == self._to_word


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words.txt", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("cost", "save", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
