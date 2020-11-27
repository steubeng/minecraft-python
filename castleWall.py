# createWall.py

# TODO: add something cylindrical
# TODO: box-top of turret with ladder acesnding to ascend
# TODO: vary height of gate above the wallY
# TODO: parapet continues above gate
# TODO: half blocks above turret doors
# TODO: canons


from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
from mcpi import block
import sys
import json
from collections import deque

def getColorConfig(colorList):
    if (type(colorList) is list):
        colorPrimary = colorList[0]
        if (len(colorList) == 2):
            colorSecondary = colorList[1]
        else:
            colorSecondary = ""
    else:
        colorPrimary = colorList
        colorSecondary = ""
    return colorPrimary, colorSecondary

# read in the data file, configure, and initialize
with open(sys.argv[1]) as f:
  data = json.load(f)
config = data['config']
color = data['color']

# colors (block types)
wallColor, wallSubColor = getColorConfig(color['wallColor'])
allureColor, allureSubColor = getColorConfig(color['allureColor'])
turretColor, turretSubColor = getColorConfig(color['turretColor'])
turretRoofColor, turretRoofSubColor = getColorConfig(color['turretRoofColor'])
turretWindowColor, turretWindowSubColor = getColorConfig(color['turretWindowColor'])
gateColor, gateSubColor = getColorConfig(color['gateColor'])
gateWallColor, gateWallSubColor = getColorConfig(color['gateWallColor'])
gateFloorColor, gateFloorSubColor = getColorConfig(color['gateFloorColor'])
decorativeStairColor = color['decorativeStairColor'] # this will always be a scalar since the "subColor" will be the "direction"
parapetColor, parapetSubColor = getColorConfig(color['parapetColor'])

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
    print('step', i+1, 'of', len(data['path']),', cmd:', step['cmd'], ', argv:', argv,', heading:', heading)
    
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
        turretHeight = argv
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

        # entrance door cutout
        if (prevHeading == 0): # north
            turretQueue.append((pos.x-1, wallY+2, pos.z+(wallThickness//2+2), pos.x+1, wallY+5, pos.z+(wallThickness//2+2), block.AIR))
            turretQueue.append((pos.x-1, wallY+5, pos.z+(wallThickness//2+2), decorativeStairColor, 5))
            turretQueue.append((pos.x+1, wallY+5, pos.z+(wallThickness//2+2), decorativeStairColor, 4))
        elif (prevHeading == 90): # east
            turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z-1, pos.x-(wallThickness//2+2), wallY+5, pos.z+1, block.AIR))
            turretQueue.append((pos.x-(wallThickness//2+2), wallY+5, pos.z-1, decorativeStairColor, 7))
            turretQueue.append((pos.x-(wallThickness//2+2), wallY+5, pos.z+1, decorativeStairColor, 6))
        elif (prevHeading == 180): # south
            turretQueue.append((pos.x-1, wallY+2, pos.z-(wallThickness//2+2), pos.x+1, wallY+5, pos.z-(wallThickness//2+2), block.AIR))
            turretQueue.append((pos.x-1, wallY+5, pos.z-(wallThickness//2+2), decorativeStairColor, 5))
            turretQueue.append((pos.x+1, wallY+5, pos.z-(wallThickness//2+2), decorativeStairColor ,4))
        elif (prevHeading == 270): # west
            turretQueue.append((pos.x+(wallThickness//2+2), wallY+2, pos.z-1, pos.x+(wallThickness//2+2), wallY+5, pos.z+1, block.AIR))
            turretQueue.append((pos.x+(wallThickness//2+2), wallY+5, pos.z-1, decorativeStairColor, 7))
            turretQueue.append((pos.x+(wallThickness//2+2), wallY+5, pos.z+1, decorativeStairColor, 6))

        # exit door cutout
        if (heading == 0): # north
            turretQueue.append((pos.x-1, wallY+2, pos.z-(wallThickness//2+2), pos.x+1, wallY+5, pos.z-(wallThickness//2+2), block.AIR))
            turretQueue.append((pos.x-1, wallY+5, pos.z-(wallThickness//2+2), decorativeStairColor, 5))
            turretQueue.append((pos.x+1, wallY+5, pos.z-(wallThickness//2+2), decorativeStairColor, 4))
        elif (heading == 90): # east
            turretQueue.append((pos.x+(wallThickness//2+2), wallY+2, pos.z-1, pos.x+(wallThickness//2+2), wallY+5, pos.z+1, block.AIR))
            turretQueue.append((pos.x+(wallThickness//2+2), wallY+5, pos.z-1, decorativeStairColor, 7))
            turretQueue.append((pos.x+(wallThickness//2+2), wallY+5, pos.z+1, decorativeStairColor, 6))
        elif (heading == 180): # south
            turretQueue.append((pos.x-1, wallY+2, pos.z+(wallThickness//2+2), pos.x+1, wallY+5, pos.z+(wallThickness//2+2), block.AIR))
            turretQueue.append((pos.x-1, wallY+5, pos.z+(wallThickness//2+2), decorativeStairColor, 5))
            turretQueue.append((pos.x+1, wallY+5, pos.z+(wallThickness//2+2), decorativeStairColor, 4))
        elif (heading == 270): # west
            turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z-1, pos.x-(wallThickness//2+2), wallY+5, pos.z+1, block.AIR))
            turretQueue.append((pos.x-(wallThickness//2+2), wallY+5, pos.z-1, decorativeStairColor, 7))
            turretQueue.append((pos.x-(wallThickness//2+2), wallY+5, pos.z+1, decorativeStairColor, 6))
        
        for j in range(wallThickness + 1, -1, -1):
            turretRoofQueue.append((pos.x-j, wallY+turretHeight+2+2*(wallThickness+1-j), pos.z-j, pos.x+j, wallY+turretHeight+3+2*(wallThickness+1-j), pos.z+j, turretRoofColor, turretRoofSubColor))
            turretRoofQueue.append((pos.x-j, wallY+turretHeight+3+2*(wallThickness+1-j)+1, pos.z-j, block.TORCH))
            turretRoofQueue.append((pos.x+j, wallY+turretHeight+3+2*(wallThickness+1-j)+1, pos.z-j, block.TORCH))
            turretRoofQueue.append((pos.x-j, wallY+turretHeight+3+2*(wallThickness+1-j)+1, pos.z+j, block.TORCH))
            turretRoofQueue.append((pos.x+j, wallY+turretHeight+3+2*(wallThickness+1-j)+1, pos.z+j, block.TORCH))

        
    elif (step['cmd'] == 'gate'):
        if (heading == 0 or heading == 180): # north or south
            if (heading == 180): # heading south, increment position first
                pos.z += argv
            # clear the entryway of debris
            gateQueue.append((pos.x-(wallThickness//2), wallY-3, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2), mc.getHeight(pos.x+(wallThickness//2), pos.z-argv+(wallThickness//2*2)), pos.z-argv+(wallThickness//2*2), block.AIR)) 
            
            # 4 posts
            gateQueue.append((pos.x-1, mc.getHeight(pos.x-1, pos.z-(wallThickness//2+1)), pos.z-(wallThickness//2+1), pos.x-2, wallY-1, pos.z-(wallThickness//2+1), gateWallColor, gateWallSubColor))
            gateQueue.append((pos.x+1, mc.getHeight(pos.x-1, pos.z-(wallThickness//2+1)), pos.z-(wallThickness//2+1), pos.x+2, wallY-1, pos.z-(wallThickness//2+1), gateWallColor, gateWallSubColor))
            gateQueue.append((pos.x-1, mc.getHeight(pos.x-1, pos.z-argv+(wallThickness//2*2)), pos.z-argv+(wallThickness//2*2), pos.x-2, wallY-1, pos.z-argv+(wallThickness//2*2), gateWallColor, gateWallSubColor))
            gateQueue.append((pos.x+1, mc.getHeight(pos.x-1, pos.z-argv+(wallThickness//2*2)), pos.z-argv+(wallThickness//2*2), pos.x+2, wallY-1, pos.z-argv+(wallThickness//2*2), gateWallColor, gateWallSubColor))
            
            # top plate
            gateQueue.append((pos.x-2, wallY, pos.z-(wallThickness//2+1), pos.x+2, wallY+3, pos.z-argv+(wallThickness//2*2), gateWallColor, gateWallSubColor))
            
            # bottom plate
            gateQueue.append((pos.x-2, mc.getHeight(pos.x, pos.z)-1, pos.z-(wallThickness//2+1), pos.x+2, mc.getHeight(pos.x, pos.z)-1, pos.z-argv+(wallThickness//2*2), gateFloorColor, gateFloorSubColor))
            
            # front plate
            gateQueue.append((pos.x-3, wallY+1, pos.z-(wallThickness//2), pos.x-3, wallY+2, pos.z-argv+(wallThickness//2*2-1), gateWallColor, gateWallSubColor))
            
            # back plate
            gateQueue.append((pos.x+3, wallY+1, pos.z-(wallThickness//2), pos.x+3, wallY+2, pos.z-argv+(wallThickness//2*2-1), gateWallColor, gateWallSubColor))
            
            # decoratoive upsidedown stair blocks
            gateQueue.append((pos.x-2, wallY-1, pos.z-(wallThickness//2+2), pos.x+2, wallY-1, pos.z-(wallThickness//2+2), decorativeStairColor, 6))
            gateQueue.append((pos.x-2, wallY-1, pos.z-argv+(wallThickness//2*2+1), pos.x+2, wallY-1, pos.z-argv+(wallThickness//2*2+1), decorativeStairColor, 7))
            
            # build the fence post gate
            gateQueue.append((pos.x, wallY, pos.z-(wallThickness//2+1), pos.x, wallY-2, pos.z-argv+(wallThickness//2*2), gateColor, gateSubColor))
            
            if (heading == 0): # heading north, increment position after drawing
                pos.z -= argv
        elif (heading == 90 or heading == 270): # east or west
            if (heading == 90): # heading south, increment position first
                pos.x += argv
            # clear the entryway of debris
            gateQueue.append((pos.x-(wallThickness//2+1), wallY-3, pos.z-(wallThickness//2), pos.x-argv+(wallThickness//2*2), mc.getHeight(pos.x-argv+(wallThickness//2*2), pos.z+(wallThickness//2)), pos.z+(wallThickness//2), block.AIR)) 
            
            # 4 posts
            gateQueue.append((pos.x-(wallThickness//2+1), mc.getHeight(pos.x-(wallThickness//2+1), pos.z-1), pos.z-1, pos.x-(wallThickness//2+1), wallY-1, pos.z-2, gateWallColor, gateWallSubColor))
            gateQueue.append((pos.x-(wallThickness//2+1), mc.getHeight(pos.x-(wallThickness//2+1), pos.z-1), pos.z+1, pos.x-(wallThickness//2+1), wallY-1, pos.z+2, gateWallColor, gateWallSubColor))
            gateQueue.append((pos.x-argv+(wallThickness//2*2), mc.getHeight(pos.x-argv+(wallThickness//2*2), pos.z-1), pos.z-1, pos.x-argv+(wallThickness//2*2), wallY-1, pos.z-2, gateWallColor, gateWallSubColor))
            gateQueue.append((pos.x-argv+(wallThickness//2*2), mc.getHeight(pos.x-argv+(wallThickness//2*2), pos.z-1), pos.z+1, pos.x-argv+(wallThickness//2*2), wallY-1, pos.z+2, gateWallColor, gateWallSubColor))
            
            # top plate
            gateQueue.append((pos.x-(wallThickness//2+1), wallY, pos.z-2, pos.x-argv+(wallThickness//2*2), wallY+3, pos.z+2, gateWallColor, gateWallSubColor))
            
            # bottom plate
            gateQueue.append((pos.x-(wallThickness//2+1), mc.getHeight(pos.x, pos.z)-1, pos.z-2, pos.x-argv+(wallThickness//2*2), mc.getHeight(pos.x, pos.z)-1, pos.z+2, gateFloorColor, gateFloorSubColor))
            
            # front plate
            gateQueue.append((pos.x-(wallThickness//2), wallY+1, pos.z-3, pos.x-argv+(wallThickness//2*2-1), wallY+2, pos.z-3, gateWallColor, gateWallSubColor))
            
            # back plate
            gateQueue.append((pos.x-(wallThickness//2), wallY+1, pos.z+3, pos.x-argv+(wallThickness//2*2-1), wallY+2, pos.z+3, gateWallColor, gateWallSubColor))
            
            # decoratoive upsidedown stair blocks
            gateQueue.append((pos.x-(wallThickness//2+2), wallY-1, pos.z-2, pos.x-(wallThickness//2+2), wallY-1, pos.z+2, decorativeStairColor, 4))
            gateQueue.append((pos.x-argv+(wallThickness//2*2+1), wallY-1, pos.z-2, pos.x-argv+(wallThickness//2*2+1), wallY-1, pos.z+2, decorativeStairColor, 5))
            
            # build the fence post gate
            gateQueue.append((pos.x-(wallThickness//2+1), wallY, pos.z, pos.x-argv+(wallThickness//2*2), wallY-2, pos.z, gateColor, gateSubColor))
            
            if (heading == 270): # heading west, increment position after drawing
                pos.x-= argv
                
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
        if (argv == 0):
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
            cannon(pos.x, wallY+2, pos.z-5, argv)
        elif (argv == 90):
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
            cannon(pos.x+5, wallY+2, pos.z, argv)
        elif (argv == 180):
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
            cannon(pos.x, wallY+2, pos.z+5, argv)
        elif (argv == 270):
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
            cannon(pos.x-5, wallY+2, pos.z, argv, 1)
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
