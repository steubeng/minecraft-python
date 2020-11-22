# createWall.py
from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
from mcpi import block
import sys
import json
from collections import deque

# read in the data file, configure, and initialize
with open(sys.argv[1]) as f:
  data = json.load(f)
config = data['config']
minWallHeight = config['minWallHeight']
maxWallHeight = config['maxWallHeight']
wallThickness = config['wallThickness']
wallColor = config['wallColor']
allureColor = config['allureColor']
turretColor = config['turretColor']
allure = config['allure']
penDown = config['penDown']
heading = config['initialHeading']
turretHeight = 6
prevHeading = heading
lastSetBlocksWallColumnBottom = {}
lastSetBlocksWallColumnTop = {}
wallQueue = deque([])
allureQueue = deque([])
debugQueue = deque([])
turretQueue = deque([])

# mcpi setup and initialization
mc = Minecraft.create()
mc.postToChat("Castle Wall!")
pos = mc.player.getPos()
wallY = mc.getHeight(pos.x, pos.z) + (maxWallHeight + minWallHeight) / 2
print('wallHeight:', (maxWallHeight - minWallHeight) / 2)
print('wallY: ', wallY)

print('processing path (', len(data['path']), 'steps )')
for i in range(len(data['path'])):
    step = data['path'][i]
    argv = step['argv']
    print('step', i+1, 'of', len(data['path']),', cmd:', step['cmd'], ', argv:', argv)
    
    ### pen
    if (step['cmd'] == 'pen'):
        if (argv == 'up'):
            penDown = False
        else:
            penDown = True
        
    ### move
    elif (step['cmd'] == 'move'):
        if (heading == 0): # north
            for z in range(argv):
                if (penDown):                    
                    if (z == 0):
                        wallQueue.append((pos.x-(wallThickness//2), mc.getHeight(pos.x, pos.z), pos.z, pos.x+(wallThickness//2), wallY, pos.z+(wallThickness//2), wallColor))
                    elif (z == argv - 1):
                        wallQueue.append((pos.x-(wallThickness//2), mc.getHeight(pos.x, pos.z), pos.z, pos.x+(wallThickness//2), wallY, pos.z-(wallThickness//2), wallColor))
                    else:
                        wallQueue.append((pos.x-(wallThickness//2), min(wallY, mc.getHeight(pos.x, pos.z)), pos.z, pos.x+(wallThickness//2), wallY, pos.z, wallColor))
                if (z < argv - 1):
                    if (allure):
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+1, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+1, pos.z+(wallThickness//2+1), allureColor))
                    pos.z -= 1
                if (z == argv - 1):
                    if (allure):
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+1, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+1, pos.z+(wallThickness//2+1), allureColor))
                if ((z < argv - (wallThickness//2)) and (z > (wallThickness//2))):
                    if (wallY - mc.getHeight(pos.x, pos.z) < minWallHeight):
                        wallY += 1
                    elif (wallY - mc.getHeight(pos.x, pos.z) > maxWallHeight):
                        wallY -= 1
        elif (heading == 90): # east
            for x in range(argv):
                if (penDown):
                    if (x == 0):
                        wallQueue.append((pos.x, mc.getHeight(pos.x, pos.z), pos.z-(wallThickness//2), pos.x-(wallThickness//2), wallY, pos.z+(wallThickness//2), wallColor))
                    elif (x == argv - 1):
                        wallQueue.append((pos.x, mc.getHeight(pos.x, pos.z), pos.z-(wallThickness//2), pos.x+(wallThickness//2), wallY, pos.z+(wallThickness//2), wallColor))
                    else:
                        wallQueue.append((pos.x, min(wallY, mc.getHeight(pos.x, pos.z)), pos.z-(wallThickness//2), pos.x, wallY, pos.z+(wallThickness//2), wallColor))
                if (x < argv - 1):
                    if (allure):
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+1, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+1, pos.z+(wallThickness//2+1), allureColor))
                    pos.x += 1
                elif (x == argv - 1):
                    if (allure):
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+1, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+1, pos.z+(wallThickness//2+1), allureColor))
                if ((x < argv - (wallThickness//2)) and (x > (wallThickness//2))):
                    if (wallY - mc.getHeight(pos.x, pos.z) < minWallHeight):
                        wallY += 1
                    elif (wallY - mc.getHeight(pos.x, pos.z) > maxWallHeight):
                        wallY -= 1
                # print('pos.x went from', pos.x-1, 'to', pos.x)
        elif (heading == 180): # south
            for z in range(argv):
                if (penDown):
                    if (z == 0):
                        wallQueue.append((pos.x-(wallThickness//2), mc.getHeight(pos.x, pos.z), pos.z, pos.x+(wallThickness//2), wallY, pos.z-(wallThickness//2), wallColor))
                    elif (z == argv - 1):
                        wallQueue.append((pos.x-(wallThickness//2), mc.getHeight(pos.x, pos.z), pos.z, pos.x+(wallThickness//2), wallY, pos.z+(wallThickness//2), wallColor))
                    else:
                        wallQueue.append((pos.x-(wallThickness//2), min(wallY, mc.getHeight(pos.x, pos.z)), pos.z, pos.x+(wallThickness//2), wallY, pos.z, wallColor))
                if (z < argv - 1):
                    if (allure):
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+1, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+1, pos.z+(wallThickness//2+1), allureColor))
                    pos.z += 1
                if (z == argv - 1):
                    if (allure):
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+1, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+1, pos.z+(wallThickness//2+1), allureColor))
                if ((z < argv - (wallThickness//2)) and (z > (wallThickness//2))):
                    if (wallY - mc.getHeight(pos.x, pos.z) < minWallHeight):
                        wallY += 1
                    elif (wallY - mc.getHeight(pos.x, pos.z) > maxWallHeight):
                        wallY -= 1
        elif (heading == 270): # west
            for x in range(argv):
                if (penDown):                    
                    if (x == 0):
                        wallQueue.append((pos.x, mc.getHeight(pos.x, pos.z), pos.z-(wallThickness//2), pos.x+(wallThickness//2), wallY, pos.z+(wallThickness//2), wallColor))
                    elif (x == argv - 1):
                        wallQueue.append((pos.x, mc.getHeight(pos.x, pos.z), pos.z-(wallThickness//2), pos.x-(wallThickness//2), wallY, pos.z+(wallThickness//2), wallColor))
                    else:
                        wallQueue.append((pos.x, min(wallY, mc.getHeight(pos.x, pos.z)), pos.z-(wallThickness//2), pos.x, wallY, pos.z+(wallThickness//2), wallColor))
                if (x < argv - 1):
                    if (allure):
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+1, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+1, pos.z+(wallThickness//2+1), allureColor))
                    pos.x -= 1
                if (x == argv - 1):
                    if (allure):
                        allureQueue.append((pos.x-(wallThickness//2+1), wallY+1, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+1, pos.z+(wallThickness//2+1), allureColor))
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
        
    ### color
    elif (step['cmd'] == 'color'):
        color = argv
        
    elif (step['cmd'] == 'turret'):
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z-(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY+2+turretHeight, pos.z-(wallThickness//2+2), turretColor))
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z+(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY+2+turretHeight, pos.z+(wallThickness//2+2), turretColor))
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z-(wallThickness//2+2), pos.x-(wallThickness//2+2), wallY+2+turretHeight, pos.z+(wallThickness//2+2), turretColor))
        turretQueue.append((pos.x+(wallThickness//2+2), wallY+2, pos.z-(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY+2+turretHeight, pos.z+(wallThickness//2+2), turretColor))
        
        turretQueue.append((pos.x+(wallThickness//2+2), wallY+1, pos.z-(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY, pos.z-(wallThickness//2+2), turretColor))
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+1, pos.z-(wallThickness//2+2), pos.x-(wallThickness//2+2), wallY, pos.z-(wallThickness//2+2), turretColor))
        turretQueue.append((pos.x+(wallThickness//2+2), wallY+1, pos.z+(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY, pos.z+(wallThickness//2+2), turretColor))
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+1, pos.z+(wallThickness//2+2), pos.x-(wallThickness//2+2), wallY, pos.z+(wallThickness//2+2), turretColor))

        if (prevHeading == 0): # north
            turretQueue.append((pos.x, wallY+2, pos.z+(wallThickness//2+2), pos.x, wallY+3, pos.z+(wallThickness//2+2), block.AIR))
        elif (prevHeading == 90): # east
            turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z, pos.x-(wallThickness//2+2), wallY+3, pos.z, block.AIR))
        elif (prevHeading == 180): # south
            turretQueue.append((pos.x, wallY+2, pos.z-(wallThickness//2+2), pos.x, wallY+3, pos.z-(wallThickness//2+2), block.AIR))
        elif (prevHeading == 270): # west
            turretQueue.append((pos.x+(wallThickness//2+2), wallY+2, pos.z, pos.x+(wallThickness//2+2), wallY+3, pos.z, block.AIR))

        if (heading == 0): # north
            turretQueue.append((pos.x, wallY+2, pos.z-(wallThickness//2+2), pos.x, wallY+3, pos.z-(wallThickness//2+2), block.AIR))
        elif (heading == 90): # east
            turretQueue.append((pos.x+(wallThickness//2+2), wallY+2, pos.z, pos.x+(wallThickness//2+2), wallY+3, pos.z, block.AIR))
        elif (heading == 180): # south
            turretQueue.append((pos.x, wallY+2, pos.z+(wallThickness//2+2), pos.x, wallY+3, pos.z+(wallThickness//2+2), block.AIR))
        elif (heading == 270): # west
            turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z, pos.x-(wallThickness//2+2), wallY+3, pos.z, block.AIR))


print('processing wallQueue')
for i in range(len(wallQueue)):
    tuple = wallQueue.popleft()
    mc.setBlocks(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], tuple[6])
    
print('processing allureQueue')
for i in range(len(allureQueue)):
    tuple = allureQueue.popleft()
    mc.setBlocks(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], tuple[6])

print('processing turretQueue')
for i in range(len(turretQueue)):
    tuple = turretQueue.popleft()
    mc.setBlocks(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], tuple[6])

print('processing debugQueue')
for i in range(len(debugQueue)):
    tuple = debugQueue.popleft()
    # mc.setBlocks(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], tuple[6])
