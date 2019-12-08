nodeMappings = []
with open('dec-06-orbital-map.txt') as mapFile:
    nodeMappings = mapFile.readlines()

nodes = dict()
for mapping in nodeMappings:
    tokens = mapping.split(')')
    parent = tokens[0].strip()
    child = tokens[1].strip()
    if parent in nodes:
        parentNode = nodes[parent]
        parentNode['childKeys'].append(child)
    else:
        nodes[str(parent)] = dict({ 
            'key': parent,
            'childKeys': [child],
            'parentKey': None 
        })
    if child in nodes:
        childNode = nodes[child]
        childNode['parentKey'] = parent 
    else:
        childNode = {
            'key': child,
            'parentKey': parent,
            'childKeys': []
        }
        nodes[str(child)] = childNode

def find_path_to_target(path, targetValue, allNodes):
    currentNodeKey = path[-1]
    currentNode = allNodes[currentNodeKey]
    adjacentNodeKeys = currentNode['childKeys'].copy()
    if currentNode['parentKey'] is not None:
        adjacentNodeKeys.insert(0, currentNode['parentKey'])
    foundTarget = False
    index = 0
    while index < len(adjacentNodeKeys) and not foundTarget:
        nextKey = adjacentNodeKeys[index]
        if nextKey == targetValue:
            path.append(nextKey)
            foundTarget = True
        elif nextKey not in path:
            path.append(nextKey)
            find_path_to_target(path, targetValue, allNodes)
            foundTarget = path[-1] == targetValue
            while not (foundTarget or path[-1] == currentNodeKey):
                del path[-1]
        index = index + 1
        
ME = 'YOU'
SANTA = 'SAN'
path = [ME]
find_path_to_target(path, SANTA, nodes)

# length of path minus one for distance between start and end, minus YOU, minus SAN
orbitalDistance = len(path) - 3 
print('orbital distance from ME to SANTA: ' + str(orbitalDistance))