from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
import random

mc = Minecraft.create()
mc.postToChat("House time!!!")

pos = mc.player.getPos()
wallHeight = 5
housePos = Vec3(pos.x, mc.getHeight(pos.x, pos.z+10), pos.z+10)


def floor(pos, sizeX, sizeZ):
    mc.setBlocks(pos.x, pos.y, pos.z, pos.x+sizeX, pos.y, pos.z+sizeZ, 98)
    
def frontAndBackWall(pos, sizeX, sizeZ, wallHeight):
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
    
def leftAndRightWall(pos, sizeX, sizeZ, wallHeight):
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
    
def roof(pos, sizeX, sizeZ, wallHeight):
    for roofLayer in range(sizeX // 2):
        mc.setBlocks(pos.x + roofLayer + 1, pos.y + wallHeight + roofLayer + 1, pos.z, pos.x + sizeX - roofLayer - 1, pos.y + wallHeight + roofLayer + 1, pos.z, 5, 1)
        mc.setBlocks(pos.x + roofLayer + 1, pos.y + wallHeight + roofLayer + 1, pos.z+sizeZ, pos.x + sizeX - roofLayer - 1, pos.y + wallHeight + roofLayer + 1, pos.z+sizeZ, 5, 1)
    for roofLayer in range(sizeX // 2 + 2):
        mc.setBlocks(pos.x-1+roofLayer, pos.y+wallHeight+roofLayer, pos.z-1, pos.x-1+roofLayer, pos.y+wallHeight+roofLayer, pos.z+sizeZ+1, 5, 2)
        mc.setBlocks(pos.x+sizeX+1-roofLayer, pos.y+wallHeight+roofLayer, pos.z-1, pos.x+sizeX+1-roofLayer, pos.y+wallHeight+roofLayer, pos.z+sizeZ+1, 5, 2)
    
def torchesAlongSidewalls(pos, sizeX, sizeZ):
    torchSpacing = 5
    for torchZ in range((sizeZ-2) // torchSpacing + 1):
        mc.setBlock(pos.x+1, pos.y+1, pos.z+1+torchZ*torchSpacing, 50)
        mc.setBlock(pos.x+sizeX-1, pos.y+1, pos.z+1+torchZ*torchSpacing, 50)
        
def frontPorch(pos, sizeX, sizeZ):
    mc.setBlocks(pos.x+(sizeX//2)-3, pos.y, pos.z-1, pos.x+(sizeX//2)+3, pos.y, pos.z-1-(sizeZ//4), 98)
    
    steps = 10
    for step in range(steps):
        mc.setBlocks(pos.x+(sizeX//2)-3, pos.y-step-1, pos.z-2-(sizeZ//4)-step, pos.x+(sizeX//2)+3, pos.y-step-1, pos.z-2-(sizeZ//4)-step, 98)

def stilts(pos, sizeX, sizeZ):
    stiltHeight = 10
    mc.setBlocks(pos.x, pos.y-1, pos.z, pos.x, pos.y-1-stiltHeight, pos.z, 17, 1)
    mc.setBlocks(pos.x+sizeX, pos.y-1, pos.z, pos.x+sizeX, pos.y-1-stiltHeight, pos.z, 17, 1)
    mc.setBlocks(pos.x, pos.y-1, pos.z+sizeZ, pos.x, pos.y-1-stiltHeight, pos.z+sizeZ, 17, 1)
    mc.setBlocks(pos.x+sizeX, pos.y-1, pos.z+sizeZ, pos.x+sizeX, pos.y-1-stiltHeight, pos.z+sizeZ, 17, 1)
    
def clearSpace(pos, sizeX, sizeZ):
    mc.setBlocks(pos.x-2, pos.y, pos.z-2, pos.x+sizeX+2, pos.y+100, pos.z+sizeZ+2, 0)

def house(pos, sizeX, sizeZ):
    print("house:", sizeX, "x", sizeZ, "at", pos)
    clearSpace(pos, sizeX, sizeZ)
    floor(pos, sizeX, sizeZ)
    frontAndBackWall(pos, sizeX, sizeZ, wallHeight)
    leftAndRightWall(pos, sizeX, sizeZ, wallHeight)
    roof(pos, sizeX, sizeZ, wallHeight)
    torchesAlongSidewalls(pos, sizeX, sizeZ)
    frontPorch(pos, sizeX, sizeZ)
    stilts(pos, sizeX, sizeZ)
    
house(housePos, random.randint(7, 30), random.randint(7, 30))


