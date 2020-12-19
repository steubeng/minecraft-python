from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
import random
from utils import getGroundHeight, circle

def house1(mc, pos):
    floorColorList = [5, 5, 5, 5, 5, 5]
    floorSubColorList = [0, 1, 2, 3, 4, 5]
    wallColorList = [98, 4, 1, 1, 24, 24]
    wallSubColorList = [0, 0, 2, 0, 1, 0]
    windowColorList = [160, 160, 160, 160, 160, 160]
    windowSubColorList = [0, 1, 2, 3, 4, 5]
    roofColorList = [5, 159, 159, 159, 159, 159]
    roofSubColorList = [1, 0, 1, 2, 3, 4]
    doorColorList = [193, 194, 195, 196, 197]
    stiltColorList = [17, 17, 17, 17, 162, 162]
    stiltSubColorList = [0, 1, 2, 3, 0, 1]
    
    floorColor = floorColorList[random.randrange(len(floorColorList))]
    floorSubColor = floorSubColorList[random.randrange(len(floorSubColorList))]
    wallColor = wallColorList[random.randrange(len(wallColorList))]
    wallSubColor = wallSubColorList[random.randrange(len(wallSubColorList))]
    windowColor = windowColorList[random.randrange(len(windowColorList))]
    windowSubColor = windowSubColorList[random.randrange(len(windowSubColorList))]
    roofColor = roofColorList[random.randrange(len(roofColorList))]
    roofSubColor = roofSubColorList[random.randrange(len(roofSubColorList))]
    doorColor = doorColorList[random.randrange(len(doorColorList))]
    stiltColor = stiltColorList[random.randrange(len(stiltColorList))]
    stiltSubColor = stiltSubColorList[random.randrange(len(stiltSubColorList))] 
    
    yMin = 256
    needStilts = False
    y, stilts = getGroundHeight(mc, pos.x-4, pos.z-4)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y
    y, stilts = getGroundHeight(mc, pos.x-4, pos.z+3)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y
    y, stilts = getGroundHeight(mc, pos.x+3, pos.z-4)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y
    y, stilts = getGroundHeight(mc, pos.x+3, pos.z+3)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y
    if (needStilts):
        pos.y = stiltsY
    else:
        pos.y = yMin
    mc.setBlocks(pos.x-4, pos.y, pos.z-4, pos.x+3, pos.y+10, pos.z+3, 0)
    
    # stilts
    if (needStilts):
        mc.setBlocks(pos.x-3, pos.y, pos.z-3, pos.x-3, pos.y-20, pos.z-3, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x+2, pos.y, pos.z-3, pos.x+2, pos.y-20, pos.z-3, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x-3, pos.y, pos.z+2, pos.x-3, pos.y-20, pos.z+2, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x+2, pos.y, pos.z+2, pos.x+2, pos.y-20, pos.z+2, stiltColor, stiltSubColor)
        pos.y += 1
        
    # wood floor
    mc.setBlocks(pos.x-3, pos.y-1, pos.z-3, pos.x+2, pos.y-1, pos.z+2, floorColor, floorSubColor)
        
    # stone brick walls
    # north wall
    mc.setBlocks(pos.x-3, pos.y, pos.z-3, pos.x-2, pos.y+3, pos.z-3, wallColor, wallSubColor)
    mc.setBlocks(pos.x+1, pos.y, pos.z-3, pos.x+2, pos.y+3, pos.z-3, wallColor, wallSubColor)
    mc.setBlocks(pos.x-1, pos.y+2, pos.z-3, pos.x, pos.y+3, pos.z-3, wallColor, wallSubColor)
    # south wall
    mc.setBlocks(pos.x-3, pos.y, pos.z+2, pos.x+2, pos.y+3, pos.z+2, wallColor, wallSubColor)
    mc.setBlocks(pos.x-1, pos.y+1, pos.z+2, pos.x, pos.y+2, pos.z+2, windowColor, windowSubColor)
    # east wall
    mc.setBlocks(pos.x+2, pos.y, pos.z-2, pos.x+2, pos.y+3, pos.z+1, wallColor, wallSubColor)
    mc.setBlocks(pos.x+2, pos.y+1, pos.z, pos.x+2, pos.y+2, pos.z-1, windowColor, windowSubColor)
    # west wall
    mc.setBlocks(pos.x-3, pos.y, pos.z-2, pos.x-3, pos.y+3, pos.z+1, wallColor, wallSubColor)
    mc.setBlocks(pos.x-3, pos.y+1, pos.z, pos.x-3, pos.y+2, pos.z-1, windowColor, windowSubColor)
    
    # roof
    mc.setBlocks(pos.x-2, pos.y+4, pos.z-2, pos.x+1, pos.y+4, pos.z+1, roofColor, roofSubColor)
    
    # torches
    mc.setBlock(pos.x-3, pos.y+4, pos.z-2, 50)
    mc.setBlock(pos.x-3, pos.y+4, pos.z+1, 50)
    mc.setBlock(pos.x+2, pos.y+4, pos.z-2, 50)
    mc.setBlock(pos.x+2, pos.y+4, pos.z+1, 50)

    mc.setBlock(pos.x-2, pos.y, pos.z-2, 50)
    mc.setBlock(pos.x-2, pos.y, pos.z+1, 50)
    mc.setBlock(pos.x+1, pos.y, pos.z-2, 50)
    mc.setBlock(pos.x+1, pos.y, pos.z+1, 50)
    
    # right door
    mc.setBlock(pos.x-1, pos.y, pos.z-3, doorColor, 4)
    mc.setBlock(pos.x-1, pos.y+1, pos.z-3, doorColor, 8)
    # left door
    mc.setBlock(pos.x, pos.y, pos.z-3, doorColor, 1)
    mc.setBlock(pos.x, pos.y+1, pos.z-3, doorColor, 8)
    
def house2(mc, pos):
    floorColorList = [1, 1, 1, 1, 1, 1]
    floorSubColorList = [0, 1, 2, 3, 4, 5]
    wallColorList = [1, 1, 1, 1, 1, 1]
    wallSubColorList = [0, 1, 2, 3, 4, 5]
    windowColorList = [160, 160, 160, 160, 160, 160]
    windowSubColorList = [0, 1, 2, 3, 4, 5]
    roofColorList = [17, 17, 17, 17]
    roofSubColorList = [0, 1, 2, 3]
    postColorList = [162, 162, 17, 17, 17, 17]
    postSubColorList = [0, 1, 0, 1, 2, 3]    
    doorColorList = [193, 194, 195, 196, 197]
    stairColorList = [53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 163, 164, 180]
    fenceColorList = [139, 139]
    fenceSubColorList = [0, 1]
    awningColorList = [182, 44, 44, 44, 44, 44, 44, 44, 44]
    awningSubColorList = [0, 0, 1, 2, 3, 4, 5, 6, 7]
    stiltColorList = [17, 17, 17, 17, 162, 162]
    stiltSubColorList = [0, 1, 2, 3, 0, 1]
    
    floorColor = floorColorList[random.randrange(len(floorColorList))]
    floorSubColor = floorSubColorList[random.randrange(len(floorSubColorList))]
    wallColor = wallColorList[random.randrange(len(wallColorList))]
    wallSubColor = wallSubColorList[random.randrange(len(wallSubColorList))]
    windowColor = windowColorList[random.randrange(len(windowColorList))]
    windowSubColor = windowSubColorList[random.randrange(len(windowSubColorList))]
    roofColor = roofColorList[random.randrange(len(roofColorList))]
    roofSubColor = roofSubColorList[random.randrange(len(roofSubColorList))]
    postColor = roofColorList[random.randrange(len(roofColorList))]
    postSubColor = roofSubColorList[random.randrange(len(roofSubColorList))]
    doorColor = doorColorList[random.randrange(len(doorColorList))]
    stairColor = stairColorList[random.randrange(len(stairColorList))]
    fenceColor = fenceColorList[random.randrange(len(fenceColorList))]
    fenceSubColor = fenceSubColorList[random.randrange(len(fenceSubColorList))]
    awningColor = awningColorList[random.randrange(len(awningColorList))]
    awningSubColor = awningSubColorList[random.randrange(len(awningSubColorList))]
    stiltColor = stiltColorList[random.randrange(len(stiltColorList))]
    stiltSubColor = stiltSubColorList[random.randrange(len(stiltSubColorList))] 
    
    yMin = 256
    needStilts = False    
    y, stilts = getGroundHeight(mc, pos.x-4, pos.z-4)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y
    y, stilts = getGroundHeight(mc, pos.x-4, pos.z+4)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y
    y, stilts = getGroundHeight(mc, pos.x+4, pos.z-4)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y
    y, stilts = getGroundHeight(mc, pos.x+4, pos.z+4)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y
    if (needStilts):
        pos.y = stiltsY
    else:
        pos.y = yMin
    mc.setBlocks(pos.x-4, pos.y, pos.z-4, pos.x+4, pos.y+10, pos.z+4, 0)
    
    # stilts
    if (needStilts):
        mc.setBlocks(pos.x-2, pos.y-1, pos.z-2, pos.x-2, pos.y-20, pos.z-2, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x-2, pos.y-1, pos.z+2, pos.x-2, pos.y-20, pos.z+2, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x+2, pos.y-1, pos.z-2, pos.x+2, pos.y-20, pos.z-2, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x+2, pos.y-1, pos.z+2, pos.x+2, pos.y-20, pos.z+2, stiltColor, stiltSubColor)
        
    # floor
    mc.setBlocks(pos.x-2, pos.y, pos.z-2, pos.x+2, pos.y, pos.z+2, floorColor)
    
    # north wall
    mc.setBlocks(pos.x-1, pos.y, pos.z-2, pos.x+1, pos.y+4, pos.z-2, floorColor)
    mc.setBlock(pos.x, pos.y+5, pos.z-2, floorColor)
    mc.setBlocks(pos.x-2, pos.y, pos.z-2, pos.x-2, pos.y+3, pos.z-2, postColor, postSubColor)
    mc.setBlocks(pos.x+2, pos.y, pos.z-2, pos.x+2, pos.y+3, pos.z-2, postColor, postSubColor)
    
    # south wall
    mc.setBlocks(pos.x-1, pos.y, pos.z+2, pos.x+1, pos.y+4, pos.z+2, floorColor)
    mc.setBlock(pos.x, pos.y+5, pos.z+2, floorColor)
    mc.setBlocks(pos.x-2, pos.y, pos.z+2, pos.x-2, pos.y+3, pos.z+2, postColor, postSubColor)
    mc.setBlocks(pos.x+2, pos.y, pos.z+2, pos.x+2, pos.y+3, pos.z+2, postColor, postSubColor)
    
    # east wall
    mc.setBlocks(pos.x+2, pos.y, pos.z-1, pos.x+2, pos.y+3, pos.z+1, floorColor)
    
    # west wall
    mc.setBlocks(pos.x-2, pos.y, pos.z-1, pos.x-2, pos.y+3, pos.z+1, floorColor)

    # stairs
    mc.setBlock(pos.x, pos.y, pos.z-3, stairColor, 2)
    mc.setBlock(pos.x-1, pos.y, pos.z-3, fenceColor, fenceSubColor)
    mc.setBlock(pos.x+1, pos.y, pos.z-3, fenceColor, fenceSubColor)
    mc.setBlock(pos.x-1, pos.y+1, pos.z-3, 50)
    mc.setBlock(pos.x+1, pos.y+1, pos.z-3, 50)
    mc.setBlock(pos.x, pos.y+3, pos.z-3, awningColor, awningSubColor+8)
    mc.setBlock(pos.x-1, pos.y+3, pos.z-3, awningColor, awningSubColor)
    mc.setBlock(pos.x+1, pos.y+3, pos.z-3, awningColor, awningSubColor)
    
    # door
    mc.setBlock(pos.x, pos.y+1, pos.z-2, doorColor, 1)
    mc.setBlock(pos.x, pos.y+2, pos.z-2, doorColor, 8)
    
    # roof
    mc.setBlocks(pos.x+3, pos.y+3, pos.z-3, pos.x+3, pos.y+3, pos.z+3, roofColor, roofSubColor+8)
    mc.setBlocks(pos.x-3, pos.y+3, pos.z-3, pos.x-3, pos.y+3, pos.z+3, roofColor, roofSubColor+8)
    mc.setBlocks(pos.x+2, pos.y+4, pos.z-3, pos.x+2, pos.y+4, pos.z+3, roofColor, roofSubColor+8)
    mc.setBlocks(pos.x-2, pos.y+4, pos.z-3, pos.x-2, pos.y+4, pos.z+3, roofColor, roofSubColor+8)
    mc.setBlocks(pos.x+1, pos.y+5, pos.z-3, pos.x+1, pos.y+5, pos.z+3, roofColor, roofSubColor+8)
    mc.setBlocks(pos.x-1, pos.y+5, pos.z-3, pos.x-1, pos.y+5, pos.z+3, roofColor, roofSubColor+8)
    mc.setBlocks(pos.x, pos.y+6, pos.z-3, pos.x, pos.y+6, pos.z+3, roofColor, roofSubColor+8)
    
    # windows
    mc.setBlock(pos.x-2, pos.y+2, pos.z, windowColor, windowSubColor)
    mc.setBlock(pos.x+2, pos.y+2, pos.z, windowColor, windowSubColor)
    mc.setBlock(pos.x, pos.y+2, pos.z+2, windowColor, windowSubColor)
    
def house3(mc, pos):
    floorColorList = [5, 5, 5, 5, 5, 5]
    floorSubColorList = [0, 1, 2, 3, 4, 5]
    slabColorList = [126, 126, 126, 126, 126, 126]
    slabSubColorList = [0, 1, 2, 3, 4, 5]
    wallColorList = [17, 17, 17, 17, 162, 162]
    wallSubColorList = [0, 1, 2, 3, 0, 1]
    windowColorList = [188, 189, 190, 191, 192]
    windowSubColorList = [0, 0, 0, 0, 0]
    roofColorList = [17, 17, 17, 17]
    roofSubColorList = [0, 1, 2, 3]
    postColorList = [162, 162, 17, 17, 17, 17]
    postSubColorList = [0, 1, 0, 1, 2, 3]    
    doorColorList = [193, 194, 195, 196, 197]
    stairColorList = [53, 67, 108, 109, 114, 128, 134, 135, 136, 156, 163, 164, 180]
    fenceColorList = [85, 139]
    fenceSubColorList = [0, 1]
    awningColorList = [182, 44, 44, 44, 44, 44, 44, 44, 44]
    awningSubColorList = [0, 0, 1, 2, 3, 4, 5, 6, 7]
    
    floorColor = floorColorList[random.randrange(len(floorColorList))]
    floorSubColor = floorSubColorList[random.randrange(len(floorSubColorList))]
    slabColor = slabColorList[random.randrange(len(slabColorList))]
    slabSubColor = slabSubColorList[random.randrange(len(slabSubColorList))]
    wallColor = wallColorList[random.randrange(len(wallColorList))]
    wallSubColor = wallSubColorList[random.randrange(len(wallSubColorList))]
    windowColor = windowColorList[random.randrange(len(windowColorList))]
    windowSubColor = windowSubColorList[random.randrange(len(windowSubColorList))]
    roofColor = roofColorList[random.randrange(len(roofColorList))]
    roofSubColor = roofSubColorList[random.randrange(len(roofSubColorList))]
    postColor = roofColorList[random.randrange(len(roofColorList))]
    postSubColor = roofSubColorList[random.randrange(len(roofSubColorList))]
    doorColor = doorColorList[random.randrange(len(doorColorList))]
    stairColor = stairColorList[random.randrange(len(stairColorList))]
    fenceColor = fenceColorList[random.randrange(len(fenceColorList))]
    fenceSubColor = fenceSubColorList[random.randrange(len(fenceSubColorList))]
    awningColor = awningColorList[random.randrange(len(awningColorList))]
    awningSubColor = awningSubColorList[random.randrange(len(awningSubColorList))]
    
    stiltColorList = [17, 17, 17, 17, 162, 162]
    stiltSubColorList = [0, 1, 2, 3, 0, 1]
    stiltColor = stiltColorList[random.randrange(len(stiltColorList))]
    stiltSubColor = stiltSubColorList[random.randrange(len(stiltSubColorList))]     
    
    yMin = 256
    needStilts = False    
    y, stilts = getGroundHeight(mc, pos.x-4, pos.z-4)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y 
    y, stilts = getGroundHeight(mc, pos.x-4, pos.z+4)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y 
    y, stilts = getGroundHeight(mc, pos.x+4, pos.z-4)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y 
    y, stilts = getGroundHeight(mc, pos.x+4, pos.z+4)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y 
    if (needStilts):
        pos.y = stiltsY
    else:
        pos.y = yMin
    mc.setBlocks(pos.x-4, pos.y, pos.z-4, pos.x+4, pos.y+10, pos.z+4, 0)

    # stilts
    if (needStilts):
        mc.setBlocks(pos.x-2, pos.y, pos.z-2, pos.x-2, pos.y-20, pos.z-2, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x-2, pos.y, pos.z+2, pos.x-2, pos.y-20, pos.z+2, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x+2, pos.y, pos.z-2, pos.x+2, pos.y-20, pos.z-2, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x+2, pos.y, pos.z+2, pos.x+2, pos.y-20, pos.z+2, stiltColor, stiltSubColor)
        pos.y += 1
    
    # floor
    mc.setBlocks(pos.x-2, pos.y-1, pos.z-2, pos.x+2, pos.y-1, pos.z+2, floorColor, floorSubColorList)
    
    # notrh wall
    mc.setBlocks(pos.x-1, pos.y, pos.z-2, pos.x+1, pos.y+3, pos.z-2, wallColor, wallSubColor)
    mc.setBlock(pos.x, pos.y, pos.z-2, doorColor, 1)
    mc.setBlock(pos.x, pos.y+1, pos.z-2, doorColor, 8)

    # south wall
    mc.setBlocks(pos.x-1, pos.y, pos.z+2, pos.x+1, pos.y+3, pos.z+2, wallColor, wallSubColor)
    mc.setBlock(pos.x, pos.y+1, pos.z+2, windowColor)

    # east wall
    mc.setBlocks(pos.x+2, pos.y, pos.z-1, pos.x+2, pos.y+3, pos.z+1, wallColor, wallSubColor)
    mc.setBlock(pos.x+2, pos.y+1, pos.z, windowColor)

    # west wall
    mc.setBlocks(pos.x-2, pos.y, pos.z-1, pos.x-2, pos.y+3, pos.z+1, wallColor, wallSubColor)
    mc.setBlock(pos.x-2, pos.y+1, pos.z, windowColor)
    
    # roof
    # layer 1
    mc.setBlocks(pos.x-2, pos.y+3, pos.z-3, pos.x+2, pos.y+3, pos.z-3, stairColor, 2) # north
    mc.setBlocks(pos.x-2, pos.y+3, pos.z+3, pos.x+2, pos.y+3, pos.z+3, stairColor, 3) # south
    mc.setBlocks(pos.x-3, pos.y+3, pos.z-2, pos.x-3, pos.y+3, pos.z+2, stairColor, 0) # west
    mc.setBlocks(pos.x+3, pos.y+3, pos.z-2, pos.x+3, pos.y+3, pos.z+2, stairColor, 1) # east
    mc.setBlock(pos.x-3, pos.y+3, pos.z-3, stairColor) # nw
    mc.setBlock(pos.x+3, pos.y+3, pos.z-3, stairColor, 1) # ne
    mc.setBlock(pos.x-3, pos.y+3, pos.z+3, stairColor) # sw
    mc.setBlock(pos.x+3, pos.y+3, pos.z+3, stairColor, 1) # se
    
    # layer 2
    mc.setBlocks(pos.x-1, pos.y+4, pos.z-2, pos.x+1, pos.y+4, pos.z-2, stairColor, 2) # north
    mc.setBlocks(pos.x-1, pos.y+4, pos.z+2, pos.x+1, pos.y+4, pos.z+2, stairColor, 3) # south
    mc.setBlocks(pos.x-2, pos.y+4, pos.z-1, pos.x-2, pos.y+4, pos.z+1, stairColor, 0) # west
    mc.setBlocks(pos.x+2, pos.y+4, pos.z-1, pos.x+2, pos.y+4, pos.z+1, stairColor, 1) # east
    mc.setBlock(pos.x-2, pos.y+4, pos.z-2, stairColor) # nw
    mc.setBlock(pos.x+2, pos.y+4, pos.z-2, stairColor, 1) # ne
    mc.setBlock(pos.x-2, pos.y+4, pos.z+2, stairColor) # sw
    mc.setBlock(pos.x+2, pos.y+4, pos.z+2, stairColor, 1) # se
    
    # layer 3
    mc.setBlock(pos.x, pos.y+5, pos.z-1, stairColor, 2) # north
    mc.setBlock(pos.x, pos.y+5, pos.z+1, stairColor, 3) # south
    mc.setBlock(pos.x-1, pos.y+5, pos.z, stairColor, 0) # west
    mc.setBlock(pos.x+1, pos.y+5, pos.z, stairColor, 1) # east
    mc.setBlock(pos.x-1, pos.y+5, pos.z-1, stairColor) # nw
    mc.setBlock(pos.x+1, pos.y+5, pos.z-1, stairColor, 1) # ne
    mc.setBlock(pos.x-1, pos.y+5, pos.z+1, stairColor) # sw
    mc.setBlock(pos.x+1, pos.y+5, pos.z+1, stairColor, 1) # se
    
    # layer 4
    mc.setBlock(pos.x, pos.y+6, pos.z, slabColor, slabSubColor)
    
    # torches
    mc.setBlock(pos.x-1, pos.y, pos.z-3, 50)
    mc.setBlock(pos.x+1, pos.y, pos.z-3, 50)
    
def house4(mc, pos):
    floorColorList = [4, 1, 1, 1, 1, 1, 1, 1, 24, 24, 24, 45]
    floorSubColorList = [0, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 0]
    floorColor = floorColorList[random.randrange(len(floorColorList))]
    floorSubColor = floorSubColorList[random.randrange(len(floorSubColorList))]
    roofColorList = [4, 1, 1, 1, 1, 1, 1, 1, 24, 24, 24, 45]
    roofSubColorList = [0, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 0]
    roofColor = roofColorList[random.randrange(len(roofColorList))]
    roofSubColor = roofSubColorList[random.randrange(len(roofSubColorList))]
    stiltColorList = [17, 17, 17, 17, 162, 162]
    stiltSubColorList = [0, 1, 2, 3, 0, 1]
    stiltColor = stiltColorList[random.randrange(len(stiltColorList))]
    stiltSubColor = stiltSubColorList[random.randrange(len(stiltSubColorList))]     
    
    yMin = 256
    needStilts = False
    y, stilts = getGroundHeight(mc, pos.x-3, pos.z-3)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y 
    y, stilts = getGroundHeight(mc, pos.x+2, pos.z-3)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y 
    y, stilts = getGroundHeight(mc, pos.x+2, pos.z+4)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y 
    y, stilts = getGroundHeight(mc, pos.x-3, pos.z+4)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y 
    if (needStilts):
        pos.y = stiltsY
    else:
        pos.y = yMin
    mc.setBlocks(pos.x-4, pos.y, pos.z-5, pos.x+4, pos.y+10, pos.z+5, 0)
    
    # stilts
    if (needStilts):
        mc.setBlocks(pos.x-3, pos.y, pos.z-3, pos.x-3, pos.y-20, pos.z-3, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x+2, pos.y, pos.z-3, pos.x+2, pos.y-20, pos.z-3, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x+2, pos.y, pos.z+1, pos.x+2, pos.y-20, pos.z+1, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x, pos.y, pos.z+4, pos.x, pos.y-20, pos.z+4, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x-3, pos.y, pos.z+4, pos.x-3, pos.y-20, pos.z+4, stiltColor, stiltSubColor)
        pos.y += 1
            
    # floor
    mc.setBlocks(pos.x-3, pos.y-1, pos.z-3, pos.x, pos.y-1, pos.z+4, floorColor, floorSubColor)
    mc.setBlocks(pos.x+1, pos.y-1, pos.z-3, pos.x+1, pos.y-1, pos.z+3, floorColor, floorSubColor)
    mc.setBlocks(pos.x+2, pos.y-1, pos.z-3, pos.x+2, pos.y-1, pos.z+1, floorColor, floorSubColor)
    
    # north wall
    mc.setBlocks(pos.x-3, pos.y, pos.z-3, pos.x+2, pos.y+2, pos.z-3, floorColor, floorSubColor)
    mc.setBlocks(pos.x, pos.y, pos.z-3, pos.x, pos.y+1, pos.z-3, 0)
    
    # east wall
    mc.setBlocks(pos.x+2, pos.y, pos.z-2, pos.x+2, pos.y+2, pos.z+1, floorColor, floorSubColor)
    mc.setBlocks(pos.x+1, pos.y, pos.z+2, pos.x+1, pos.y+2, pos.z+3, floorColor, floorSubColor)

    # south wall
    mc.setBlocks(pos.x, pos.y, pos.z+4, pos.x-3, pos.y+2, pos.z+4, floorColor, floorSubColor)
    
    # west wall
    mc.setBlocks(pos.x-3, pos.y, pos.z-2, pos.x-3, pos.y+2, pos.z+3, floorColor, floorSubColor)
    
    # furnace
    mc.setBlocks(pos.x, pos.y, pos.z+2, pos.x-2, pos.y, pos.z+2, floorColor, floorSubColor)
    mc.setBlocks(pos.x-2, pos.y, pos.z+3, pos.x-2, pos.y+1, pos.z+3, floorColor, floorSubColor)
    mc.setBlocks(pos.x, pos.y, pos.z+3, pos.x-1, pos.y, pos.z+3, 11) # lava
    mc.setBlocks(pos.x, pos.y+2, pos.z+3, pos.x-2, pos.y+2, pos.z+2, floorColor, floorSubColor)
    mc.setBlock(pos.x, pos.y+1, pos.z+2, 101) # iron bars
    mc.setBlock(pos.x-2, pos.y+1, pos.z+2, 101) # iron bars
    
    # roof
    mc.setBlocks(pos.x-2, pos.y+3, pos.z-2, pos.x+1, pos.y+3, pos.z+1, roofColor, roofSubColor)
    mc.setBlocks(pos.x-1, pos.y+4, pos.z-1, pos.x, pos.y+4, pos.z, roofColor, roofSubColor)
    
    # torches
    mc.setBlock(pos.x-2, pos.y, pos.z-2, 50)
    mc.setBlock(pos.x+1, pos.y, pos.z, 50)
    mc.setBlock(pos.x-3, pos.y+3, pos.z-3, 50)
    mc.setBlock(pos.x+2, pos.y+3, pos.z-3, 50)
    
    
def house5(mc, pos):
    floorColorList = [5, 5, 5, 5, 5, 5]
    floorSubColorList = [0, 1, 2, 3, 4, 5]
    floorColor = floorColorList[random.randrange(len(floorColorList))]
    floorSubColor = floorSubColorList[random.randrange(len(floorSubColorList))]
    roofColorList = [5, 5, 5, 5, 5, 5]
    roofSubColorList = [0, 1, 2, 3, 4, 5]
    roofColor = roofColorList[random.randrange(len(roofColorList))]
    roofSubColor = roofSubColorList[random.randrange(len(roofSubColorList))]
    stiltColorList = [17, 17, 17, 17, 162, 162]
    stiltSubColorList = [0, 1, 2, 3, 0, 1]
    stiltColor = stiltColorList[random.randrange(len(stiltColorList))]
    stiltSubColor = stiltSubColorList[random.randrange(len(stiltSubColorList))]     
    wallColorList = [1, 1, 1, 1, 1, 1]
    wallSubColorList = [0, 1, 2, 3, 4, 5]    
    wallColor = wallColorList[random.randrange(len(wallColorList))]
    wallSubColor = wallSubColorList[random.randrange(len(wallSubColorList))]
    
    radius = 4
    yMin = 256
    needStilts = False
    y, stilts = getGroundHeight(mc, pos.x-radius, pos.z-radius)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y 
    y, stilts = getGroundHeight(mc, pos.x+radius, pos.z-radius)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y 
    y, stilts = getGroundHeight(mc, pos.x+radius, pos.z+radius)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y 
    y, stilts = getGroundHeight(mc, pos.x-radius, pos.z+radius)
    if (y < yMin):
        yMin = y
    if (stilts):
        needStilts = True
        stiltsY = y 
    if (needStilts):
        pos.y = stiltsY
    else:
        pos.y = yMin
    mc.setBlocks(pos.x-(radius+1), pos.y, pos.z-(radius+1), pos.x+(radius+1), pos.y+radius, pos.z+(radius+1), 0)
    
    # stilts
    if (needStilts):
        mc.setBlocks(pos.x-4, pos.y, pos.z, pos.x-4, pos.y-20, pos.z, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x+4, pos.y, pos.z, pos.x+4, pos.y-20, pos.z, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x, pos.y, pos.z+4, pos.x, pos.y-20, pos.z+4, stiltColor, stiltSubColor)
        mc.setBlocks(pos.x, pos.y, pos.z-4, pos.x, pos.y-20, pos.z-4, stiltColor, stiltSubColor)
        pos.y += 1
        
    # floor
    pos.y -= 1
    circle(mc, pos, radius, True, floorColor, floorSubColor)
    mc.setBlock(pos.x, pos.y+1, pos.z, 50)
    
    # walls
    pos.y += 1
    circle(mc, pos, radius, False, wallColor, wallSubColor)
    pos.y += 1
    circle(mc, pos, radius, False, wallColor, wallSubColor)
    pos.y += 1
    circle(mc, pos, radius, False, wallColor, wallSubColor)
    
    # door
    mc.setBlocks(pos.x, pos.y-1, pos.z-radius, pos.x, pos.y-2, pos.z-radius, 0)
    
    # for i in range(10):
    #     pos.y += 1
    #     circle(mc, pos, radius, False, wallColor, wallSubColor)
    
    # roof
    r = radius + 1
    for i in range(radius+1):
        pos.y += 1
        circle(mc, pos, r-i, False, roofColor, roofSubColor)
    pos.y += 1
    mc.setBlock(pos.x, pos.y, pos.z, roofColor, roofSubColor)
    mc.setBlock(pos.x, pos.y+1, pos.z, 50)
            
    
    