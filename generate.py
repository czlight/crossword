import sys

from crossword import *


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
        print("******calling enforce node consistency!!*******")
        # node consistency is a unary constraint
        # loop over every word in crossword.words
        # loop over every variable's domain (i.e., self.domains[variable])

        removeSet = set()

        # Iterate over every variable
        for variable in self.crossword.variables:
            print("checking variable:::", variable)
            print("this variable's domain is: ", self.domains[variable])
            # iterate over every word in crossword puzzle
            for word in self.crossword.words:
                # if constraint not met (i.e., length of variable and length of word aren't equal, remove the word from its domain)
                # it doesn't fit in the spot we've alloted for a word
                if len(word) != variable.length:
                    removeSet.add(word)
            for item in removeSet:
                print("removing to enforce node consistency: ", item)
                self.domains[variable].remove(item)
            print("domain of variable", variable, "is now:!!:!::", self.domains[variable])
            # Clear the set before checking next variable
            removeSet.clear()

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """

        # for domains in domains[x]; remove any domains that
        # makes domains[y] == None (i.e., removes all domains of y)
        # iterate over domains in x if len(domains[y]) == 1 and domains[x] = domains[y]:
        # remove domain from x

        # strategy: iterate over every variable in the puzzle
        # for each neighbor of that variable, call overlap
        # overlap gives you the cell/coordinate they share
        # remove item in variablex
        print("calling revise function...........")
        print("variable x is: ", x)
        print("variable y is: ", y)
        print("self.domains is ", self.domains)
        arcRemovalSet = set()
        # neighbors = self.crossword.neighbors(x)

        # check for overlap between variables

        overlapIndices = self.crossword.overlaps[x,y]

        if overlapIndices == None:
            print("no overlap")
            return False
        else:
            print("there's overlap!")
            print("overlapIndices is:", overlapIndices)
            for xvalue in self.domains[x]:
                for yvalue in self.domains[y]:
                    if xvalue[overlapIndices[0]] == yvalue[overlapIndices[1]]:
                        # this value in x's domain has a possible value in y's domain
                        return True



        variableRevised = False
        for xvalue in self.domains[x]:
            print("xvalue is", xvalue)
            noOverlapCount = 0
            for yvalue in self.domains[y]:
                print("loop xvalue, yvalue", xvalue, yvalue)
                #print("self.crossword.structure[xvalue][yvalue]:", self.crossword.structure[x[xvalue]][y[yvalue]])
                #print("self.crossword.overlaps", self.crossword.overlaps)
                #if (x[xvalue], y[yvalue]) in self.crossword.overlaps:
                  #  print("self.crossword.overlaps[(x,y)]:", self.crossword.overlaps[(x[xvalue], y[yvalue])])
                #print("yvalue is ", yvalue)
                # if no overlap, add this item to set of values to remove from X's domain
                #if (xvalue, yvalue) in self.crossword.overlaps and not self.crossword.overlaps[(xvalue, yvalue)]:
                 #   print("xvalue", xvalue, ", and yvalue: ", yvalue, "don't overlap")
                  #  noOverlapCount += 1
            if noOverlapCount == len(self.domains[y]):
                    arcRemovalSet.add(xvalue)

        if arcRemovalSet:
            variableRevised = True
            for item in arcRemovalSet:
                self.domains[x].remove(item)

        return variableRevised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        raise NotImplementedError


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
