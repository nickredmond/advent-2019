
def add_values(value1, value2):
    return value1 + value2

def multiply_values(value1, value2):
    return value1 * value2

PROGRAM_TERMINATION_CODE = 99
PROGRAM_OPERATIONS = {
    1: add_values,
    2: multiply_values
}

def perform_operation(currentIndex, programCode):
    operationValue = programCode[currentIndex]
    positionValue1 = programCode[currentIndex + 1]
    positionValue2 = programCode[currentIndex + 2]
    value1 = programCode[positionValue1]
    value2 = programCode[positionValue2]
    operation = PROGRAM_OPERATIONS[operationValue]
    return operation(value1, value2)

def program_has_next(currentIndex, programCode):
    return len(programCode) > currentIndex and programCode[currentIndex] is not PROGRAM_TERMINATION_CODE

def execute_program(programCode):
    currentIndex = 0
    while (program_has_next(currentIndex, programCode)):
        currentOperationResult = perform_operation(currentIndex, programCode)
        placementIndex = programCode[currentIndex + 3]
        programCode[placementIndex] = currentOperationResult
        currentIndex = currentIndex + 4

programData = []
with open('dec-02-pt1-program-input.txt') as programInput:
    programData = programInput.read().split(',')

initialProgramCode = []
for datum in programData:
    value = int(datum)
    initialProgramCode.append(value)

EXPECTED_OUTPUT = 19690720
MAX_INPUT = 99
currentOutput = 0
noun = MAX_INPUT
verb = MAX_INPUT
while currentOutput != EXPECTED_OUTPUT and noun >= 0:
    while currentOutput != EXPECTED_OUTPUT and verb >= 0:
        programCode = initialProgramCode.copy()
        programCode[1] = noun
        programCode[2] = verb
        execute_program(programCode)
        currentOutput = programCode[0]
        if currentOutput != EXPECTED_OUTPUT:
            verb = verb - 1
    if verb < 0:
        noun = noun - 1
        verb = MAX_INPUT

if currentOutput == EXPECTED_OUTPUT:
    answer = 100 * noun + verb
    print('result: ' + str(answer))
else:
    print('ERROR: did not work. :(')