def place_result_value(value, programCode, currentIndex):
    placementIndex = int(programCode[currentIndex + 3])
    programCode[placementIndex] = value

def get_instruction_value(paramText, mode, programCode):
    paramValue = int(paramText)
    return paramValue if mode == 1 else int(programCode[paramValue])

def add_values(paramModes, programCode, currentIndex):
    values = []
    params = [programCode[currentIndex + 1], programCode[currentIndex + 2]]
    for index, param in enumerate(params):
        mode = int(paramModes[index])
        value = get_instruction_value(param, mode, programCode)
        values.append(value)
    result = sum(values) 
    # print('adding ' + str(result) + ', ' + str(values) + ', ' + str(paramModes))
    place_result_value(result, programCode, currentIndex)

def multiply_values(paramModes, programCode, currentIndex):
    product = 1
    params = [programCode[currentIndex + 1], programCode[currentIndex + 2]]
    for index, param in enumerate(params):
        mode = int(paramModes[index])
        value = get_instruction_value(param, mode, programCode)
        product = product * value
    place_result_value(product, programCode, currentIndex)

def store_user_input(paramModes, programCode, currentIndex):
    userInput = input('Please provide value: ')
    userValue = int(userInput)
    address = int(programCode[currentIndex + 1])
    programCode[address] = userValue

def output_value(paramModes, programCode, currentIndex):
    param = int(programCode[currentIndex + 1])
    mode = int(paramModes[0])
    address = currentIndex + 1 if mode == 1 else param
    print('T.E.S.T. output: [i=' + str(currentIndex) + '] -- ' + str(programCode[address]))
    # print('code ' + str(programCode))

def get_new_pointer_if_value(paramModes, programCode, currentIndex, isZero):
    distanceToPointer = None
    param = int(programCode[currentIndex + 1])
    mode = int(paramModes[0])
    value = param if mode == 1 else int(programCode[param])
    isValue = value == 0 if isZero else value != 0
    # print('point ' + str(isValue) + ', ' + str(currentIndex))
    if isValue:
        pointerParam = int(programCode[currentIndex + 2])
        pointerMode = int(paramModes[1])
        pointerAddress = pointerParam if pointerMode == 1 else int(programCode[pointerParam])
        distanceToPointer = pointerAddress - currentIndex
    return distanceToPointer

def jump_if_true(paramModes, programCode, currentIndex):
    notZero = False
    return get_new_pointer_if_value(paramModes, programCode, currentIndex, notZero)

def jump_if_false(paramModes, programCode, currentIndex):
    isZero = True
    return get_new_pointer_if_value(paramModes, programCode, currentIndex, isZero)

def is_less_than(value1, value2):
    return value1 < value2

def is_equal(value1, value2):
    return value1 == value2

COMPARISON_FUNCS = {
    '<': is_less_than,
    '=': is_equal
}

def check_value_comparison(paramModes, programCode, currentIndex, comparisonType):
    mode1 = int(paramModes[0])
    mode2 = int(paramModes[1])
    # mode3 = int(paramModes[2])
    param1 = int(programCode[currentIndex + 1])
    param2 = int(programCode[currentIndex + 2])
    param3 = int(programCode[currentIndex + 3])
    value1 = param1 if mode1 == 1 else int(programCode[param1])
    value2 = param2 if mode2 == 1 else int(programCode[param2])
    # value3 = param3 if mode3 == 1 else int(programCode[param3])
    # value3= int(programCode[param3])
    succeeds = COMPARISON_FUNCS[comparisonType](value1, value2)
    result = 1 if succeeds else 0
    # print('eval ' + str(result) + ', ' + str(value3) + ', ' + str(param3))
    programCode[param3] = result

def check_less_than(paramModes, programCode, currentIndex):
    check_value_comparison(paramModes, programCode, currentIndex, '<')

def check_equals(paramModes, programCode, currentIndex):
    check_value_comparison(paramModes, programCode, currentIndex, '=')

PROGRAM_TERMINATION_CODE = 99
PROGRAM_OPERATIONS = {
    1: add_values,
    2: multiply_values,
    3: store_user_input,
    4: output_value,
    5: jump_if_true,
    6: jump_if_false,
    7: check_less_than,
    8: check_equals
}
PARAMS_QTY_BY_OPERATION = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    99: -1
}

# todo -- modify for new, shorter ops, and implement immediate mode (value mode rather than addr. mode, only for values to add/multiply, not addr. to store)
# op 3: take input from user (me) and save at address (2-char op length)
# op 4: ouput value of param to console(?), e.g. 4,50 outputs val @ addr. 50 if in op mode not immediate mode (2-char op length)

def get_instruction(instructionCode):
    instructionText = str(instructionCode)
    index = len(instructionText) - 1
    paramModesRemaining = 0
    instruction = ''
    while paramModesRemaining == 0:
        instructionPart = instructionText[index] if index >= 0 else '0'
        instruction = instructionPart + instruction
        if (len(instruction) == 2):
            operation = int(instruction)
            paramModesRemaining = PARAMS_QTY_BY_OPERATION[operation]
        index = index - 1
    while paramModesRemaining > 0:
        paramMode = instructionText[index] if index >= 0 else '0'
        instruction = paramMode + instruction
        paramModesRemaining = paramModesRemaining - 1
        index = index - 1
    return instruction 

def perform_operation(currentIndex, programCode):
    instructionCode = programCode[currentIndex]
    # print('eyp ' + str(instructionCode) + ', ' + str(currentIndex) + ', ' + str(programCode))
    instruction = get_instruction(instructionCode)
    skipAheadLength = 0
    if (int(instruction) is not PROGRAM_TERMINATION_CODE):
        operationValue = int(instruction[len(instruction) - 2:])
        paramModes = []
        index = len(instruction) - 3
        while index >= 0:
            mode = instruction[index]
            paramModes.append(mode)
            index = index - 1
        operation = PROGRAM_OPERATIONS[operationValue]
        distanceToNextInstruction = operation(paramModes, programCode, currentIndex)
        skipAheadLength = len(paramModes) + 1 if distanceToNextInstruction is None else distanceToNextInstruction
    return skipAheadLength

def program_has_next(currentIndex, programCode):
    return len(programCode) > currentIndex and int(programCode[currentIndex]) is not PROGRAM_TERMINATION_CODE

def execute_program(programCode):
    currentIndex = 0
    instructionLength = perform_operation(currentIndex, programCode)
    currentIndex = currentIndex + instructionLength
    while instructionLength > 0:
        instructionLength = perform_operation(currentIndex, programCode)
        currentIndex = currentIndex + instructionLength

programData = []
with open('dec-05-diagnostic-program.txt') as programInput:
    programData = programInput.read().split(',')

execute_program(programData)