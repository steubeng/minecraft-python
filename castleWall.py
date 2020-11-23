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
turretRoofColor = config['turretRoofColor']
turretWindowColor = config['turretWindowColor']
gateColor = config['gateColor']
gateWallColor = config['gateWallColor']
gateFloorColor = config['gateFloorColor']
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
turretRoofQueue = deque([])
gateQueue = deque([])

# mcpi setup and initialization
mc = Minecraft.create()
mc.postToChat("Castle Wall!")
pos = mc.player.getPos()
wallY = mc.getHeight(pos.x, pos.z) + (maxWallHeight + minWallHeight) / 2


def processSetBlocksQueue(queue):
    for i in range(len(queue)):
        tuple = queue.popleft()
        if (len(tuple) >= 7):
            mc.setBlocks(tuple[0], tuple[1], tuple[2], tuple[3], tuple[4], tuple[5], tuple[6])
    

print('processing path (', len(data['path']), 'steps )')
for i in range(len(data['path'])):
    step = data['path'][i]
    argv = step['argv']
    print('step', i+1, 'of', len(data['path']),', cmd:', step['cmd'], ', argv:', argv,', heading:', heading)
    
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
        # clear the ground
        turretQueue.append((pos.x-(wallThickness//2+1), wallY+2, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+2, pos.z+(wallThickness//2+1), block.AIR))
    
    
        # main walls
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z-(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY+2+turretHeight, pos.z-(wallThickness//2+2), turretColor))
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z+(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY+2+turretHeight, pos.z+(wallThickness//2+2), turretColor))
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z-(wallThickness//2+2), pos.x-(wallThickness//2+2), wallY+2+turretHeight, pos.z+(wallThickness//2+2), turretColor))
        turretQueue.append((pos.x+(wallThickness//2+2), wallY+2, pos.z-(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY+2+turretHeight, pos.z+(wallThickness//2+2), turretColor))
        
        # outer decorative down hangers
        turretQueue.append((pos.x+(wallThickness//2+2), wallY+1, pos.z-(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY, pos.z-(wallThickness//2+2), turretColor))
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+1, pos.z-(wallThickness//2+2), pos.x-(wallThickness//2+2), wallY, pos.z-(wallThickness//2+2), turretColor))
        turretQueue.append((pos.x+(wallThickness//2+2), wallY+1, pos.z+(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY, pos.z+(wallThickness//2+2), turretColor))
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+1, pos.z+(wallThickness//2+2), pos.x-(wallThickness//2+2), wallY, pos.z+(wallThickness//2+2), turretColor))

        # inner decorative down hangers
        turretQueue.append((pos.x+(wallThickness//2+1), wallY, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY-2, pos.z-(wallThickness//2+1), turretColor))
        turretQueue.append((pos.x-(wallThickness//2+1), wallY, pos.z-(wallThickness//2+1), pos.x-(wallThickness//2+1), wallY-2, pos.z-(wallThickness//2+1), turretColor))
        turretQueue.append((pos.x+(wallThickness//2+1), wallY, pos.z+(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY-2, pos.z+(wallThickness//2+1), turretColor))
        turretQueue.append((pos.x-(wallThickness//2+1), wallY, pos.z+(wallThickness//2+1), pos.x-(wallThickness//2+1), wallY-2, pos.z+(wallThickness//2+1), turretColor))

        # cut out windows on all sides, the door ways will cut the opening larger in certain areas
        turretQueue.append((pos.x-1, wallY+3, pos.z-(wallThickness//2+2), pos.x+1, wallY+4, pos.z-(wallThickness//2+2), turretWindowColor))
        turretQueue.append((pos.x-1, wallY+3, pos.z+(wallThickness//2+2), pos.x+1, wallY+4, pos.z+(wallThickness//2+2), turretWindowColor))
        turretQueue.append((pos.x+(wallThickness//2+2), wallY+3, pos.z-1, pos.x+(wallThickness//2+2), wallY+4, pos.z+1, turretWindowColor))
        turretQueue.append((pos.x-(wallThickness//2+2), wallY+3, pos.z-1, pos.x-(wallThickness//2+2), wallY+4, pos.z+1, turretWindowColor))
        

        # entrance door cutout
        if (prevHeading == 0): # north
            turretQueue.append((pos.x-1, wallY+2, pos.z+(wallThickness//2+2), pos.x+1, wallY+4, pos.z+(wallThickness//2+2), block.AIR))
        elif (prevHeading == 90): # east
            turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z-1, pos.x-(wallThickness//2+2), wallY+4, pos.z+1, block.AIR))
        elif (prevHeading == 180): # south
            turretQueue.append((pos.x-1, wallY+2, pos.z-(wallThickness//2+2), pos.x+1, wallY+4, pos.z-(wallThickness//2+2), block.AIR))
        elif (prevHeading == 270): # west
            turretQueue.append((pos.x+(wallThickness//2+2), wallY+2, pos.z-1, pos.x+(wallThickness//2+2), wallY+4, pos.z+1, block.AIR))

        # exit door cutout
        if (heading == 0): # north
            turretQueue.append((pos.x-1, wallY+2, pos.z-(wallThickness//2+2), pos.x+1, wallY+4, pos.z-(wallThickness//2+2), block.AIR))
        elif (heading == 90): # east
            turretQueue.append((pos.x+(wallThickness//2+2), wallY+2, pos.z-1, pos.x+(wallThickness//2+2), wallY+4, pos.z+1, block.AIR))
        elif (heading == 180): # south
            turretQueue.append((pos.x-1, wallY+2, pos.z+(wallThickness//2+2), pos.x+1, wallY+4, pos.z+(wallThickness//2+2), block.AIR))
        elif (heading == 270): # west
            turretQueue.append((pos.x-(wallThickness//2+2), wallY+2, pos.z-1, pos.x-(wallThickness//2+2), wallY+4, pos.z+1, block.AIR))
            
        #turret roof (north)
        turretRoofQueue.append((pos.x-(wallThickness//2+3), wallY+turretHeight+2, pos.z-(wallThickness//2+3), pos.x+(wallThickness//2+3), wallY+turretHeight+2, pos.z-(wallThickness//2+3), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+3), wallY+turretHeight+3, pos.z-(wallThickness//2+3), pos.x+(wallThickness//2+3), wallY+turretHeight+3, pos.z-(wallThickness//2+3), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+2), wallY+turretHeight+4, pos.z-(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY+turretHeight+4, pos.z-(wallThickness//2+2), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+2), wallY+turretHeight+5, pos.z-(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY+turretHeight+5, pos.z-(wallThickness//2+2), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+1), wallY+turretHeight+6, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+turretHeight+6, pos.z-(wallThickness//2+1), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+1), wallY+turretHeight+7, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+turretHeight+7, pos.z-(wallThickness//2+1), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+0), wallY+turretHeight+8, pos.z-(wallThickness//2+0), pos.x+(wallThickness//2+0), wallY+turretHeight+8, pos.z-(wallThickness//2+0), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+0), wallY+turretHeight+9, pos.z-(wallThickness//2+0), pos.x+(wallThickness//2+0), wallY+turretHeight+9, pos.z-(wallThickness//2+0), turretRoofColor))
        
        #turret roof (east)
        turretRoofQueue.append((pos.x+(wallThickness//2+3), wallY+turretHeight+2, pos.z-(wallThickness//2+3), pos.x+(wallThickness//2+3), wallY+turretHeight+2, pos.z+(wallThickness//2+3), turretRoofColor))
        turretRoofQueue.append((pos.x+(wallThickness//2+3), wallY+turretHeight+3, pos.z-(wallThickness//2+3), pos.x+(wallThickness//2+3), wallY+turretHeight+3, pos.z+(wallThickness//2+3), turretRoofColor))
        turretRoofQueue.append((pos.x+(wallThickness//2+2), wallY+turretHeight+4, pos.z-(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY+turretHeight+4, pos.z+(wallThickness//2+2), turretRoofColor))
        turretRoofQueue.append((pos.x+(wallThickness//2+2), wallY+turretHeight+5, pos.z-(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY+turretHeight+5, pos.z+(wallThickness//2+2), turretRoofColor))
        turretRoofQueue.append((pos.x+(wallThickness//2+1), wallY+turretHeight+6, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+turretHeight+6, pos.z+(wallThickness//2+1), turretRoofColor))
        turretRoofQueue.append((pos.x+(wallThickness//2+1), wallY+turretHeight+7, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+turretHeight+7, pos.z+(wallThickness//2+1), turretRoofColor))
        turretRoofQueue.append((pos.x+(wallThickness//2+0), wallY+turretHeight+8, pos.z-(wallThickness//2+0), pos.x+(wallThickness//2+0), wallY+turretHeight+8, pos.z+(wallThickness//2+0), turretRoofColor))
        turretRoofQueue.append((pos.x+(wallThickness//2+0), wallY+turretHeight+9, pos.z-(wallThickness//2+0), pos.x+(wallThickness//2+0), wallY+turretHeight+9, pos.z+(wallThickness//2+0), turretRoofColor))

        #turret roof (south)
        turretRoofQueue.append((pos.x-(wallThickness//2+3), wallY+turretHeight+2, pos.z+(wallThickness//2+3), pos.x+(wallThickness//2+3), wallY+turretHeight+2, pos.z+(wallThickness//2+3), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+3), wallY+turretHeight+3, pos.z+(wallThickness//2+3), pos.x+(wallThickness//2+3), wallY+turretHeight+3, pos.z+(wallThickness//2+3), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+2), wallY+turretHeight+4, pos.z+(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY+turretHeight+4, pos.z+(wallThickness//2+2), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+2), wallY+turretHeight+5, pos.z+(wallThickness//2+2), pos.x+(wallThickness//2+2), wallY+turretHeight+5, pos.z+(wallThickness//2+2), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+1), wallY+turretHeight+6, pos.z+(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+turretHeight+6, pos.z+(wallThickness//2+1), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+1), wallY+turretHeight+7, pos.z+(wallThickness//2+1), pos.x+(wallThickness//2+1), wallY+turretHeight+7, pos.z+(wallThickness//2+1), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+0), wallY+turretHeight+8, pos.z+(wallThickness//2+0), pos.x+(wallThickness//2+0), wallY+turretHeight+8, pos.z+(wallThickness//2+0), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+0), wallY+turretHeight+9, pos.z+(wallThickness//2+0), pos.x+(wallThickness//2+0), wallY+turretHeight+9, pos.z+(wallThickness//2+0), turretRoofColor))
        
        #turret roof (west)
        turretRoofQueue.append((pos.x-(wallThickness//2+3), wallY+turretHeight+2, pos.z-(wallThickness//2+3), pos.x-(wallThickness//2+3), wallY+turretHeight+2, pos.z+(wallThickness//2+3), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+3), wallY+turretHeight+3, pos.z-(wallThickness//2+3), pos.x-(wallThickness//2+3), wallY+turretHeight+3, pos.z+(wallThickness//2+3), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+2), wallY+turretHeight+4, pos.z-(wallThickness//2+2), pos.x-(wallThickness//2+2), wallY+turretHeight+4, pos.z+(wallThickness//2+2), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+2), wallY+turretHeight+5, pos.z-(wallThickness//2+2), pos.x-(wallThickness//2+2), wallY+turretHeight+5, pos.z+(wallThickness//2+2), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+1), wallY+turretHeight+6, pos.z-(wallThickness//2+1), pos.x-(wallThickness//2+1), wallY+turretHeight+6, pos.z+(wallThickness//2+1), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+1), wallY+turretHeight+7, pos.z-(wallThickness//2+1), pos.x-(wallThickness//2+1), wallY+turretHeight+7, pos.z+(wallThickness//2+1), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+0), wallY+turretHeight+8, pos.z-(wallThickness//2+0), pos.x-(wallThickness//2+0), wallY+turretHeight+8, pos.z+(wallThickness//2+0), turretRoofColor))
        turretRoofQueue.append((pos.x-(wallThickness//2+0), wallY+turretHeight+9, pos.z-(wallThickness//2+0), pos.x-(wallThickness//2+0), wallY+turretHeight+9, pos.z+(wallThickness//2+0), turretRoofColor))

        #turret roof (top spire)
        turretRoofQueue.append((pos.x-(wallThickness//2-1), wallY+turretHeight+10, pos.z, pos.x+(wallThickness//2-1), wallY+turretHeight+15, pos.z, turretRoofColor))

    elif (step['cmd'] == 'gate'):
        if (heading == 0 or heading == 180): # north or south
            if (heading == 180): # heading south, increment position first
                pos.z += argv
            # clear the entryway of debris
            gateQueue.append((pos.x-(wallThickness//2), wallY-3, pos.z-(wallThickness//2+1), pos.x+(wallThickness//2), mc.getHeight(pos.x+(wallThickness//2), pos.z-argv+(wallThickness//2*2)), pos.z-argv+(wallThickness//2*2), block.AIR)) 
            
            # 4 posts
            gateQueue.append((pos.x-1, mc.getHeight(pos.x-1, pos.z-(wallThickness//2+1)), pos.z-(wallThickness//2+1), pos.x-2, wallY-1, pos.z-(wallThickness//2+1), gateWallColor))
            gateQueue.append((pos.x+1, mc.getHeight(pos.x-1, pos.z-(wallThickness//2+1)), pos.z-(wallThickness//2+1), pos.x+2, wallY-1, pos.z-(wallThickness//2+1), gateWallColor))
            gateQueue.append((pos.x-1, mc.getHeight(pos.x-1, pos.z-argv+(wallThickness//2*2)), pos.z-argv+(wallThickness//2*2), pos.x-2, wallY-1, pos.z-argv+(wallThickness//2*2), gateWallColor))
            gateQueue.append((pos.x+1, mc.getHeight(pos.x-1, pos.z-argv+(wallThickness//2*2)), pos.z-argv+(wallThickness//2*2), pos.x+2, wallY-1, pos.z-argv+(wallThickness//2*2), gateWallColor))
            
            # top plate
            gateQueue.append((pos.x-2, wallY, pos.z-(wallThickness//2+1), pos.x+2, wallY+2, pos.z-argv+(wallThickness//2*2), gateWallColor))
            
            # build the fence post gate
            gateQueue.append((pos.x, wallY, pos.z-(wallThickness//2+1), pos.x, wallY-2, pos.z-argv+(wallThickness//2*2), gateColor))
            
            # front plate
            gateQueue.append((pos.x-3, wallY+1, pos.z-(wallThickness//2), pos.x-3, wallY+1, pos.z-argv+(wallThickness//2*2-1), gateWallColor))
            
            # back plate
            gateQueue.append((pos.x+3, wallY+1, pos.z-(wallThickness//2), pos.x+3, wallY+1, pos.z-argv+(wallThickness//2*2-1), gateWallColor))
            
            # bottom plate
            gateQueue.append((pos.x-2, mc.getHeight(pos.x, pos.z)-1, pos.z-(wallThickness//2+1), pos.x+2, mc.getHeight(pos.x, pos.z)-1, pos.z-argv+(wallThickness//2*2), gateFloorColor))
            
            if (heading == 0): # heading north, increment position after drawing
                pos.z -= argv
        elif (heading == 90): # east
            gateQueue.append(())
        elif (heading == 270): # west
            gateQueue.append(())
        

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

print('processing debugQueue')
processSetBlocksQueue(debugQueue)
