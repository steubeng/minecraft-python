from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3

# return the ground height but don't consider the blocks in blockList to be the ground
# also returns true if we should build stilts under the house (because we're on water)
# or false if stilts are not needed
def getGroundHeight(mc, x, z):
    blockList = [0, 6, 8, 9, 10, 11, 17, 18, 30, 31, 32, 37, 38, 39, 40, 50, 51, 55, 59, 78, 81, 83, 104, 105, 106]
    y = mc.getHeight(x, z)
    blockId = mc.getBlock(x, y, z)
    if (blockId == 8 or blockId == 9):
        return y+1, True
    while (blockId in blockList):
        y -= 1
        blockId = mc.getBlock(x, y, z)
        if (blockId == 8 or blockId == 9):
            return y+1, True
    return y+1, False


def circle(mc, pos, r, fill=False, blockId=4, subBlockId=0):
    n = 2 * r + 1
    x = int(pos.x)
    z = int(pos.z)
    for i in range(n):
        for j in range(n):
            x = i-r; 
            z = j-r;
            if (fill):
                if (x*x + z*z <= r*r+1):
                    mc.setBlock(pos.x+x, pos.y, pos.z+z, blockId)
            else:
                if ((x*x + z*z <= r*r+1) and (x*x + z*z > (r-1)*(r-1))):
                    mc.setBlock(pos.x+x, pos.y, pos.z+z, blockId)