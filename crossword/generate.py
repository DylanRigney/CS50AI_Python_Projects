import sys

from crossword import *
from crossword import Variable, Crossword
from collections import deque


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # iterate through self.domains, check if each value in the domain is node consistent
        # if a value is inconsistent it should be removed from self.domains
        # ie if that length of the word in self.domains violates length constraint remove

        # for each var get the domain
        for var in self.domains:
            for word in self.domains[var].copy():
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False

        # if no overlap x and y are arc consistent otherwise get overlaps
        if self.crossword.overlaps[x, y] is None:
            return revised
        overlaps_x, overlaps_y = self.crossword.overlaps[x, y]

        # iterate through x's domain
        for x_word in self.domains[x].copy():
            # if no y_word in y is consistent with x_word
            if not any(x_word[overlaps_x] == y_word[overlaps_y] for y_word in self.domains[y]):
                self.domains[x].remove(x_word)
                revised = True

        return revised

    def get_arc_queue(self, var=None):
        arc_queue = deque()

        if var:
            neighbors = self.crossword.neighbors(var)
            for neighbor in neighbors:
                arc_queue.append((neighbor, var))

        else:
            for var in self.crossword.variables:
                neighbors = self.crossword.neighbors(var)
                for neighbor in neighbors:
                    arc_queue.append((var, neighbor))

        return arc_queue

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = self.get_arc_queue()
        else:
            arcs = deque(arcs)

        while arcs:
            (x, y) = arcs.popleft()

            revised = self.revise(x, y)
            if revised:
                if len(self.domains[x]) == 0:
                    return False
                for neighbor in self.crossword.neighbors(x):
                    if neighbor != y:
                        arcs.append((neighbor, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment.keys()) == len(self.crossword.variables)

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # all values in assigment must be distinct.
        if len(assignment.values()) > len(set(assignment.values())):
            return False

        for var in assignment:
            # check if each variable is the same length as it's value
            if var.length != len(assignment[var]):
                return False

            # Check if there are conflicts between overlapping assignments
            neighbors = self.crossword.neighbors(var)
            for neighbor in neighbors:
                if neighbor in assignment:
                    i, j = self.crossword.overlaps[var, neighbor]
                    if assignment[var][i] != assignment[neighbor][j]:
                        return False

        return True

    def eliminate_values(self, var, option, assignment):
        # create set and dictionary to track eliminated values
        eliminated = set()

        # get neighbors for var
        neighbors = self.crossword.neighbors(var)

        # for each neighbor that hasn't already been assigned a value
        for neighbor in neighbors - set(assignment.keys()):
            # get overlap between var and neighbor
            i, j = self.crossword.overlaps[var, neighbor]

            # eliminate some extra checking
            neighbor_dom = set(self.domains[neighbor])
            neighbor_dom -= eliminated

            # iterate through the neighbors domain, adding eliminated
            for value in neighbor_dom:
                # check if the overlapping letters are the different(word is eliminated)
                if option[i] != value[j]:
                    eliminated.add(value)

        # however many words are in the set is how many values were eliminated
        return len(eliminated)

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # get list of possible values for var
        domain_values = self.domains[var]

        # Sort domain values and
        # return list of values
        return sorted(domain_values, key=lambda option: self.eliminate_values(var, option, assignment))

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # return variable with MRV(fewest domain values) w/ highest degree tiebreak
        # make sure that the variable isn't in assignment
        return min(self.domains.keys() - assignment.keys(), key=lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var))))

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # if assigment is complete return assignment
        if len(assignment.keys()) == len(self.crossword.variables):
            return assignment

        # select an unassigned variable
        variable = self.select_unassigned_variable(assignment)

        # for each word in the variables domain
        for word in self.domains[variable]:

            # assign the word to a variable
            new_assignment = assignment.copy()
            new_assignment[variable] = word

            # if that word is consistent with assignment
            if self.consistent(new_assignment):

                # Run backtrack with that assignment.
                result = self.backtrack(new_assignment)

                # if it's successful return that assignment
                if result is not None:
                    return result

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
