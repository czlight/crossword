from crossword import *
from generate import *

variable1 = Variable(1, 4, Variable.DOWN, 4)
variable2 = Variable(0, 1, Variable.DOWN, 5)


#use for structure1 and word1
# variable1 = Variable(4,4, Variable.ACROSS, 5)
#variable2 = Variable(2,1, Variable.DOWN, 5)

print(hash(variable1))
print(str(variable1))


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    myCrossword = Crossword(structure, words)
    myCreator = CrosswordCreator(myCrossword)
    #assignment = creator.solve()
    myCreator.revise(variable1, variable2)

    for y in range(myCrossword.height):
        for x in range(crossword.height):
            print(crossword)

    # print("crossword.structure[i][j] is True if blank")

    # Print result
    #if assignment is None:
     #   print("No solution.")
    #else:
    #    creator.print(assignment)
     #   if output:
      #      creator.save(assignment, output)


if __name__ == "__main__":
    main()
