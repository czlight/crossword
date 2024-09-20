from crossword import *
from generate import *

variable1 = Variable(4,4, Variable.ACROSS, 5)
variable2 = Variable(2,1, Variable.DOWN, 5)

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
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    #assignment = creator.solve()
    creator.revise(variable1, variable2)

    # Print result
    #if assignment is None:
     #   print("No solution.")
    #else:
    #    creator.print(assignment)
     #   if output:
      #      creator.save(assignment, output)


if __name__ == "__main__":
    main()
