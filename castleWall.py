# createWall.py

# TODO: add something cylindrical
# TODO: box-top of turret with ladder acesnding to ascend
# TODO: vary height of gate above the wallY
# TODO: parapet continues above gate
# TODO: half blocks above turret doors
# TODO: canons
# TODO: custom getHeight function
# TODO: torches by gates
# TODO: embelish turret windows
# TODO: decorative upsidedown stairs under flat turret roof
# TODO: add ladder to flat turret roof
# TODO: add half-blocks between parapets on flat turret roofs


from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
from mcpi import block
import sys
import json
from collections import deque

def splitList(myList):
    if (type(myList) is list):
        first = myList[0]
        if (len(myList) == 2):
            second = myList[1]
        else:
            second = ""
    else:
        first = myList
        second = ""
    return first, second

# read in the data file, configure, and initialize
with open(sys.argv[1]) as f:
  data = json.load(f)
config = data['config']
color = data['color']

# colors (block types)
wallColor, wallSubColor = splitList(color['wallColor'])
allureColor, allureSubColor = splitList(color['allureColor'])
turretColor, turretSubColor = splitList(color['turretColor'])
turretRoofColor, turretRoofSubColor = splitList(color['turretRoofColor'])
turretWindowColor, turretWindowSubColor = splitList(color['turretWindowColor'])
gateColor, gateSubColor = splitList(color['gateColor'])
gateWallColor, gateWallSubColor = splitList(color['gateWallColor'])
gateFloorColor, gateFloorSubColor = splitList(color['gateFloorColor'])
decorativeStairColor = color['decorativeStairColor'] # this will always be a scalar since the "subColor" will be the "direction"
parapetColor, parapetSubColor = splitList(color['parapetColor'])
parapetSlabColor, parapetSlabSubColor = splitList(color['parapetSlabColor'])
awningColor, awningSubColor = splitList(color['awningColor'])
awningSupportColor, awningSupportSubColor = splitList(color['awningSupportColor'])
awningBaseColor, awningBaseSubColor = splitList(color['awningBaseColor'])
decorativeTurretStairColor, decorativeTurretStairSubColor = splitList(color['decorativeTurretStairColor'])

# config
minWallHeight = config['minWallHeight']
maxWallHeight = config['maxWallHeight']
wallThickness = config['wallThickness']
allure = config['allure']
parapet = config['parapet'] and allure
heading = config['initialHeading']
prevHeading = heading
prevCmd = ""
lastSetBlocksWallColumnBottom = {}
lastSetBlocksWallColumnTop = {}
wallQueue = deque([])
allureQueue = deque([])
debugQueue = deque([])
turretQueue = deque([])
turretRoofQueue = deque([])
gateQueue = deque([])
cannonQueue = deque([])

# mcpi setup and initialization
mc = Minecraft.create()
mc.postToChat("Castle Wall!")
pos = mc.player.getPos()
wallY = mc.getHeight(pos.x, pos.z) + (maxWallHeight + minWallHeight) / 2

def cannon(x, y, z, heading, type=2):
    if (type == 1):
        if (heading == 0):
            cannonQueue.append((x, y, z, 145, 0)) # anvil
            cannonQueue.append((x, y, z-1, 23, 2)) # dispenser
            cannonQueue.append((x, y+1, z, 69, 5)) # lever
            cannonQueue.append((x+1, y, z, 96, 7)) # trap door 1
            cannonQueue.append((x-1, y, z, 96, 6)) # trap door 2
        elif (heading == 90):
            cannonQueue.append((x, y, z, 145, 1)) # anvil
            cannonQueue.append((x+1, y, z, 23, 5)) # dispenser
            cannonQueue.append((x, y+1, z, 69, 5)) # lever
            cannonQueue.append((x, y, z+1, 96, 5)) # trap door 1
            cannonQueue.append((x, y, z-1, 96, 4)) # trap door 2
        elif (heading == 180):
            cannonQueue.append((x, y, z, 145, 0)) # anvil
            cannonQueue.append((x, y, z+1, 23, 3)) # dispenser
            cannonQueue.append((x, y+1, z, 69, 5)) # lever
            cannonQueue.append((x+1, y, z, 96, 7)) # trap door 1
            cannonQueue.append((x-1, y, z, 96, 6)) # trap door 2
        elif (heading == 270):
            cannonQueue.append((x, y, z, 145, 1)) # anvil
            cannonQueue.append((x-1, y, z, 23, 4)) # dispenser
            cannonQueue.append((x, y+1, z, 69, 5)) # lever
            cannonQueue.append((x, y, z+1, 96, 5)) # trap door 1
            cannonQueue.append((x, y, z-1, 96, 4)) # trap door 2
    elif (type == 2):
        if (heading == 0):
            cannonQueue.append((x+1, y+1, z, 134, 2)) # right side, north, upper
            cannonQueue.append((x-1, y+1, z, 134, 2)) # left side, north, upper
            cannonQueue.append((x+1, y+1, z+1, 134, 3)) # right side, south, upper
            cannonQueue.append((x-1, y+1, z+1, 134, 3)) # left side, south, upper
            cannonQueue.append((x+1, y, z, 134, 6)) # right side, north, lower
            cannonQueue.append((x-1, y, z, 134, 6)) # left side, north, lower
            cannonQueue.append((x+1, y, z+1, 134, 7)) # right side, south, lower
            cannonQueue.append((x-1, y, z+1, 134, 7)) # left side, south, lower
            cannonQueue.append((x, y, z+1, 44, 42)) # wood slab
            cannonQueue.append((x, y, z+2, 44, 42)) # wood slab
            cannonQueue.append((x, y, z+3, 5)) # oak wood
            cannonQueue.append((x, y, z+4, 44, 2)) # wood slab
            cannonQueue.append((x, y+1, z-2, x, y+1, z+2, 35, 15))
            cannonQueue.append((x, y+2, z+2, 76)) # redstone torch
            cannonQueue.append((x, y+1, z-3, 77, 4)) # button
        elif (heading == 90):
            cannonQueue.append((x, y+1, z-1, 134, 1)) # north side, right, upper
            cannonQueue.append((x, y+1, z+1, 134, 1)) # south side, right, upper
            cannonQueue.append((x-1, y+1, z-1, 134, 0)) # north side, left, upper
            cannonQueue.append((x-1, y+1, z+1, 134, 0)) # south side, left, upper
            cannonQueue.append((x-1, y, z+1, 134, 4)) # north side, right, lower
            cannonQueue.append((x-1, y, z-1, 134, 4)) # south side, right, lower
            cannonQueue.append((x, y, z+1, 134, 5)) # north side, left, lower
            cannonQueue.append((x, y, z-1, 134, 5)) # south side, left, lower
            cannonQueue.append((x-1, y, z, 44, 42)) # wood slab
            cannonQueue.append((x-2, y, z, 44, 42)) # wood slab
            cannonQueue.append((x-3, y, z, 5)) # oak wood
            cannonQueue.append((x-4, y, z, 44, 2)) # wood slab
            cannonQueue.append((x-2, y+1, z, x+2, y+1, z, 35, 15))
            cannonQueue.append((x-2, y+2, z, 76)) # redstone torch
            cannonQueue.append((x+3, y+1, z, 77, 1)) # button
        elif (heading == 180):
            cannonQueue.append((x+1, y+1, z-1, 134, 2)) # right side, north, upper
            cannonQueue.append((x-1, y+1, z-1, 134, 2)) # left side, north, upper
            cannonQueue.append((x+1, y+1, z, 134, 3)) # right side, south, upper
            cannonQueue.append((x-1, y+1, z, 134, 3)) # left side, south, upper
            cannonQueue.append((x+1, y, z-1, 134, 6)) # right side, north, lower
            cannonQueue.append((x-1, y, z-1, 134, 6)) # left side, north, lower
            cannonQueue.append((x+1, y, z, 134, 7)) # right side, south, lower
            cannonQueue.append((x-1, y, z, 134, 7)) # left side, south, lower
            cannonQueue.append((x, y, z-1, 44, 42)) # wood slab
            cannonQueue.append((x, y, z-2, 44, 42)) # wood slab
            cannonQueue.append((x, y, z-3, 5)) # oak wood
            cannonQueue.append((x, y, z-4, 44, 2)) # wood slab
            cannonQueue.append((x, y+1, z-2, x, y+1, z+2, 35, 15))
            cannonQueue.append((x, y+2, z-2, 76)) # redstone torch
            cannonQueue.append((x, y+1, z+3, 77, 3)) # button
        elif (heading == 270):
            cannonQueue.append((x+1, y+1, z-1, 134, 1)) # north side, right, upper
            cannonQueue.append((x+1, y+1, z+1, 134, 1)) # south side, right, upper
            cannonQueue.append((x, y+1, z-1, 134, 0)) # north side, left, upper
            cannonQueue.append((x, y+1, z+1, 134, 0)) # south side, left, upper
            cannonQueue.append((x, y, z+1, 134, 4)) # north side, right, lower
            cannonQueue.append((x, y, z-1, 134, 4)) # south side, right, lower
            cannonQueue.append((x+1, y, z+1, 134, 5)) # north side, left, lower
            cannonQueue.append((x+1, y, z-1, 134, 5)) # south side, left, lower
            cannonQueue.append((x+1, y, z, 44, 42)) # wood slab
            cannonQueue.append((x+2, y, z, 44, 42)) # wood slab
            cannonQueue.append((x+3, y, z, 5)) # oak wood
            cannonQueue.append((x+4, y, z, 44, 2)) # wood slab
            cannonQueue.append((x+2, y+1, z, x-2, y+1, z, 35, 15))
            cannonQueue.append((x+2, y+2, z, 76)) # redstone torch
            cannonQueue.append((x-3, y+1, z, 77, 2)) # button

def processSetBlocksQueue(queue):
    for i in range(len(queue)):
        tuple = queue.popleft()
        if (len(tuple) == 8 and tuple[7] != ""):
            mc.setBlocks(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], tuple[6], tuple[7])
        elif (len(tuple) >= 7):
            mc.setBlocks(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], tuple[6])
        elif (len(tuple) == 5 and tuple[4] != ""):
            mc.setBlock(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4])
        elif (len(tuple) >= 4):
            mc.setBlock(tuple[0], tuple[1], tuple[2], tuple[3])
        else:
            print('something weird happened, len(tuple):', len(tuple))


print('processing path (', len(data['path']), 'steps )')
for i in range(len(data['path'])):
    step = data['path'][i]
    argv = step['argv']
    
    # message = 'step ' + str(i+1) + ' of ' + str(len(data['path'])) + ', cmd: ' + str(step['cmd']) + ', argv: ' + str(argv) + ', heading: ' + str(heading)
    mc.postToChat('step ' + str(i+1) + ' of ' + str(len(data['path'])))
    print('step', i+1, 'of', len(data['path']),'\tcmd:', step['cmd'], '\targv:', argv,'\theading:', heading)
    
    ### move
    if (step['cmd'] == 'move'):
        prevHeading = heading
        if (heading == 0): # north
            for z in range(argv):
                if (allure):
                    allureQueue.append((pos.x-(wallThickness//2+1), wallY+1, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+1, pos.z+(wallThickness//2+1), allureColor, allureSubColor))
                if (z == 0): # first one
                    wallQueue.append((pos.x-(wallThickness//2), mc.getHeight(pos.x, pos.z), pos.z, pos.x+(wallThickness//2), wallY, pos.z+(wallThickness//2), wallColor, wallSubColor))
                    if (parapet):
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z+2, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z+2, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+3, pos.z, block.TORCH))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+3, pos.z, block.TORCH))
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+3, pos.z+2, block.TORCH))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+3, pos.z+2, block.TORCH))
                    pos.z -= 1
                elif (z == argv - 1): # last one
                    wallQueue.append((pos.x-(wallThickness//2), mc.getHeight(pos.x, pos.z), pos.z, pos.x+(wallThickness//2), wallY, pos.z-(wallThickness//2), wallColor, wallSubColor))
                    if (parapet and z % 2 == 0):
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z-2, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z-2, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+3, pos.z, block.TORCH))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+3, pos.z, block.TORCH))
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+3, pos.z-2, block.TORCH))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+3, pos.z-2, block.TORCH))
                else: # everything else
                    wallQueue.append((pos.x-(wallThickness//2), min(wallY, mc.getHeight(pos.x, pos.z)), pos.z, pos.x+(wallThickness//2), wallY, pos.z, wallColor, wallSubColor))
                    if (parapet and z % 2 == 0):
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+3, pos.z, block.TORCH))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+3, pos.z, block.TORCH))
                    pos.z -= 1                        
                if ((z < argv - (wallThickness//2)) and (z > (wallThickness//2))):
                    if (wallY - mc.getHeight(pos.x, pos.z) < minWallHeight):
                        wallY += 1
                    elif (wallY - mc.getHeight(pos.x, pos.z) > maxWallHeight):
                        wallY -= 1
                        
        elif (heading == 90): # east
            for x in range(argv):
                if (allure):
                    allureQueue.append((pos.x-(wallThickness//2+1), wallY+1, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+1, pos.z+(wallThickness//2+1), allureColor, allureSubColor))
                if (x == 0): # first one
                    wallQueue.append((pos.x, mc.getHeight(pos.x, pos.z), pos.z-(wallThickness//2), pos.x-(wallThickness//2), wallY, pos.z+(wallThickness//2), wallColor, wallSubColor))
                    if (parapet):
                        allureQueue.append((pos.x, wallY+2, pos.z-(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x, wallY+2, pos.z+(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x-2, wallY+2, pos.z-(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x-2, wallY+2, pos.z+(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x, wallY+3, pos.z-(wallThickness//2+1), block.TORCH))
                        allureQueue.append((pos.x, wallY+3, pos.z+(wallThickness//2+1), block.TORCH))
                        allureQueue.append((pos.x-2, wallY+3, pos.z-(wallThickness//2+1), block.TORCH))
                        allureQueue.append((pos.x-2, wallY+3, pos.z+(wallThickness//2+1), block.TORCH))
                    pos.x += 1
                elif (x == argv - 1): # last one
                    wallQueue.append((pos.x, mc.getHeight(pos.x, pos.z), pos.z-(wallThickness//2), pos.x+(wallThickness//2), wallY, pos.z+(wallThickness//2), wallColor, wallSubColor))
                    if (parapet and x % 2 == 0):
                        allureQueue.append((pos.x, wallY+2, pos.z-(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x, wallY+2, pos.z+(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x+2, wallY+2, pos.z-(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x+2, wallY+2, pos.z+(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x, wallY+3, pos.z-(wallThickness//2+1), block.TORCH))
                        allureQueue.append((pos.x, wallY+3, pos.z+(wallThickness//2+1), block.TORCH))
                        allureQueue.append((pos.x+2, wallY+3, pos.z-(wallThickness//2+1), block.TORCH))
                        allureQueue.append((pos.x+2, wallY+3, pos.z+(wallThickness//2+1), block.TORCH))
                else: # everything else
                    wallQueue.append((pos.x, min(wallY, mc.getHeight(pos.x, pos.z)), pos.z-(wallThickness//2), pos.x, wallY, pos.z+(wallThickness//2), wallColor, wallSubColor))
                    if (parapet and x % 2 == 0):
                        allureQueue.append((pos.x, wallY+2, pos.z-(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x, wallY+2, pos.z+(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x, wallY+3, pos.z-(wallThickness//2+1), block.TORCH))
                        allureQueue.append((pos.x, wallY+3, pos.z+(wallThickness//2+1), block.TORCH))
                    pos.x += 1
                if ((x < argv - (wallThickness//2)) and (x > (wallThickness//2))):
                    if (wallY - mc.getHeight(pos.x, pos.z) < minWallHeight):
                        wallY += 1
                    elif (wallY - mc.getHeight(pos.x, pos.z) > maxWallHeight):
                        wallY -= 1

        elif (heading == 180): # south
            for z in range(argv):
                if (allure):
                    allureQueue.append((pos.x-(wallThickness//2+1), wallY+1, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+1, pos.z+(wallThickness//2+1), allureColor, allureSubColor))
                if (z == 0): # first one
                    wallQueue.append((pos.x-(wallThickness//2), mc.getHeight(pos.x, pos.z), pos.z, pos.x+(wallThickness//2), wallY, pos.z-(wallThickness//2), wallColor, wallSubColor))
                    if (parapet):
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z-2, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z-2, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+3, pos.z, block.TORCH))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+3, pos.z, block.TORCH))
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+3, pos.z-2, block.TORCH))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+3, pos.z-2, block.TORCH))
                    pos.z += 1
                elif (z == argv - 1): # last one
                    wallQueue.append((pos.x-(wallThickness//2), mc.getHeight(pos.x, pos.z), pos.z, pos.x+(wallThickness//2), wallY, pos.z+(wallThickness//2), wallColor, wallSubColor))
                    if (parapet and z % 2 == 0):
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z+2, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z+2, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+3, pos.z, block.TORCH))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+3, pos.z, block.TORCH))
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+3, pos.z+2, block.TORCH))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+3, pos.z+2, block.TORCH))
                else: # everything else
                    wallQueue.append((pos.x-(wallThickness//2), min(wallY, mc.getHeight(pos.x, pos.z)), pos.z, pos.x+(wallThickness//2), wallY, pos.z, wallColor, wallSubColor))
                    if (parapet and z % 2 == 0):
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z, parapetColor, parapetSubColor))
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+3, pos.z, block.TORCH))
                        allureQueue.append((pos.x+(wallThickness//2+1), wallY+3, pos.z, block.TORCH))
                    pos.z += 1                        
                if ((z < argv - (wallThickness//2)) and (z > (wallThickness//2))):
                    if (wallY - mc.getHeight(pos.x, pos.z) < minWallHeight):
                        wallY += 1
                    elif (wallY - mc.getHeight(pos.x, pos.z) > maxWallHeight):
                        wallY -= 1

        elif (heading == 270): # west
            for x in range(argv):
                if (allure):
                    allureQueue.append((pos.x-(wallThickness//2+1), wallY+1, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+1, pos.z+(wallThickness//2+1), allureColor, allureSubColor))
                if (x == 0): # first one
                    wallQueue.append((pos.x, mc.getHeight(pos.x, pos.z), pos.z-(wallThickness//2), pos.x+(wallThickness//2), wallY, pos.z+(wallThickness//2), wallColor, wallSubColor))
                    if (parapet):
                        allureQueue.append((pos.x, wallY+2, pos.z-(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x, wallY+2, pos.z+(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x+2, wallY+2, pos.z-(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x+2, wallY+2, pos.z+(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x, wallY+3, pos.z-(wallThickness//2+1), block.TORCH))
                        allureQueue.append((pos.x, wallY+3, pos.z+(wallThickness//2+1), block.TORCH))
                        allureQueue.append((pos.x+2, wallY+3, pos.z-(wallThickness//2+1), block.TORCH))
                        allureQueue.append((pos.x+2, wallY+3, pos.z+(wallThickness//2+1), block.TORCH))
                    pos.x -= 1
                elif (x == argv - 1): # last one
                    wallQueue.append((pos.x, mc.getHeight(pos.x, pos.z), pos.z-(wallThickness//2), pos.x-(wallThickness//2), wallY, pos.z+(wallThickness//2), wallColor, wallSubColor))
                    if (parapet and x % 2 == 0):
                        allureQueue.append((pos.x, wallY+2, pos.z-(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x, wallY+2, pos.z+(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x-2, wallY+2, pos.z-(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x-2, wallY+2, pos.z+(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x, wallY+3, pos.z-(wallThickness//2+1), block.TORCH))
                        allureQueue.append((pos.x, wallY+3, pos.z+(wallThickness//2+1), block.TORCH))
                        allureQueue.append((pos.x-2, wallY+3, pos.z-(wallThickness//2+1), block.TORCH))
                        allureQueue.append((pos.x-2, wallY+3, pos.z+(wallThickness//2+1), block.TORCH))
                else: # everything else
                    wallQueue.append((pos.x, min(wallY, mc.getHeight(pos.x, pos.z)), pos.z-(wallThickness//2), pos.x, wallY, pos.z+(wallThickness//2), wallColor, wallSubColor))
                    if (parapet and x % 2 == 0):
                        allureQueue.append((pos.x, wallY+2, pos.z-(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x, wallY+2, pos.z+(wallThickness//2+1), parapetColor, parapetSubColor))
                        allureQueue.append((pos.x, wallY+3, pos.z-(wallThickness//2+1), block.TORCH))
                        allureQueue.append((pos.x, wallY+3, pos.z+(wallThickness//2+1), block.TORCH))
                    pos.x -= 1
                if ((x < argv - (wallThickness//2)) and (x > (wallThickness//2))):
                    if (wallY - mc.getHeight(pos.x, pos.z) < minWallHeight):
                        wallY += 1
                    elif (wallY - mc.getHeight(pos.x, pos.z) > maxWallHeight):
                        wallY -= 1

    ### turn left
    elif (step['cmd'] == 'left'):
        prevHeading = heading
        debugQueue.append((pos.x, wallY + 3, pos.z, pos.x, wallY + 3, pos.z, 103))
        heading = (heading - argv + 360) % 360
        

    ### turn right
    elif (step['cmd'] == 'right'):
        prevHeading = heading
        debugQueue.append((pos.x, wallY + 3, pos.z, pos.x, wallY + 3, pos.z, 103))
        heading = (heading + argv) % 360
        
    elif (step['cmd'] == 'turret'):
        turretHeight, roofType = splitList(argv)
        if (roofType == ""):
            roofType = "flat"
            
        windowNorth = not(prevHeading == 180 or heading == 0)
        windowSouth = not(prevHeading == 0 or heading == 180)
        windowEast = not(prevHeading == 270 or heading == 90)
        windowWest = not(prevHeading == 90 or heading == 270)

        # clear the ground
        turretQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+2, pos.z+(wallThickness//2+1), block.AIR))
    
        # main walls
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z-(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY+2+turretHeight, pos.z-(wallThickness//2+2), turretColor, turretSubColor))
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z+(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY+2+turretHeight, pos.z+(wallThickness//2+2), turretColor, turretSubColor))
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z-(wallThickness//2+2), pos.x-(wallThickness//2+2), wallY+2+turretHeight, pos.z+(wallThickness//2+2), turretColor, turretSubColor))
        turretQueue.append((pos.x+(wallThickness//2+2), wallY+2, pos.z-(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY+2+turretHeight, pos.z+(wallThickness//2+2), turretColor, turretSubColor))
        
        # outer decorative down hangers
        turretQueue.append((pos.x+(wallThickness//2+2), wallY+1, pos.z-(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY, pos.z-(wallThickness//2+2), turretColor, turretSubColor))
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+1, pos.z-(wallThickness//2+2), pos.x-(wallThickness//2+2), wallY, pos.z-(wallThickness//2+2), turretColor, turretSubColor))
        turretQueue.append((pos.x+(wallThickness//2+2), wallY+1, pos.z+(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY, pos.z+(wallThickness//2+2), turretColor, turretSubColor))
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+1, pos.z+(wallThickness//2+2), pos.x-(wallThickness//2+2), wallY, pos.z+(wallThickness//2+2), turretColor, turretSubColor))

        # inner decorative down hangers
        turretQueue.append((pos.x+(wallThickness//2+1), wallY, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY-2, pos.z-(wallThickness//2+1), turretColor, turretSubColor))
        turretQueue.append((pos.x-(wallThickness//2+1), wallY, pos.z-(wallThickness//2+1), pos.x-(wallThickness//2+1), wallY-2, pos.z-(wallThickness//2+1), turretColor, turretSubColor))
        turretQueue.append((pos.x+(wallThickness//2+1), wallY, pos.z+(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY-2, pos.z+(wallThickness//2+1), turretColor, turretSubColor))
        turretQueue.append((pos.x-(wallThickness//2+1), wallY, pos.z+(wallThickness//2+1), pos.x-(wallThickness//2+1), wallY-2, pos.z+(wallThickness//2+1), turretColor, turretSubColor))

        # cut out windows on all sides, the doorways will cut the opening larger in certain areas
        turretQueue.append((pos.x-1, wallY+3, pos.z-(wallThickness//2+2), pos.x+1, wallY+4, pos.z-(wallThickness//2+2), turretWindowColor, turretWindowSubColor))
        turretQueue.append((pos.x-1, wallY+3, pos.z+(wallThickness//2+2), pos.x+1, wallY+4, pos.z+(wallThickness//2+2), turretWindowColor, turretWindowSubColor))
        turretQueue.append((pos.x+(wallThickness//2+2), wallY+3, pos.z-1, pos.x+(wallThickness//2+2), wallY+4, pos.z+1, turretWindowColor, turretWindowSubColor))
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+3, pos.z-1, pos.x-(wallThickness//2+2), wallY+4, pos.z+1, turretWindowColor, turretWindowSubColor))

        # window awning/dressing
        if (windowNorth):
            turretQueue.append((pos.x-2, wallY+2, pos.z-(wallThickness//2+3), pos.x+2, wallY+2, pos.z-(wallThickness//2+3), decorativeTurretStairColor, 6))
            turretQueue.append((pos.x-2, wallY+5, pos.z-(wallThickness//2+3), pos.x+2, wallY+5, pos.z-(wallThickness//2+3), decorativeTurretStairColor, 2))
            turretQueue.append((pos.x-2, wallY+3, pos.z-(wallThickness//2+3), pos.x-2, wallY+4, pos.z-(wallThickness//2+3), awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x+2, wallY+3, pos.z-(wallThickness//2+3), pos.x+2, wallY+4, pos.z-(wallThickness//2+3), awningSupportColor, awningSupportSubColor))
        if (windowSouth):
            turretQueue.append((pos.x-2, wallY+2, pos.z+(wallThickness//2+3), pos.x+2, wallY+2, pos.z+(wallThickness//2+3), decorativeTurretStairColor, 7))
            turretQueue.append((pos.x-2, wallY+5, pos.z+(wallThickness//2+3), pos.x+2, wallY+5, pos.z+(wallThickness//2+3), decorativeTurretStairColor, 3))
            turretQueue.append((pos.x-2, wallY+3, pos.z+(wallThickness//2+3), pos.x-2, wallY+4, pos.z+(wallThickness//2+3), awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x+2, wallY+3, pos.z+(wallThickness//2+3), pos.x+2, wallY+4, pos.z+(wallThickness//2+3), awningSupportColor, awningSupportSubColor))
        if (windowEast):
            turretQueue.append((pos.x+(wallThickness//2+3), wallY+2, pos.z-2, pos.x+(wallThickness//2+3), wallY+2, pos.z+2, decorativeTurretStairColor, 5))
            turretQueue.append((pos.x+(wallThickness//2+3), wallY+5, pos.z-2, pos.x+(wallThickness//2+3), wallY+5, pos.z+2, decorativeTurretStairColor, 1))
            turretQueue.append((pos.x+(wallThickness//2+3), wallY+3, pos.z-2, pos.x+(wallThickness//2+3), wallY+4, pos.z-2, awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x+(wallThickness//2+3), wallY+3, pos.z+2, pos.x+(wallThickness//2+3), wallY+4, pos.z+2, awningSupportColor, awningSupportSubColor))
        if (windowWest):
            turretQueue.append((pos.x-(wallThickness//2+3), wallY+2, pos.z-2, pos.x-(wallThickness//2+3), wallY+2, pos.z+2, decorativeTurretStairColor, 4))
            turretQueue.append((pos.x-(wallThickness//2+3), wallY+5, pos.z-2, pos.x-(wallThickness//2+3), wallY+5, pos.z+2, decorativeTurretStairColor, 0))
            turretQueue.append((pos.x-(wallThickness//2+3), wallY+3, pos.z-2, pos.x-(wallThickness//2+3), wallY+4, pos.z-2, awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x-(wallThickness//2+3), wallY+3, pos.z+2, pos.x-(wallThickness//2+3), wallY+4, pos.z+2, awningSupportColor, awningSupportSubColor))

        # door cutouts / archways
        if (prevHeading == 0 or heading == 180): # north on previous or south on current
            turretQueue.append((pos.x-1, wallY+2, pos.z+(wallThickness//2+2), pos.x+1, wallY+5, pos.z+(wallThickness//2+2), block.AIR))
            turretQueue.append((pos.x-1, wallY+5, pos.z+(wallThickness//2+2), decorativeStairColor, 5))
            turretQueue.append((pos.x+1, wallY+5, pos.z+(wallThickness//2+2), decorativeStairColor, 4))
            turretQueue.append((pos.x, wallY+6, pos.z+(wallThickness//2+3), awningColor, awningSubColor))
            turretQueue.append((pos.x-1, wallY+5, pos.z+(wallThickness//2+3), awningColor, awningSubColor+8))
            turretQueue.append((pos.x+1, wallY+5, pos.z+(wallThickness//2+3), awningColor, awningSubColor+8))
            turretQueue.append((pos.x-2, wallY+5, pos.z+(wallThickness//2+3), awningColor, awningSubColor))
            turretQueue.append((pos.x+2, wallY+5, pos.z+(wallThickness//2+3), awningColor, awningSubColor))
            turretQueue.append((pos.x-2, wallY+4, pos.z+(wallThickness//2+3), awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x+2, wallY+4, pos.z+(wallThickness//2+3), awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x-2, wallY+3, pos.z+(wallThickness//2+3), awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x+2, wallY+3, pos.z+(wallThickness//2+3), awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x-2, wallY+2, pos.z+(wallThickness//2+3), awningBaseColor, awningBaseSubColor))
            turretQueue.append((pos.x+2, wallY+2, pos.z+(wallThickness//2+3), awningBaseColor, awningBaseSubColor))
        if (prevHeading == 90 or heading == 270): # east on previous or west on current
            turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z-1, pos.x-(wallThickness//2+2), wallY+5, pos.z+1, block.AIR))
            turretQueue.append((pos.x-(wallThickness//2+2), wallY+5, pos.z-1, decorativeStairColor, 7))
            turretQueue.append((pos.x-(wallThickness//2+2), wallY+5, pos.z+1, decorativeStairColor, 6))
            turretQueue.append((pos.x-(wallThickness//2+3), wallY+6, pos.z, awningColor, awningSubColor))
            turretQueue.append((pos.x-(wallThickness//2+3), wallY+5, pos.z-1, awningColor, awningSubColor+8))
            turretQueue.append((pos.x-(wallThickness//2+3), wallY+5, pos.z+1, awningColor, awningSubColor+8))
            turretQueue.append((pos.x-(wallThickness//2+3), wallY+5, pos.z-2, awningColor, awningSubColor))
            turretQueue.append((pos.x-(wallThickness//2+3), wallY+5, pos.z+2, awningColor, awningSubColor))
            turretQueue.append((pos.x-(wallThickness//2+3), wallY+4, pos.z-2, awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x-(wallThickness//2+3), wallY+4, pos.z+2, awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x-(wallThickness//2+3), wallY+3, pos.z-2, awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x-(wallThickness//2+3), wallY+3, pos.z+2, awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x-(wallThickness//2+3), wallY+2, pos.z-2, awningBaseColor, awningBaseSubColor))
            turretQueue.append((pos.x-(wallThickness//2+3), wallY+2, pos.z+2, awningBaseColor, awningBaseSubColor))
        if (prevHeading == 180 or heading == 0): # south on previous or north on current
            turretQueue.append((pos.x-1, wallY+2, pos.z-(wallThickness//2+2), pos.x+1, wallY+5, pos.z-(wallThickness//2+2), block.AIR))
            turretQueue.append((pos.x-1, wallY+5, pos.z-(wallThickness//2+2), decorativeStairColor, 5))
            turretQueue.append((pos.x+1, wallY+5, pos.z-(wallThickness//2+2), decorativeStairColor ,4))
            turretQueue.append((pos.x, wallY+6, pos.z-(wallThickness//2+3), awningColor, awningSubColor))
            turretQueue.append((pos.x-1, wallY+5, pos.z-(wallThickness//2+3), awningColor, awningSubColor+8))
            turretQueue.append((pos.x+1, wallY+5, pos.z-(wallThickness//2+3), awningColor, awningSubColor+8))
            turretQueue.append((pos.x-2, wallY+5, pos.z-(wallThickness//2+3), awningColor, awningSubColor))
            turretQueue.append((pos.x+2, wallY+5, pos.z-(wallThickness//2+3), awningColor, awningSubColor))
            turretQueue.append((pos.x-2, wallY+4, pos.z-(wallThickness//2+3), awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x+2, wallY+4, pos.z-(wallThickness//2+3), awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x-2, wallY+3, pos.z-(wallThickness//2+3), awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x+2, wallY+3, pos.z-(wallThickness//2+3), awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x-2, wallY+2, pos.z-(wallThickness//2+3), awningBaseColor, awningBaseSubColor))
            turretQueue.append((pos.x+2, wallY+2, pos.z-(wallThickness//2+3), awningBaseColor, awningBaseSubColor))
        if (prevHeading == 270 or heading == 90): # west on previous or east on current
            turretQueue.append((pos.x+(wallThickness//2+2), wallY+2, pos.z-1, pos.x+(wallThickness//2+2), wallY+5, pos.z+1, block.AIR))
            turretQueue.append((pos.x+(wallThickness//2+2), wallY+5, pos.z-1, decorativeStairColor, 7))
            turretQueue.append((pos.x+(wallThickness//2+2), wallY+5, pos.z+1, decorativeStairColor, 6))
            turretQueue.append((pos.x+(wallThickness//2+3), wallY+6, pos.z, awningColor, awningSubColor))
            turretQueue.append((pos.x+(wallThickness//2+3), wallY+5, pos.z-1, awningColor, awningSubColor+8))
            turretQueue.append((pos.x+(wallThickness//2+3), wallY+5, pos.z+1, awningColor, awningSubColor+8))
            turretQueue.append((pos.x+(wallThickness//2+3), wallY+5, pos.z-2, awningColor, awningSubColor))
            turretQueue.append((pos.x+(wallThickness//2+3), wallY+5, pos.z+2, awningColor, awningSubColor))
            turretQueue.append((pos.x+(wallThickness//2+3), wallY+4, pos.z-2, awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x+(wallThickness//2+3), wallY+4, pos.z+2, awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x+(wallThickness//2+3), wallY+3, pos.z-2, awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x+(wallThickness//2+3), wallY+3, pos.z+2, awningSupportColor, awningSupportSubColor))
            turretQueue.append((pos.x+(wallThickness//2+3), wallY+2, pos.z-2, awningBaseColor, awningBaseSubColor))
            turretQueue.append((pos.x+(wallThickness//2+3), wallY+2, pos.z+2, awningBaseColor, awningBaseSubColor))
        
        if (roofType == "tapered"):
            for j in range(wallThickness + 1, -1, -1):
                turretRoofQueue.append((pos.x-j, wallY+turretHeight+2+2*(wallThickness+1-j), pos.z-j, pos.x+j, wallY+turretHeight+3+2*(wallThickness+1-j), pos.z+j, turretRoofColor, turretRoofSubColor))
                turretRoofQueue.append((pos.x-j, wallY+turretHeight+3+2*(wallThickness+1-j)+1, pos.z-j, block.TORCH))
                turretRoofQueue.append((pos.x+j, wallY+turretHeight+3+2*(wallThickness+1-j)+1, pos.z-j, block.TORCH))
                turretRoofQueue.append((pos.x-j, wallY+turretHeight+3+2*(wallThickness+1-j)+1, pos.z+j, block.TORCH))
                turretRoofQueue.append((pos.x+j, wallY+turretHeight+3+2*(wallThickness+1-j)+1, pos.z+j, block.TORCH))
        elif (roofType == "flat"):
            turretRoofQueue.append((pos.x-(wallThickness+1), wallY+turretHeight+2, pos.z-(wallThickness+1), pos.x+(wallThickness+1), wallY+turretHeight+3, pos.z+(wallThickness+1), turretRoofColor, turretRoofSubColor))
            for j in range(2*(wallThickness+1)):
                if (j % 2 == 0):
                    # parapet
                    turretRoofQueue.append((pos.x-(wallThickness+1)+j, wallY+turretHeight+4, pos.z-(wallThickness+1), parapetColor, parapetSubColor))
                    turretRoofQueue.append((pos.x+(wallThickness+1)-j, wallY+turretHeight+4, pos.z+(wallThickness+1), parapetColor, parapetSubColor))
                    turretRoofQueue.append((pos.x-(wallThickness+1), wallY+turretHeight+4, pos.z+(wallThickness+1)-j, parapetColor, parapetSubColor))
                    turretRoofQueue.append((pos.x+(wallThickness+1), wallY+turretHeight+4, pos.z-(wallThickness+1)+j, parapetColor, parapetSubColor))
                    # torches
                    turretRoofQueue.append((pos.x-(wallThickness+1)+j, wallY+turretHeight+5, pos.z-(wallThickness+1), block.TORCH))
                    turretRoofQueue.append((pos.x+(wallThickness+1)-j, wallY+turretHeight+5, pos.z+(wallThickness+1), block.TORCH))
                    turretRoofQueue.append((pos.x-(wallThickness+1), wallY+turretHeight+5, pos.z+(wallThickness+1)-j, block.TORCH))
                    turretRoofQueue.append((pos.x+(wallThickness+1), wallY+turretHeight+5, pos.z-(wallThickness+1)+j, block.TORCH))
                else:
                    turretRoofQueue.append((pos.x-(wallThickness+1)+j, wallY+turretHeight+4, pos.z-(wallThickness+1), parapetSlabColor, parapetSlabSubColor))
                    turretRoofQueue.append((pos.x+(wallThickness+1)-j, wallY+turretHeight+4, pos.z+(wallThickness+1), parapetSlabColor, parapetSlabSubColor))
                    turretRoofQueue.append((pos.x-(wallThickness+1), wallY+turretHeight+4, pos.z+(wallThickness+1)-j, parapetSlabColor, parapetSlabSubColor))
                    turretRoofQueue.append((pos.x+(wallThickness+1), wallY+turretHeight+4, pos.z-(wallThickness+1)+j, parapetSlabColor, parapetSlabSubColor))
                    
                    #turretRoofQueue.append((pos.x+(wallThickness+1)+j, wallY+turretHeight+4, pos.z-(wallThickness+1), parapetSlabColor, parapetSlabSubColor))
                    #turretRoofQueue.append((pos.x+(wallThickness+1)+j, wallY+turretHeight+4, pos.z+(wallThickness+1), parapetSlabColor, parapetSlabSubColor))
                    #turretRoofQueue.append((pos.x-(wallThickness+1)+j, wallY+turretHeight+4, pos.z-(wallThickness+1), parapetSlabColor, parapetSlabSubColor))
                    #turretRoofQueue.append((pos.x-(wallThickness+1)+j, wallY+turretHeight+4, pos.z+(wallThickness+1), parapetSlabColor, parapetSlabSubColor))
            # ladder
            turretRoofQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z+(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+3+turretHeight, pos.z+(wallThickness//2+1), block.LADDER))
        
        # roof downhangers
        turretRoofQueue.append((pos.x-(wallThickness+1), wallY+turretHeight+1, pos.z-(wallThickness+1), pos.x-(wallThickness+1), wallY+turretHeight-1, pos.z-(wallThickness+1), turretRoofColor, turretRoofSubColor))
        turretRoofQueue.append((pos.x-(wallThickness+1), wallY+turretHeight+1, pos.z+(wallThickness+1), pos.x-(wallThickness+1), wallY+turretHeight-1, pos.z+(wallThickness+1), turretRoofColor, turretRoofSubColor))
        turretRoofQueue.append((pos.x+(wallThickness+1), wallY+turretHeight+1, pos.z-(wallThickness+1), pos.x+(wallThickness+1), wallY+turretHeight-1, pos.z-(wallThickness+1), turretRoofColor, turretRoofSubColor))
        turretRoofQueue.append((pos.x+(wallThickness+1), wallY+turretHeight+1, pos.z+(wallThickness+1), pos.x+(wallThickness+1), wallY+turretHeight-1, pos.z+(wallThickness+1), turretRoofColor, turretRoofSubColor))
        
        turretRoofQueue.append((pos.x-(wallThickness+1), wallY+turretHeight+1 ,pos.z-(wallThickness), decorativeTurretStairColor, 7))
        turretRoofQueue.append((pos.x-(wallThickness+1), wallY+turretHeight+1 ,pos.z+(wallThickness), decorativeTurretStairColor, 6))
        turretRoofQueue.append((pos.x+(wallThickness+1), wallY+turretHeight+1 ,pos.z-(wallThickness), decorativeTurretStairColor, 7))
        turretRoofQueue.append((pos.x+(wallThickness+1), wallY+turretHeight+1 ,pos.z+(wallThickness), decorativeTurretStairColor, 6))
        
        turretRoofQueue.append((pos.x-(wallThickness), wallY+turretHeight+1, pos.z-(wallThickness+1), decorativeTurretStairColor, 5))        
        turretRoofQueue.append((pos.x+(wallThickness), wallY+turretHeight+1, pos.z-(wallThickness+1), decorativeTurretStairColor, 4))
        turretRoofQueue.append((pos.x-(wallThickness), wallY+turretHeight+1, pos.z+(wallThickness+1), decorativeTurretStairColor, 5))
        turretRoofQueue.append((pos.x+(wallThickness), wallY+turretHeight+1, pos.z+(wallThickness+1), decorativeTurretStairColor, 4))        
        
    elif (step['cmd'] == 'gate'):
        gateSize, state = splitList(argv)
        if (heading == 0 or heading == 180): # north or south
            if (heading == 180): # heading south, increment position first
                pos.z += gateSize
            # clear the entryway of debris
            gateQueue.append((pos.x-(wallThickness//2), wallY-3, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2), mc.getHeight(pos.x+(wallThickness//2), pos.z-gateSize+(wallThickness//2*2)), pos.z-argv+(wallThickness//2*2), block.AIR)) 
            
            # 4 posts
            gateQueue.append((pos.x-1, mc.getHeight(pos.x-1, pos.z-(wallThickness//2+1)), pos.z-(wallThickness//2+1), pos.x-2, wallY-1, pos.z-(wallThickness//2+1), gateWallColor, gateWallSubColor))
            gateQueue.append((pos.x+1, mc.getHeight(pos.x-1, pos.z-(wallThickness//2+1)), pos.z-(wallThickness//2+1), pos.x+2, wallY-1, pos.z-(wallThickness//2+1), gateWallColor, gateWallSubColor))
            gateQueue.append((pos.x-1, mc.getHeight(pos.x-1, pos.z-gateSize+(wallThickness//2*2)), pos.z-gateSize+(wallThickness//2*2), pos.x-2, wallY-1, pos.z-gateSize+(wallThickness//2*2), gateWallColor, gateWallSubColor))
            gateQueue.append((pos.x+1, mc.getHeight(pos.x-1, pos.z-gateSize+(wallThickness//2*2)), pos.z-gateSize+(wallThickness//2*2), pos.x+2, wallY-1, pos.z-gateSize+(wallThickness//2*2), gateWallColor, gateWallSubColor))
            
            # torches
            # for j in range(5):
            #     if (j == 2):
            #         continue
            #     gateQueue.append((pos.x-2+j, mc.getHeight(pos.x-2+j, pos.z-(wallThickness//2)), pos.z-(wallThickness//2), block.TORCH)) # south row of torches
            #     gateQueue.append((pos.x-2+j, mc.getHeight(pos.x-2+j, pos.z-gateSize+(wallThickness//2*2)+1), pos.z-gateSize+(wallThickness//2*2)+1, block.TORCH)) # north row of torches
            
            # top plate
            gateQueue.append((pos.x-2, wallY, pos.z-(wallThickness//2+1), pos.x+2, wallY+3, pos.z-gateSize+(wallThickness//2*2), gateWallColor, gateWallSubColor))
            
            # bottom plate
            gateQueue.append((pos.x-2, mc.getHeight(pos.x, pos.z)-1, pos.z-(wallThickness//2+1), pos.x+2, mc.getHeight(pos.x, pos.z)-1, pos.z-gateSize+(wallThickness//2*2), gateFloorColor, gateFloorSubColor))
            
            # front plate
            gateQueue.append((pos.x-3, wallY+1, pos.z-(wallThickness//2), pos.x-3, wallY+2, pos.z-gateSize+(wallThickness//2*2-1), gateWallColor, gateWallSubColor))
            
            # back plate
            gateQueue.append((pos.x+3, wallY+1, pos.z-(wallThickness//2), pos.x+3, wallY+2, pos.z-gateSize+(wallThickness//2*2-1), gateWallColor, gateWallSubColor))
            
            # decoratoive upsidedown stair blocks
            gateQueue.append((pos.x-2, wallY-1, pos.z-(wallThickness//2+2), pos.x+2, wallY-1, pos.z-(wallThickness//2+2), decorativeStairColor, 6))
            gateQueue.append((pos.x-2, wallY-1, pos.z-gateSize+(wallThickness//2*2+1), pos.x+2, wallY-1, pos.z-gateSize+(wallThickness//2*2+1), decorativeStairColor, 7))
            
            # build the fence post gate
            if (state == "open"):
                gateQueue.append((pos.x, wallY, pos.z-(wallThickness//2+1), pos.x, wallY-2, pos.z-gateSize+(wallThickness//2*2), gateColor, gateSubColor))
            elif (state == "closed"):
                gateQueue.append((pos.x, wallY, pos.z-(wallThickness//2+1), pos.x, mc.getHeight(pos.x, pos.z), pos.z-gateSize+(wallThickness//2*2), gateColor, gateSubColor))
            if (heading == 0): # heading north, increment position after drawing
                pos.z -= gateSize
        elif (heading == 90 or heading == 270): # east or west
            if (heading == 90): # heading south, increment position first
                pos.x += gateSize
            # clear the entryway of debris
            gateQueue.append((pos.x-(wallThickness//2+1), wallY-3, pos.z-(wallThickness//2), pos.x-gateSize+(wallThickness//2*2), mc.getHeight(pos.x-gateSize+(wallThickness//2*2), pos.z+(wallThickness//2)), pos.z+(wallThickness//2), block.AIR)) 
            
            # 4 posts
            gateQueue.append((pos.x-(wallThickness//2+1), mc.getHeight(pos.x-(wallThickness//2+1), pos.z-1), pos.z-1, pos.x-(wallThickness//2+1), wallY-1, pos.z-2, gateWallColor, gateWallSubColor))
            gateQueue.append((pos.x-(wallThickness//2+1), mc.getHeight(pos.x-(wallThickness//2+1), pos.z-1), pos.z+1, pos.x-(wallThickness//2+1), wallY-1, pos.z+2, gateWallColor, gateWallSubColor))
            gateQueue.append((pos.x-gateSize+(wallThickness//2*2), mc.getHeight(pos.x-gateSize+(wallThickness//2*2), pos.z-1), pos.z-1, pos.x-gateSize+(wallThickness//2*2), wallY-1, pos.z-2, gateWallColor, gateWallSubColor))
            gateQueue.append((pos.x-gateSize+(wallThickness//2*2), mc.getHeight(pos.x-gateSize+(wallThickness//2*2), pos.z-1), pos.z+1, pos.x-gateSize+(wallThickness//2*2), wallY-1, pos.z+2, gateWallColor, gateWallSubColor))
            
            # torches
            # for j in range(5):
            #     if (j == 2):
            #         continue
            #     gateQueue.append((pos.x-(wallThickness//2)-2, mc.getHeight(pos.x-(wallThickness//2)-2, pos.z-2+j)+2, pos.z-2+j, block.TORCH)) # east of torches
            #     gateQueue.append((pos.x-gateSize+(wallThickness//2*2)+1, mc.getHeight(pos.x-gateSize+(wallThickness//2*2)+1, pos.z-2+j)+2, pos.z-2+j, block.TORCH)) # west row of torches

            # top plate
            gateQueue.append((pos.x-(wallThickness//2+1), wallY, pos.z-2, pos.x-gateSize+(wallThickness//2*2), wallY+3, pos.z+2, gateWallColor, gateWallSubColor))
            
            # bottom plate
            gateQueue.append((pos.x-(wallThickness//2+1), mc.getHeight(pos.x, pos.z)-1, pos.z-2, pos.x-gateSize+(wallThickness//2*2), mc.getHeight(pos.x, pos.z)-1, pos.z+2, gateFloorColor, gateFloorSubColor))
            
            # front plate
            gateQueue.append((pos.x-(wallThickness//2), wallY+1, pos.z-3, pos.x-gateSize+(wallThickness//2*2-1), wallY+2, pos.z-3, gateWallColor, gateWallSubColor))
            
            # back plate
            gateQueue.append((pos.x-(wallThickness//2), wallY+1, pos.z+3, pos.x-gateSize+(wallThickness//2*2-1), wallY+2, pos.z+3, gateWallColor, gateWallSubColor))
            
            # decoratoive upsidedown stair blocks
            gateQueue.append((pos.x-(wallThickness//2+2), wallY-1, pos.z-2, pos.x-(wallThickness//2+2), wallY-1, pos.z+2, decorativeStairColor, 4))
            gateQueue.append((pos.x-gateSize+(wallThickness//2*2+1), wallY-1, pos.z-2, pos.x-gateSize+(wallThickness//2*2+1), wallY-1, pos.z+2, decorativeStairColor, 5))
            
            # build the fence post gate
            if (state == "open"):
                gateQueue.append((pos.x-(wallThickness//2+1), wallY, pos.z, pos.x-gateSize+(wallThickness//2*2), wallY-2, pos.z, gateColor, gateSubColor))
            elif (state == "closed"):
                gateQueue.append((pos.x-(wallThickness//2+1), wallY, pos.z, pos.x-gateSize+(wallThickness//2*2), mc.getHeight(pos.x, pos.z), pos.z, gateColor, gateSubColor))
            if (heading == 270): # heading west, increment position after drawing
                pos.x-= gateSize
                
    elif (step['cmd'] == "jump"):
        if (heading == 0): # north
            pos.z -= argv
        elif (heading == 90): # east
            pos.x += argv
        elif (heading == 180): # south
            pos.z += argv
        elif (heding == 270): # west
            pos.x -= argv
        wallY = mc.getHeight(pos.x, pos.z) + (maxWallHeight + minWallHeight) / 2
        
    elif (step['cmd'] == 'cannon'):
        cannonHeading = 0
        if (argv == "right"):
            cannonHeading = heading + 90
        elif (argv == "left"):
            cannonHeading = heading - 90
        if (cannonHeading == 0):
            y = mc.getHeight(pos.x, pos.z)
            # clear the parapet from the area
            cannonQueue.append((pos.x-(wallThickness//2), wallY+2, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2), wallY+3, pos.z-(wallThickness//2+1), block.AIR))
            
            # wall
            cannonQueue.append((pos.x-(wallThickness//2), wallY, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2), y-5, pos.z-(wallThickness//2+4), wallColor, wallSubColor))
            
            # allure
            cannonQueue.append((pos.x-(wallThickness//2+1), wallY+1, pos.z-(wallThickness//2+2), pos.x+(wallThickness//2+1), wallY+1, pos.z-(wallThickness//2+5), allureColor, allureSubColor))

            # parapet and torches
            cannonQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z-(wallThickness//2+3), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z-(wallThickness//2+5), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z-(wallThickness//2+3), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z-(wallThickness//2+5), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x, wallY+2, pos.z-(wallThickness//2+5), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x-(wallThickness//2+1), wallY+3, pos.z-(wallThickness//2+3), block.TORCH))
            cannonQueue.append((pos.x-(wallThickness//2+1), wallY+3, pos.z-(wallThickness//2+5), block.TORCH))
            cannonQueue.append((pos.x+(wallThickness//2+1), wallY+3, pos.z-(wallThickness//2+3), block.TORCH))
            cannonQueue.append((pos.x+(wallThickness//2+1), wallY+3, pos.z-(wallThickness//2+5), block.TORCH))

            # finally, the cannon!
            cannon(pos.x, wallY+2, pos.z-5, cannonHeading)
        elif (cannonHeading == 90):
            y = mc.getHeight(pos.x, pos.z)
            # clear the parapet from the area
            cannonQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z-(wallThickness//2), pos.x+(wallThickness//2+1), wallY+3, pos.z+(wallThickness//2), block.AIR))
            
            # wall
            cannonQueue.append((pos.x+(wallThickness//2+1), wallY, pos.z-(wallThickness//2), pos.x+(wallThickness//2+4), y-5, pos.z+(wallThickness//2), wallColor, wallSubColor))
            
            # allure
            cannonQueue.append((pos.x+(wallThickness//2+2), wallY+1, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+5), wallY+1, pos.z+(wallThickness//2+1), allureColor, allureSubColor))

            # parapet and torches
            cannonQueue.append((pos.x+(wallThickness//2+3), wallY+2, pos.z-(wallThickness//2+1), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x+(wallThickness//2+5), wallY+2, pos.z-(wallThickness//2+1), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x+(wallThickness//2+3), wallY+2, pos.z+(wallThickness//2+1), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x+(wallThickness//2+5), wallY+2, pos.z+(wallThickness//2+1), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x+(wallThickness//2+5), wallY+2, pos.z, parapetColor, parapetSubColor))
            cannonQueue.append((pos.x+(wallThickness//2+3), wallY+3, pos.z-(wallThickness//2+1), block.TORCH))
            cannonQueue.append((pos.x+(wallThickness//2+5), wallY+3, pos.z-(wallThickness//2+1), block.TORCH))
            cannonQueue.append((pos.x+(wallThickness//2+3), wallY+3, pos.z+(wallThickness//2+1), block.TORCH))
            cannonQueue.append((pos.x+(wallThickness//2+5), wallY+3, pos.z+(wallThickness//2+1), block.TORCH))

            # finally, the cannon!
            cannon(pos.x+5, wallY+2, pos.z, cannonHeading)
        elif (cannonHeading == 180):
            y = mc.getHeight(pos.x, pos.z)
            # clear the parapet from the area
            cannonQueue.append((pos.x-(wallThickness//2), wallY+2, pos.z+(wallThickness//2+1), pos.x+(wallThickness//2), wallY+3, pos.z+(wallThickness//2+1), block.AIR))
            
            # wall
            cannonQueue.append((pos.x-(wallThickness//2), wallY, pos.z+(wallThickness//2+1), pos.x+(wallThickness//2), y-5, pos.z+(wallThickness//2+4), wallColor, wallSubColor))
            
            # allure
            cannonQueue.append((pos.x-(wallThickness//2+1), wallY+1, pos.z+(wallThickness//2+2), pos.x+(wallThickness//2+1), wallY+1, pos.z+(wallThickness//2+5), allureColor, allureSubColor))

            # parapet and torches
            cannonQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z+(wallThickness//2+3), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z+(wallThickness//2+5), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z+(wallThickness//2+3), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x+(wallThickness//2+1), wallY+2, pos.z+(wallThickness//2+5), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x, wallY+2, pos.z+(wallThickness//2+5), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x-(wallThickness//2+1), wallY+3, pos.z+(wallThickness//2+3), block.TORCH))
            cannonQueue.append((pos.x-(wallThickness//2+1), wallY+3, pos.z+(wallThickness//2+5), block.TORCH))
            cannonQueue.append((pos.x+(wallThickness//2+1), wallY+3, pos.z+(wallThickness//2+3), block.TORCH))
            cannonQueue.append((pos.x+(wallThickness//2+1), wallY+3, pos.z+(wallThickness//2+5), block.TORCH))

            # finally, the cannon!
            cannon(pos.x, wallY+2, pos.z+5, cannonHeading)
        elif (cannonHeading == 270):
            y = mc.getHeight(pos.x, pos.z)
            # clear the parapet from the area
            cannonQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z-(wallThickness//2), pos.x-(wallThickness//2+1), wallY+3, pos.z+(wallThickness//2), block.AIR))
            
            # wall
            cannonQueue.append((pos.x-(wallThickness//2+1), wallY, pos.z-(wallThickness//2), pos.x-(wallThickness//2+4), y-5, pos.z+(wallThickness//2), wallColor, wallSubColor))
            
            # allure
            cannonQueue.append((pos.x-(wallThickness//2+2), wallY+1, pos.z-(wallThickness//2+1), pos.x-(wallThickness//2+5), wallY+1, pos.z+(wallThickness//2+1), allureColor, allureSubColor))

            # parapet and torches
            cannonQueue.append((pos.x-(wallThickness//2+3), wallY+2, pos.z-(wallThickness//2+1), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x-(wallThickness//2+5), wallY+2, pos.z-(wallThickness//2+1), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x-(wallThickness//2+3), wallY+2, pos.z+(wallThickness//2+1), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x-(wallThickness//2+5), wallY+2, pos.z+(wallThickness//2+1), parapetColor, parapetSubColor))
            cannonQueue.append((pos.x-(wallThickness//2+5), wallY+2, pos.z, parapetColor, parapetSubColor))
            cannonQueue.append((pos.x-(wallThickness//2+3), wallY+3, pos.z-(wallThickness//2+1), block.TORCH))
            cannonQueue.append((pos.x-(wallThickness//2+5), wallY+3, pos.z-(wallThickness//2+1), block.TORCH))
            cannonQueue.append((pos.x-(wallThickness//2+3), wallY+3, pos.z+(wallThickness//2+1), block.TORCH))
            cannonQueue.append((pos.x-(wallThickness//2+5), wallY+3, pos.z+(wallThickness//2+1), block.TORCH))

            # finally, the cannon!
            cannon(pos.x-5, wallY+2, pos.z, cannonHeading)
    prevCmd = step['cmd']    


print('processing wallQueue')
processSetBlocksQueue(wallQueue)
    
print('processing allureQueue')
processSetBlocksQueue(allureQueue)

print('processing turretQueue')
processSetBlocksQueue(turretQueue)

print('processing turretRoofQueue')
processSetBlocksQueue(turretRoofQueue)

print('processing gateQueue')
processSetBlocksQueue(gateQueue)

print('processing cannonQueue, size:', len(cannonQueue))
processSetBlocksQueue(cannonQueue)
# print('processing debugQueue')
# processSetBlocksQueue(debugQueue)
