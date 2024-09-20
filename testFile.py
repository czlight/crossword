from crossword import *

variable1 = Variable(0,0, Variable.DOWN, 5)
variable2 = Variable(0,0, Variable.DOWN, 5)

print(hash(variable1))
print(str(variable1))

CrosswordCreator.revise(variable1, variable1)
