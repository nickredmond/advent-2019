def go_right(x, y, units):
    return x + units, y

def go_left(x, y, units):
    return x - units, y

def go_up(x, y, units): 
    return x, y + units

def go_down(x, y, units):
    return x, y - units

MOVEMENTS = {
    'R': go_right,
    'L': go_left,
    'U': go_up,
    'D': go_down
}

def get_line_segments(linePath):
    startingX = 0
    startingY = 0
    segments = []
    for direction in linePath:
        directionCode = direction[0]
        units = int(direction[1:])
        movement = MOVEMENTS[directionCode]
        endingX, endingY = movement(startingX, startingY, units)
        segment = {
            'x1': startingX,
            'y1': startingY,
            'x2': endingX,
            'y2': endingY
        }
        segments.append(segment)
        startingX, startingY = endingX, endingY
    return segments

def calculate_slope(x1, x2, y1, y2):
    return None if x1 == x2 else (y2 - y1) / (x2 - x1)

def calculate_y_intercept(m, x, y):
    return y - (m * x)

def calculate_intersect_x(m1, m2, b1, b2):
    return (b2 - b1) / (m1 - m2)

def calculate_intersect_y(m, x, b):
    return (m * x) + b

def intersects(intersectX, intersectY, segmentA, segmentB):
    ax1 = segmentA['x1']
    ax2 = segmentA['x2']
    ay1 = segmentA['y1']
    ay2 = segmentA['y2']
    bx1 = segmentB['x1']
    bx2 = segmentB['x2']
    by1 = segmentB['y1']
    by2 = segmentB['y2']
    leftX_a = min(ax1, ax2)
    leftX_b = min(bx1, bx2)
    rightX_a = max(ax1, ax2)
    rightX_b = max(bx1, bx2)
    topY_a = min(ay1, ay2)
    topY_b = min(by1, by2)
    botY_a = max(ay1, ay2)
    botY_b = max(by1, by2)
    maxLeftX = max(leftX_a, leftX_b)
    minRightX = min(rightX_a, rightX_b)
    maxTopY = max(topY_a, topY_b)
    minBotY = min(botY_a, botY_b)
    return intersectX >= maxLeftX and intersectX <= minRightX and intersectY >= maxTopY and intersectY <= minBotY

def calculate_distance_left(segment, intersectX, intersectY):
    return max(segment['x1'], segment['x2']) - intersectX

def calculate_distance_right(segment, intersectX, intersectY):
    return intersectX - min(segment['x1'], segment['x2'])

def calculate_distance_up(segment, intersectX, intersectY):
    return intersectY - min(segment['y1'], segment['y2'])

def calculate_distance_down(segment, intersectX, intersectY):
    return max(segment['y1'], segment['y2']) - intersectY

DISTANCE_FUNCTIONS = {
    'R': calculate_distance_right,
    'L': calculate_distance_left,
    'U': calculate_distance_up,
    'D': calculate_distance_down
}

def calculate_distance_traveled(index, lastDirectionTraveled, segments, intersectX, intersectY):
    totalDistance = 0
    currentIndex = 0
    while currentIndex < index:
        segment = segments[currentIndex]
        distance = abs(segment['x2'] - segment['x1']) if segment['y1'] == segment['y2'] else abs(segment['y2'] - segment['y1'])
        totalDistance = totalDistance + distance
        currentIndex = currentIndex + 1
    lastSegment = segments[index]
    lastDistance = DISTANCE_FUNCTIONS[lastDirectionTraveled](lastSegment, intersectX, intersectY)
    totalDistance = totalDistance + lastDistance
    return totalDistance

def find_closest_distance(pathA, pathB):
    segmentsA = get_line_segments(pathA)
    segmentsB = get_line_segments(pathB)
    closestDistance = None
    for indexA, segmentA in enumerate(segmentsA):
        for indexB, segmentB in enumerate(segmentsB):
            slopeA = calculate_slope(segmentA['x1'], segmentA['x2'], segmentA['y1'], segmentA['y2'])
            slopeB = calculate_slope(segmentB['x1'], segmentB['x2'], segmentB['y1'], segmentB['y2'])
            if slopeA != slopeB:
                yInterceptA = None if slopeA is None else calculate_y_intercept(slopeA, segmentA['x1'], segmentA['y1'])
                yInterceptB = None if slopeB is None else calculate_y_intercept(slopeB, segmentB['x1'], segmentB['y1'])
                intersectX = None
                intersectY = None
                if slopeA is None:
                    intersectX = segmentA['x1']
                    intersectY = calculate_intersect_y(slopeB, intersectX, yInterceptB)
                elif slopeB is None:
                    intersectX = segmentB['x1']
                    intersectY = calculate_intersect_y(slopeA, intersectX, yInterceptA)
                else:
                    intersectX = calculate_intersect_x(slopeA, slopeB, yInterceptA, yInterceptB)
                    intersectY = calculate_intersect_y(slopeA, intersectX, yInterceptA)
                if (indexA > 0 or indexB > 0) and intersects(intersectX, intersectY, segmentA, segmentB):
                    distanceA = calculate_distance_traveled(indexA, pathA[indexA][0], segmentsA, intersectX, intersectY)
                    distanceB = calculate_distance_traveled(indexB, pathB[indexB][0], segmentsB, intersectX, intersectY)
                    totalDistance = distanceA + distanceB
                    if closestDistance is None or totalDistance < closestDistance:
                        closestDistance = totalDistance 
    return closestDistance

pathA = []
pathB = []
with open('dec-03-pt1-line-paths.txt') as linePathsFile:
    linePaths = linePathsFile.readlines()
    pathA = linePaths[0].split(',')
    pathB = linePaths[1].split(',')

closestDistance = find_closest_distance(pathA, pathB)
print('closest distance to reach intersection: ' + str(closestDistance))