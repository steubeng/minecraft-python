from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
import random

def floor(mc, pos, sizeX, sizeZ):
    mc.setBlocks(pos.x, pos.y, pos.z, pos.x+sizeX, pos.y, pos.z+sizeZ, 98)
    
def frontAndBackWall(mc, pos, sizeX, sizeZ, wallHeight):
    # front wall
    mc.setBlocks(pos.x+1, pos.y+1, pos.z, pos.x+sizeX-1, pos.y+wallHeight-1, pos.z, 5, 1)
    mc.setBlocks(pos.x, pos.y+1, pos.z, pos.x, pos.y+wallHeight-1, pos.z, 17,1)
    mc.setBlocks(pos.x+sizeX, pos.y+1, pos.z, pos.x+sizeX, pos.y+wallHeight-1, pos.z, 17,1)
    mc.setBlocks(pos.x+1, pos.y+1, pos.z+sizeZ, pos.x+sizeX-1, pos.y+wallHeight-1, pos.z+sizeZ, 5, 1)
    
    # front door
    if (wallHeight > 2):
        mc.setBlock(pos.x+(sizeX//2), pos.y+1, pos.z, 64, 0)
        mc.setBlock(pos.x+(sizeX//2), pos.y+2, pos.z, 64, 8)

    # front windows
    if (sizeX > 5 and wallHeight > 2):
        mc.setBlock(pos.x+(sizeX//2 - 2), pos.y+2, pos.z, 102)
        mc.setBlock(pos.x+(sizeX//2 + 2), pos.y+2, pos.z, 102)
    
    # back wall
    mc.setBlocks(pos.x, pos.y+1, pos.z+sizeZ, pos.x, pos.y+wallHeight-1, pos.z+sizeZ, 17,1)
    mc.setBlocks(pos.x+sizeX, pos.y+1, pos.z+sizeZ, pos.x+sizeX, pos.y+wallHeight-1, pos.z+sizeZ, 17,1)
    mc.setBlocks(pos.x, pos.y+wallHeight, pos.z, pos.x+sizeX, pos.y+wallHeight, pos.z, 17, 1)
    mc.setBlocks(pos.x, pos.y+wallHeight, pos.z+sizeZ, pos.x+sizeX, pos.y+wallHeight, pos.z+sizeZ, 17, 1)
    
def leftAndRightWall(mc, pos, sizeX, sizeZ, wallHeight):
    # left wall
    mc.setBlocks(pos.x, pos.y+1, pos.z+1, pos.x, pos.y+wallHeight-1, pos.z+sizeZ-1, 5, 1)
    mc.setBlocks(pos.x+sizeX, pos.y+1, pos.z+1, pos.x+sizeX, pos.y+wallHeight-1, pos.z+sizeZ-1, 5, 1)
    
    # right wall
    mc.setBlocks(pos.x, pos.y+wallHeight, pos.z, pos.x, pos.y+wallHeight, pos.z+sizeZ, 17, 1)
    mc.setBlocks(pos.x+sizeX, pos.y+wallHeight, pos.z, pos.x+sizeX, pos.y+wallHeight, pos.z+sizeZ, 17, 1)
    
    # windows
    windowSpacing = 3
    for windowZ in range((sizeZ-4) // windowSpacing + 1):
        mc.setBlock(pos.x, pos.y+2, pos.z+2+windowZ*windowSpacing, 102)
        mc.setBlock(pos.x+sizeX, pos.y+2, pos.z+2+windowZ*windowSpacing, 102)
    
def roof(mc, pos, sizeX, sizeZ, wallHeight):
    for roofLayer in range(sizeX // 2):
        mc.setBlocks(pos.x + roofLayer + 1, pos.y + wallHeight + roofLayer + 1, pos.z, pos.x + sizeX - roofLayer - 1, pos.y + wallHeight + roofLayer + 1, pos.z, 5, 1)
        mc.setBlocks(pos.x + roofLayer + 1, pos.y + wallHeight + roofLayer + 1, pos.z+sizeZ, pos.x + sizeX - roofLayer - 1, pos.y + wallHeight + roofLayer + 1, pos.z+sizeZ, 5, 1)
    for roofLayer in range(sizeX // 2 + 2):
        mc.setBlocks(pos.x-1+roofLayer, pos.y+wallHeight+roofLayer, pos.z-1, pos.x-1+roofLayer, pos.y+wallHeight+roofLayer, pos.z+sizeZ+1, 5, 2)
        mc.setBlocks(pos.x+sizeX+1-roofLayer, pos.y+wallHeight+roofLayer, pos.z-1, pos.x+sizeX+1-roofLayer, pos.y+wallHeight+roofLayer, pos.z+sizeZ+1, 5, 2)
    
def torchesAlongSidewalls(mc, pos, sizeX, sizeZ):
    torchSpacing = 5
    for torchZ in range((sizeZ-2) // torchSpacing + 1):
        mc.setBlock(pos.x+1, pos.y+1, pos.z+1+torchZ*torchSpacing, 50)
        mc.setBlock(pos.x+sizeX-1, pos.y+1, pos.z+1+torchZ*torchSpacing, 50)
        
def frontPorch(mc, pos, sizeX, sizeZ):
    mc.setBlocks(pos.x+(sizeX//2)-3, pos.y, pos.z-1, pos.x+(sizeX//2)+3, pos.y, pos.z-1-(sizeZ//4), 98)
    
    steps = 10
    for step in range(steps):
        mc.setBlocks(pos.x+(sizeX//2)-3, pos.y-step-1, pos.z-2-(sizeZ//4)-step, pos.x+(sizeX//2)+3, pos.y-step-1, pos.z-2-(sizeZ//4)-step, 98)

def stilts(mc, pos, sizeX, sizeZ):
    stiltHeight = 10
    mc.setBlocks(pos.x, pos.y-1, pos.z, pos.x, pos.y-1-stiltHeight, pos.z, 17, 1)
    mc.setBlocks(pos.x+sizeX, pos.y-1, pos.z, pos.x+sizeX, pos.y-1-stiltHeight, pos.z, 17, 1)
    mc.setBlocks(pos.x, pos.y-1, pos.z+sizeZ, pos.x, pos.y-1-stiltHeight, pos.z+sizeZ, 17, 1)
    mc.setBlocks(pos.x+sizeX, pos.y-1, pos.z+sizeZ, pos.x+sizeX, pos.y-1-stiltHeight, pos.z+sizeZ, 17, 1)
    
def clearSpace(mc, pos, sizeX, sizeZ):
    mc.setBlocks(pos.x-2, pos.y, pos.z-2, pos.x+sizeX+2, pos.y+100, pos.z+sizeZ+2, 0)

def house(mc, pos, sizeX, sizeZ):
    # print("house:", sizeX, "x", sizeZ, "at", pos)
    wallHeight = 5
    clearSpace(mc, pos, sizeX, sizeZ)
    floor(mc, pos, sizeX, sizeZ)
    frontAndBackWall(mc, pos, sizeX, sizeZ, wallHeight)
    leftAndRightWall(mc, pos, sizeX, sizeZ, wallHeight)
    roof(mc, pos, sizeX, sizeZ, wallHeight)
    torchesAlongSidewalls(mc, pos, sizeX, sizeZ)
    frontPorch(mc, pos, sizeX, sizeZ)
    stilts(mc, pos, sizeX, sizeZ)
    
def christmasTree(mc, pos):
    print("christmasTree:", pos)

    layer = 0
    mc.setBlock(pos.x, pos.y+layer, pos.z, 17, 1)
    
    layer += 1
    mc.setBlock(pos.x, pos.y+layer, pos.z, 17, 1)
    mc.setBlock(pos.x-1, pos.y+layer, pos.z-3, 18, 1)
    mc.setBlock(pos.x+1, pos.y+layer, pos.z-3, 18, 1)
    mc.setBlock(pos.x-2, pos.y+layer, pos.z-2, 18, 1)
    mc.setBlock(pos.x, pos.y+layer, pos.z-2, 18, 1)
    mc.setBlock(pos.x+2, pos.y+layer, pos.z-2, 18, 1)
    mc.setBlock(pos.x-3, pos.y+layer, pos.z-1, 18, 1)
    mc.setBlock(pos.x+3, pos.y+layer, pos.z-1, 18, 1)
    mc.setBlock(pos.x-2, pos.y+layer, pos.z, 18, 1)
    mc.setBlock(pos.x+2, pos.y+layer, pos.z, 18, 1)
    mc.setBlock(pos.x-1, pos.y+layer, pos.z+3, 18, 1)
    mc.setBlock(pos.x+1, pos.y+layer, pos.z+3, 18, 1)
    mc.setBlock(pos.x-2, pos.y+layer, pos.z+2, 18, 1)
    mc.setBlock(pos.x, pos.y+layer, pos.z+2, 18, 1)
    mc.setBlock(pos.x+2, pos.y+layer, pos.z+2, 18, 1)
    mc.setBlock(pos.x-3, pos.y+layer, pos.z+1, 18, 1)
    mc.setBlock(pos.x+3, pos.y+layer, pos.z+1, 18, 1)
    
    layer += 1
    mc.setBlock(pos.x, pos.y+layer, pos.z, 17, 1)
    mc.setBlock(pos.x-1, pos.y+layer, pos.z-3, 18, 1)
    mc.setBlock(pos.x, pos.y+layer, pos.z-3, 18, 1)
    mc.setBlock(pos.x+1, pos.y+layer, pos.z-3, 18, 1)
    mc.setBlock(pos.x-1, pos.y+layer, pos.z-1, 18, 1)
    mc.setBlock(pos.x-3, pos.y+layer, pos.z-1, 18, 1)
    mc.setBlock(pos.x+1, pos.y+layer, pos.z-1, 18, 1)
    mc.setBlock(pos.x+3, pos.y+layer, pos.z-1, 18, 1)
    
    mc.setBlock(pos.x-3, pos.y+layer, pos.z, 18, 1)
    mc.setBlock(pos.x+3, pos.y+layer, pos.z, 18, 1)
    
    mc.setBlock(pos.x-1, pos.y+layer, pos.z+3, 18, 1)
    mc.setBlock(pos.x, pos.y+layer, pos.z+3, 18, 1)
    mc.setBlock(pos.x+1, pos.y+layer, pos.z+3, 18, 1)
    mc.setBlock(pos.x-1, pos.y+layer, pos.z+1, 18, 1)
    mc.setBlock(pos.x-3, pos.y+layer, pos.z+1, 18, 1)
    mc.setBlock(pos.x+1, pos.y+layer, pos.z+1, 18, 1)
    mc.setBlock(pos.x+3, pos.y+layer, pos.z+1, 18, 1)

    layer += 1
    mc.setBlock(pos.x, pos.y+layer, pos.z, 17, 1)
    mc.setBlock(pos.x, pos.y+layer, pos.z-2, 18, 1)
    mc.setBlock(pos.x-1, pos.y+layer, pos.z-2, 18, 1)
    mc.setBlock(pos.x+1, pos.y+layer, pos.z-2, 18, 1)
    mc.setBlock(pos.x, pos.y+layer, pos.z+2, 18, 1)
    mc.setBlock(pos.x-1, pos.y+layer, pos.z+2, 18, 1)
    mc.setBlock(pos.x+1, pos.y+layer, pos.z+2, 18, 1)
    mc.setBlock(pos.x-2, pos.y+layer, pos.z, 18, 1)
    mc.setBlock(pos.x-2, pos.y+layer, pos.z-1, 18, 1)
    mc.setBlock(pos.x-2, pos.y+layer, pos.z+1, 18, 1)
    mc.setBlock(pos.x+2, pos.y+layer, pos.z, 18, 1)
    mc.setBlock(pos.x+2, pos.y+layer, pos.z-1, 18, 1)
    mc.setBlock(pos.x+2, pos.y+layer, pos.z+1, 18, 1)
    
    layer += 1
    mc.setBlock(pos.x, pos.y+layer, pos.z, 17, 1)
    mc.setBlock(pos.x, pos.y+layer, pos.z-1, 18, 1)
    mc.setBlock(pos.x-1, pos.y+layer, pos.z-2, 18, 1)
    mc.setBlock(pos.x+1, pos.y+layer, pos.z-2, 18, 1)
    mc.setBlock(pos.x, pos.y+layer, pos.z+1, 18, 1)
    mc.setBlock(pos.x-1, pos.y+layer, pos.z+2, 18, 1)
    mc.setBlock(pos.x+1, pos.y+layer, pos.z+2, 18, 1)
    mc.setBlock(pos.x-1, pos.y+layer, pos.z, 18, 1)
    mc.setBlock(pos.x-2, pos.y+layer, pos.z+1, 18, 1)
    mc.setBlock(pos.x-2, pos.y+layer, pos.z-1, 18, 1)
    mc.setBlock(pos.x+1, pos.y+layer, pos.z, 18, 1)
    mc.setBlock(pos.x+2, pos.y+layer, pos.z+1, 18, 1)
    mc.setBlock(pos.x+2, pos.y+layer, pos.z-1, 18, 1)

    layer += 1
    mc.setBlock(pos.x, pos.y+layer, pos.z, 17, 1)
    mc.setBlock(pos.x-1, pos.y+layer, pos.z-1, 18, 1)
    mc.setBlock(pos.x, pos.y+layer, pos.z-1, 18, 1)
    mc.setBlock(pos.x+1, pos.y+layer, pos.z-1, 18, 1)
    mc.setBlock(pos.x-1, pos.y+layer, pos.z+1, 18, 1)
    mc.setBlock(pos.x, pos.y+layer, pos.z+1, 18, 1)
    mc.setBlock(pos.x+1, pos.y+layer, pos.z+1, 18, 1)
    mc.setBlock(pos.x-1, pos.y+layer, pos.z, 18, 1)
    mc.setBlock(pos.x+1, pos.y+layer, pos.z, 18, 1)
    
    layer += 1
    mc.setBlock(pos.x, pos.y+layer, pos.z, 17, 1)
    mc.setBlock(pos.x+1, pos.y+layer, pos.z, 18, 1)
    mc.setBlock(pos.x-1, pos.y+layer, pos.z, 18, 1)
    mc.setBlock(pos.x, pos.y+layer, pos.z+1, 18, 1)
    mc.setBlock(pos.x, pos.y+layer, pos.z-1, 18, 1)

    layer += 1
    mc.setBlock(pos.x, pos.y+layer, pos.z, 18, 1)

    layer += 1
    mc.setBlock(pos.x, pos.y+layer, pos.z, 18, 1)

# mc = Minecraft.create()
# mc.postToChat("House time!!!")
# pos = mc.player.getPos()
# housePos = Vec3(pos.x, mc.getHeight(pos.x, pos.z+10), pos.z+10)
# house(housePos, random.randint(7, 30), random.randint(7, 30))


