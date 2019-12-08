import math

def calculateRequiredFuel(moduleMass):
    currentRequiredFuel = moduleMass
    totalRequiredFuel = 0
    while currentRequiredFuel > 0: 
        nextRequiredFuel = math.floor(currentRequiredFuel / 3) - 2
        if nextRequiredFuel > 0:
            totalRequiredFuel = totalRequiredFuel + nextRequiredFuel
        currentRequiredFuel = nextRequiredFuel
    return totalRequiredFuel

moduleMassesText = []
with open('dec-01-module-masses.txt') as moduleMassesFile:
    moduleMassesText = moduleMassesFile.readlines()

totalFuelRequired = 0
for moduleMassText in moduleMassesText:
    moduleMass = int(moduleMassText)
    moduleFuelRequired = calculateRequiredFuel(moduleMass)
    totalFuelRequired = totalFuelRequired + moduleFuelRequired

print('fuel required: ' + str(totalFuelRequired))