from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
from collections import deque
from mcpi import block
import time

mc = Minecraft.create()
mc.postToChat("Wall mode!!!")
queue = deque([])
minimumQueueSize = 2

previousPos = mc.player.getTilePos()

def getDirection(posPrev, posCurrent):
    if (posPrev.z < posCurrent.z):
        return "s"
    elif (posPrev.z > posCurrent.z):
        return "n"
    elif (posPrev.x < posCurrent.x):
        return "e"
    elif (posPrev.x > posCurrent.x):
        return "w"
    elif (posPrev.y < posCurrent.y):
        return "u"
    elif (posPrev.y > posCurrent.y):
        return "d"

parapetCounter = 0
while(True):
    currentPos = mc.player.getTilePos()
    if (previousPos.x != currentPos.x or previousPos.y != currentPos.y or previousPos.z != currentPos.z):
        direction = getDirection(previousPos, currentPos)
        print('prevPos:',previousPos,'currentPos:',currentPos,'direction:',direction,'queueSize',len(queue))
        
        # do these now
        if (direction == 'n'):
            mc.setBlocks(currentPos.x-2, currentPos.y-1, currentPos.z-2, currentPos.x+2, currentPos.y+3, currentPos.z-3, block.AIR)
            mc.setBlocks(currentPos.x-1, currentPos.y+4, currentPos.z-2, currentPos.x+1, currentPos.y+4, currentPos.z-3, block.AIR)
        elif (direction == 's'):
            mc.setBlocks(currentPos.x-2, currentPos.y-1, currentPos.z+2, currentPos.x+2, currentPos.y+3, currentPos.z+3, block.AIR)
            mc.setBlocks(currentPos.x-1, currentPos.y+4, currentPos.z+2, currentPos.x+1, currentPos.y+4, currentPos.z+3, block.AIR)
        elif (direction == 'e'):
            mc.setBlocks(currentPos.x+2, currentPos.y-1, currentPos.z-2, currentPos.x+3, currentPos.y+3, currentPos.z+2, block.AIR)
            mc.setBlocks(currentPos.x+2, currentPos.y+4, currentPos.z-1, currentPos.x+3, currentPos.y+4, currentPos.z+1, block.AIR)
        elif (direction == 'w'):
            mc.setBlocks(currentPos.x-2, currentPos.y-1, currentPos.z-2, currentPos.x-3, currentPos.y+3, currentPos.z+2, block.AIR)
            mc.setBlocks(currentPos.x-2, currentPos.y+4, currentPos.z-1, currentPos.x-3, currentPos.y+4, currentPos.z+1, block.AIR)
            
        
        startSize = len(queue)
        
        # main wall, 3m thick
        queue.append(Vec3(currentPos.x+1, currentPos.y-3, currentPos.z+1)) # conrer 1
        queue.append(Vec3(currentPos.x-1, min(currentPos.y-3, mc.getHeight(currentPos.x, currentPos.z)-3), currentPos.z-1)) # corner 2
        queue.append(block.MOSS_STONE) # block id
        
        # top of wall, 1 layer, 3m thick
        queue.append(Vec3(currentPos.x+2, currentPos.y-2, currentPos.z+2)) # corner 1
        queue.append(Vec3(currentPos.x-2, currentPos.y-2, currentPos.z-2)) # corner 2
        queue.append(block.STONE_BRICK) # block id
        
        # parapet
        if (parapetCounter % 2 == 0):
            parapetBlockId = block.STONE_BRICK
        else:
            parapetBlockId = block.TORCH
        parapetCounter += 1
        
        if (direction == 'n' or direction == 's'):
            queue.append(Vec3(currentPos.x-2, currentPos.y-1, currentPos.z))
            queue.append(Vec3(currentPos.x+2, currentPos.y-1, currentPos.z))
            queue.append(parapetBlockId)
        elif (direction == 'e' or direction == 'w'):
            queue.append(Vec3(currentPos.x, currentPos.y-1, currentPos.z-2))
            queue.append(Vec3(currentPos.x, currentPos.y-1, currentPos.z+2))
            queue.append(parapetBlockId)
        elif (direction == 'u' or direction == 'd'):
            queue.append(Vec3(currentPos.x, currentPos.y-1, currentPos.z-2))
            queue.append(Vec3(currentPos.x, currentPos.y-1, currentPos.z+2))
            queue.append(parapetBlockId)
            
        endSize = len(queue)
        itemsInQueuePerPosition = endSize - startSize
        if (len(queue) > (itemsInQueuePerPosition * minimumQueueSize)):
        
            # main wall
            corner1 = queue.popleft()
            corner2 = queue.popleft()
            blockId = queue.popleft()
            mc.setBlocks(corner1.x, corner1.y, corner1.z, corner2.x, corner2.y, corner2.z, blockId)
            
            # top of wall
            corner1 = queue.popleft()
            corner2 = queue.popleft()
            blockId = queue.popleft()
            mc.setBlocks(corner1.x, corner1.y, corner1.z, corner2.x, corner2.y, corner2.z, blockId)
            
            # parapet
            parapet1 = queue.popleft()
            parapet2 = queue.popleft()
            blockId = queue.popleft()
            mc.setBlock(parapet1.x, parapet1.y, parapet1.z, blockId)
            mc.setBlock(parapet2.x, parapet2.y, parapet2.z, blockId)
            
    previousPos = currentPos

