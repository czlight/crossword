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
        # create empty set that will hold item to remove, if any
        arcRemovalSet = set()
        # neighbors = self.crossword.neighbors(x)

        # return value of function. will be set to True if x's domain is changed
        variableRevised = False

        # check for overlap between variables
        overlapIndices = self.crossword.overlaps[x,y]

        # keep track of how many items are in y's domain
        # to determine when, for each value in x's domain,
        # we have iterated through every item in y's domain
        yDomainLength = len(self.domains[y])

        # if variables don't overlap no revision is needed
        if overlapIndices == None:
            print("no overlap")
            return variableRevised
        else:
            print("there's overlap!")
            print("overlapIndices is:", overlapIndices)

            # iterate over every value in x's domain
            for xvalue in self.domains[x]:

                # set count to 0 for each new value in x's domain
                iterationCount = 0

                for yvalue in self.domains[y]:
                    iterationCount += 1
                    print("iteration count:", iterationCount)
                    print("checking indices of xvalue, yvalue", xvalue, yvalue)

                    if xvalue[overlapIndices[0]] == yvalue[overlapIndices[1]]:
                        # this value in x's domain has a value in y's
                        # break in order to check next xvalue in self.domains[x]
                        print("x has a value in its domain that has a possible value in y's domain")
                        print("these values are: " ,xvalue, yvalue)
                        break

                    # this value in x's domain does not have a possible value in y's, remove it from x's domain
                    if iterationCount == yDomainLength:
                        arcRemovalSet.add(xvalue)

        # iterate over every item added to set
        # and remove it from variable's domain
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
        print("calling ac3*!*!***************")

        # create an empty list to represent queue
        arcQueue = []

        # use optional argument 'arcs' as initial list
        if arcs != None:
            arcQueue = arcs
        else:
            # iterate over each variable pair (i.e., key) and value and add to queue
            for item, overlap in self.crossword.overlaps.items():
                if overlap is not None:
                    print("item in overlaps", item)
                    arcQueue.append(item)
        print("arcQueue contains the following: ", arcQueue)

        # loop until list is empty
        while arcQueue:
            print("queue isn't empty")
            ((x,y)) = arcQueue.pop(0)

            if self.revise(x,y):
                # check for empty domain (i.e., problem not solvable)
                if not self.domains[x]:
                    print("problem not solvable!")
                    return False
                # enqueue each neighbor of x because it was revised
                for neighbors in self.crossword.neighbors(x) - {y}:
                    arcQueue.append((neighbors, x))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        print("-----_------calling assignment_complete function")
        # to return True, below criteria must be satisfied:
        # 1. every variable exists in assignment
        # 2. every assignment is non-null

        # reminder: self.crossword.variables is a set of all variables in the puzzle
        # assignment is a dictionary mapping variable objects to word

        allVariables = self.crossword.variables
        print("all variables is: ", allVariables)

        for item in allVariables:
            if item not in assignment:
                return False

        # iterate over each variable/key in assignment, return False if value is

        for variable in assignment:
            # check whether each variable has a word assigned to it
            if assignment[variable] == None:
                return False

        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.

        # return True under the following conditions:
        # 1. variable word length property and assigned word match
        # 2. no conflicting overlaps (i.e., overlapping neighbors agree on letter in cell)
        # 3. all values are distinct.
        # Note: not all variables will necessarily be present in the assignment
        """

        for variable in assignment:

            neighborsRemovalSet = set()

            neighbors = self.crossword.neighbors(variable)

            # remove all neighbors that aren't in assignment
            for item in neighbors:
                if item not in assignment:
                    neighborsRemovalSet.add(item)

            if neighborsRemovalSet:
                for item in neighborsRemovalSet:
                    neighbors.remove(item)

            # check whether variable's length property matches length of its assigned word
            if variable.length != len(assignment[variable]):
                print("variable's length", variable.length, "does not match assigned word::", assignment[variable], "length")
                return False

            # for each variable in assignments, check overlap and ensure word indices match.
            for neighbor in neighbors:
                overlapIndices = self.crossword.overlaps[variable, neighbor]

                if (neighbor in assignment and assignment[variable][overlapIndices[0]] != assignment[neighbor][overlapIndices[1]]) or assignment[variable] == assignment[neighbor]:
                    return False
        return True




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
