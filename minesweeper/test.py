class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        print(f"{self.cells} = {self.count}")

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        raise NotImplementedError
    

# Define the cells
cells = {
    'A': (1, 2),
    'B': (3, 4),
    'C': (5, 6),
    'D': (7, 8),
    'E': (9, 10),
    'F': (11, 12),
    'G': (13, 14)
}

# Create two sentences with sets of cells and counts
sentence1 = Sentence(['A', 'B', 'C'], 1)
sentence2 = Sentence(['A', 'B', 'C', 'D', 'E', 'F', 'G'], 2)

# Print the sentences
print(sentence2)
print(sentence1)

if sentence1.cells.issubset(sentence2.cells):
    sentence3 = Sentence(sentence2.cells - sentence1.cells, sentence2.count - sentence1.count)
    print(sentence3)

if len(sentence1.cells) == sentence1.count:
    print("All cells in sentence1 are mines")
else:
    print("Not all cells in sentence1 are mines")

