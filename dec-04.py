lowerLimit = 0
upperLimit = 0
with open('dec-04-password-range.txt') as passwordFile:
    passwordValues = passwordFile.readline().split('-')
    lowerLimit = int(passwordValues[0])
    upperLimit = int(passwordValues[1])

def is_password(value):
    valueText = str(value)
    lastRank = -1
    lastRankCount = 0
    increasing = True
    hasDouble = False
    i = 0
    while i < len(valueText) and increasing:
        rank = int(valueText[i])
        if rank == lastRank:
            lastRankCount = lastRankCount + 1
            hasDouble = hasDouble or (i == len(valueText) - 1 and lastRankCount == 2)
        else:
            increasing = rank > lastRank
            hasDouble = hasDouble or lastRankCount == 2
            lastRankCount = 1
            lastRank = rank
        i = i + 1
    return hasDouble and increasing

numberOfPasswords = 0
currentValue = lowerLimit
while currentValue <= upperLimit:
    if is_password(currentValue):
        numberOfPasswords = numberOfPasswords + 1
    currentValue = currentValue + 1

print('number of passwords: ' + str(numberOfPasswords))