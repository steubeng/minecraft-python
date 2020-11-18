from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3

mc = Minecraft.create()
mc.postToChat("Creeper Head!")

pos = mc.player.getPos()

def creeperHead(pos): 
    mc.setBlocks(pos.x+6, pos.y, pos.z, pos.x+6+6, pos.y+7, pos.z+7, 35, 5)

    # layer 1
    mc.setBlock(pos.x+5, pos.y, pos.z+0, 35, 5)
    mc.setBlock(pos.x+5, pos.y, pos.z+1, 35, 5)
    mc.setBlock(pos.x+5, pos.y, pos.z+2, 35, 15)
    mc.setBlock(pos.x+5, pos.y, pos.z+3, 35, 5)
    mc.setBlock(pos.x+5, pos.y, pos.z+4, 35, 5)
    mc.setBlock(pos.x+5, pos.y, pos.z+5, 35, 15)
    mc.setBlock(pos.x+5, pos.y, pos.z+6, 35, 5)
    mc.setBlock(pos.x+5, pos.y, pos.z+7, 35, 5)

    # layer 2
    mc.setBlock(pos.x+5, pos.y+1, pos.z+0, 35, 5)
    mc.setBlock(pos.x+5, pos.y+1, pos.z+1, 35, 5)
    mc.setBlock(pos.x+5, pos.y+1, pos.z+2, 35, 15)
    mc.setBlock(pos.x+5, pos.y+1, pos.z+3, 35, 15)
    mc.setBlock(pos.x+5, pos.y+1, pos.z+4, 35, 15)
    mc.setBlock(pos.x+5, pos.y+1, pos.z+5, 35, 15)
    mc.setBlock(pos.x+5, pos.y+1, pos.z+6, 35, 5)
    mc.setBlock(pos.x+5, pos.y+1, pos.z+7, 35, 5)

    # layer 3
    mc.setBlock(pos.x+5, pos.y+2, pos.z+0, 35, 5)
    mc.setBlock(pos.x+5, pos.y+2, pos.z+1, 35, 5)
    mc.setBlock(pos.x+5, pos.y+2, pos.z+2, 35, 15)
    mc.setBlock(pos.x+5, pos.y+2, pos.z+3, 35, 15)
    mc.setBlock(pos.x+5, pos.y+2, pos.z+4, 35, 15)
    mc.setBlock(pos.x+5, pos.y+2, pos.z+5, 35, 15)
    mc.setBlock(pos.x+5, pos.y+2, pos.z+6, 35, 5)
    mc.setBlock(pos.x+5, pos.y+2, pos.z+7, 35, 5)

    # layer 4
    mc.setBlock(pos.x+5, pos.y+3, pos.z+0, 35, 5)
    mc.setBlock(pos.x+5, pos.y+3, pos.z+1, 35, 5)
    mc.setBlock(pos.x+5, pos.y+3, pos.z+2, 35, 5)
    mc.setBlock(pos.x+5, pos.y+3, pos.z+3, 35, 15)
    mc.setBlock(pos.x+5, pos.y+3, pos.z+4, 35, 15)
    mc.setBlock(pos.x+5, pos.y+3, pos.z+5, 35, 5)
    mc.setBlock(pos.x+5, pos.y+3, pos.z+6, 35, 5)
    mc.setBlock(pos.x+5, pos.y+3, pos.z+7, 35, 5)

    # lsyer 5
    mc.setBlock(pos.x+5, pos.y+4, pos.z+0, 35, 5)
    mc.setBlock(pos.x+5, pos.y+4, pos.z+1, 35, 15)
    mc.setBlock(pos.x+5, pos.y+4, pos.z+2, 35, 15)
    mc.setBlock(pos.x+5, pos.y+4, pos.z+3, 35, 5)
    mc.setBlock(pos.x+5, pos.y+4, pos.z+4, 35, 5)
    mc.setBlock(pos.x+5, pos.y+4, pos.z+5, 35, 15)
    mc.setBlock(pos.x+5, pos.y+4, pos.z+6, 35, 15)
    mc.setBlock(pos.x+5, pos.y+4, pos.z+7, 35, 5)

    # layer 6
    mc.setBlock(pos.x+5, pos.y+5, pos.z+0, 35, 15)
    mc.setBlock(pos.x+5, pos.y+5, pos.z+1, 35, 15)
    mc.setBlock(pos.x+5, pos.y+5, pos.z+2, 35, 15)
    mc.setBlock(pos.x+5, pos.y+5, pos.z+3, 35, 5)
    mc.setBlock(pos.x+5, pos.y+5, pos.z+4, 35, 5)
    mc.setBlock(pos.x+5, pos.y+5, pos.z+5, 35, 15)
    mc.setBlock(pos.x+5, pos.y+5, pos.z+6, 35, 15)
    mc.setBlock(pos.x+5, pos.y+5, pos.z+7, 35, 5)

    # layer 7
    for i in range(8):
        mc.setBlock(pos.x+5, pos.y+6, pos.z+i, 35, 5)

    # layer 8
    for i in range(8):
        mc.setBlock(pos.x+5, pos.y+7, pos.z+i, 35, 5)


creeperHead(pos)
