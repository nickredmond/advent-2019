def place_result_value(value, programCode, currentIndex):
    placementIndex = int(programCode[currentIndex + 3])
    programCode[placementIndex] = value

def get_instruction_value(paramText, mode, programCode):
    paramValue = int(paramText)
    return paramValue if mode == 1 else int(programCode[paramValue])

def add_values(paramModes, programCode, currentIndex, inputs):
    values = []
    params = [programCode[currentIndex + 1], programCode[currentIndex + 2]]
    for index, param in enumerate(params):
        mode = int(paramModes[index])
        value = get_instruction_value(param, mode, programCode)
        values.append(value)
    result = sum(values) 
    place_result_value(result, programCode, currentIndex)
    return None, None

def multiply_values(paramModes, programCode, currentIndex, inputs):
    product = 1
    params = [programCode[currentIndex + 1], programCode[currentIndex + 2]]
    for index, param in enumerate(params):
        mode = int(paramModes[index])
        value = get_instruction_value(param, mode, programCode)
        product = product * value
    place_result_value(product, programCode, currentIndex)
    return None, None

def store_input(paramModes, programCode, currentIndex, inputs):
    inputValue = int(inputs[0])
    del inputs[0]
    address = int(programCode[currentIndex + 1])
    programCode[address] = inputValue
    return None, None

def output_value(paramModes, programCode, currentIndex, inputs):
    param = int(programCode[currentIndex + 1])
    mode = int(paramModes[0])
    address = currentIndex + 1 if mode == 1 else param
    return None, programCode[address]

def get_new_pointer_if_value(paramModes, programCode, currentIndex, isZero):
    distanceToPointer = None
    param = int(programCode[currentIndex + 1])
    mode = int(paramModes[0])
    value = param if mode == 1 else int(programCode[param])
    isValue = value == 0 if isZero else value != 0
    if isValue:
        pointerParam = int(programCode[currentIndex + 2])
        pointerMode = int(paramModes[1])
        pointerAddress = pointerParam if pointerMode == 1 else int(programCode[pointerParam])
        distanceToPointer = pointerAddress - currentIndex
    return distanceToPointer, None

def jump_if_true(paramModes, programCode, currentIndex, inputs):
    notZero = False
    return get_new_pointer_if_value(paramModes, programCode, currentIndex, notZero)

def jump_if_false(paramModes, programCode, currentIndex, inputs):
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
    param1 = int(programCode[currentIndex + 1])
    param2 = int(programCode[currentIndex + 2])
    param3 = int(programCode[currentIndex + 3])
    value1 = param1 if mode1 == 1 else int(programCode[param1])
    value2 = param2 if mode2 == 1 else int(programCode[param2])
    succeeds = COMPARISON_FUNCS[comparisonType](value1, value2)
    result = 1 if succeeds else 0
    programCode[param3] = result

def check_less_than(paramModes, programCode, currentIndex, inputs):
    check_value_comparison(paramModes, programCode, currentIndex, '<')
    return None, None

def check_equals(paramModes, programCode, currentIndex, inputs):
    check_value_comparison(paramModes, programCode, currentIndex, '=')
    return None, None

PROGRAM_TERMINATION_CODE = 99
PROGRAM_OPERATIONS = {
    1: add_values,
    2: multiply_values,
    3: store_input,
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

# NOTE maybe turn this into a class so "inputs" and "modes" can be stateful (instead of some isolated/global var)
# cuz some ops dont use all supplied params
def perform_operation(currentIndex, programCode, inputs):
    instructionCode = programCode[currentIndex]
    instruction = get_instruction(instructionCode)
    skipAheadLength = 0
    output = None
    if (int(instruction) is not PROGRAM_TERMINATION_CODE):
        operationValue = int(instruction[len(instruction) - 2:])
        paramModes = []
        index = len(instruction) - 3
        while index >= 0:
            mode = instruction[index]
            paramModes.append(mode)
            index = index - 1
        operation = PROGRAM_OPERATIONS[operationValue]
        distanceToNextInstruction, output = operation(paramModes, programCode, currentIndex, inputs)
        skipAheadLength = len(paramModes) + 1 if distanceToNextInstruction is None else distanceToNextInstruction
    return skipAheadLength, output

def program_has_next(currentIndex, programCode):
    return len(programCode) > currentIndex and int(programCode[currentIndex]) is not PROGRAM_TERMINATION_CODE

def execute_amplification(programCode, inputValue, phase):
    currentIndex = 0
    instructionLength = 1
    inputs = [int(phase), inputValue]
    finalOutput = None
    while instructionLength > 0:
        instructionLength, output = perform_operation(currentIndex, programCode, inputs)
        currentIndex = currentIndex + instructionLength
        if output is not None:
            finalOutput = output
    return finalOutput

numberOfAmplifiers = 5
phaseOptions = []
phaseOption = 0
while phaseOption < numberOfAmplifiers:
    phaseOptions.append(phaseOption)
    phaseOption = phaseOption + 1

# NOTE: yes, this is incredibly inefficient because Nick forgot the algorithm for combinations where ea. value is used once, and was on a plane at the time :shrug:
def phases_valid(currentPhaseCombination):
    phasesUsed = []
    index = 0
    isValid = True
    while index < len(currentPhaseCombination) and isValid:
        phase = currentPhaseCombination[index]
        if phase not in phasesUsed:
            phasesUsed.append(phase)
        else:
            isValid = False
        index = index + 1
    return isValid

def amplify_thrust(phases, programCode):
    programInput = 0
    for phase in phases:
        programCopy = programCode.copy()
        programInput = execute_amplification(programCode, programInput, phase)
    return programInput

def increment_phase_combination(currentCombination, maxDigit):
    digitsPlace = -1
    maxDigitsPlace = -1 * len(currentCombination)
    placeNeedsIncrement = True
    result = list(currentCombination)
    while digitsPlace >= maxDigitsPlace and placeNeedsIncrement:
        nextDigit = int(result[digitsPlace]) + 1
        placeNeedsIncrement = nextDigit > maxDigit
        if placeNeedsIncrement:
            nextDigit = 0
        result[digitsPlace] = str(nextDigit)
        digitsPlace = digitsPlace - 1
    return None if placeNeedsIncrement else ''.join(result)

maxThrust = 0
currentPhaseCombination = ''
maxPhaseValue = str(numberOfAmplifiers - 1)
maxPhaseCombination = ''
for _ in range(numberOfAmplifiers):
    maxPhaseCombination = maxPhaseCombination + maxPhaseValue
    currentPhaseCombination = currentPhaseCombination + '0'
maxPhaseCombination = int(maxPhaseCombination)

programData = []
with open('dec-07-amp-program.txt') as programInput:
    programData = programInput.read().split(',')

maxDigit = numberOfAmplifiers - 1
while currentPhaseCombination is not None:
    if phases_valid(currentPhaseCombination):
        thrust = amplify_thrust(currentPhaseCombination, programData)
        maxThrust = max(thrust, maxThrust)
    currentPhaseCombination = increment_phase_combination(currentPhaseCombination, maxDigit)

print('max. thrust after amplification: ' + str(maxThrust))
