# createWall.py
from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
import sys
import json


with open(sys.argv[1]) as f:
  data = json.load(f)
config = data['config']
minWallHeight = config['minWallHeight']
maxWallHeight = config['maxWallHeight']
wallHeight = minWallHeight
if (config['penDown'] == 'True'):
    penDown =  True
else:
    penDown = False;
heading = config['initialHeading']
print('heading:', heading)
mc = Minecraft.create()
mc.postToChat("Castle Wall!")
pos = mc.player.getPos()
wallY = mc.getHeight(pos.x, pos.z) + (maxWallHeight - minWallHeight) / 2

for i in range(len(data['path'])):
    print('path', i)
    step = data['path'][i]
    argv = step['argv']
    print('\tcmd:', step['cmd'], '\n\targv:', argv)
    
    ### pen
    if (step['cmd'] == 'pen'):
        if (argv == 'up'):
            penDown = False
        else:
            penDown = True
        print('\tpenDown is', penDown)
        
    ### move
    elif (step['cmd'] == 'move'):
        print('\tmoving at heading', heading, 'by', argv, 'blocks')
        if (heading == 0): # north
            for z in range(argv):
                if (penDown):
                    mc.setBlocks(pos.x, mc.getHeight(pos.x, pos.z), pos.z, pos.x, wallY, pos.z, 42)
                pos.z -= 1
        elif (heading == 90): # east
            for x in range(argv):
                if (penDown):
                    mc.setBlocks(pos.x, mc.getHeight(pos.x, pos.z), pos.z, pos.x, wallY, pos.z, 42)
                pos.x += 1
        elif (heading == 180): # south
            for z in range(argv):
                if (penDown):
                    mc.setBlocks(pos.x, mc.getHeight(pos.x, pos.z), pos.z, pos.x, wallY, pos.z, 42)
                pos.z += 1
        elif (heading == 270): # west
            for x in range(argv):
                if (penDown):
                    mc.setBlocks(pos.x, mc.getHeight(pos.x, pos.z), pos.z, pos.x, wallY, pos.z, 42)
                pos.x -= 1
        if (wallY - mc.getHeight(pos.x, pos.z) < minWallHeight):
            wallY += 1
        elif (wallY - mc.getHeight(pos.x, pos.z) > maxWallHeight):
            wallY -= 1

    ### turn left
    elif (step['cmd'] == 'left'):
        print('\tturning lefyt by', argv, 'degrees')
        heading = (heading - argv + 360) % 360

    ### turn right
    elif (step['cmd'] == 'right'):
        print('\tturning right by', argv, 'degrees')
        heading = (heading + argv) % 360


