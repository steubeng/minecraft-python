from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
from collections import deque
from mcpi import block

mc = Minecraft.create()
mc.postToChat("Wall mode!!!")
queue = deque([])
itemsInQueuePerPosition = 6
minimumQueueSize = 2

previousPos = mc.player.getTilePos()
while(True):
    currentPos = mc.player.getTilePos()
    if (previousPos.x != currentPos.x or previousPos.y != currentPos.y or previousPos.z != currentPos.z):
        print(currentPos)
        queue.append(Vec3(currentPos.x+1, currentPos.y-3, currentPos.z+1)) # corer 1
        queue.append(Vec3(currentPos.x-1, mc.getHeight(currentPos.x, currentPos.z)-3, currentPos.z-1)) # corner 2
        queue.append(block.MOSS_STONE) # block id
        queue.append(Vec3(currentPos.x+2, currentPos.y-2, currentPos.z+2)) # corer 1
        queue.append(Vec3(currentPos.x-2, currentPos.y-2, currentPos.z-2)) # corner 2
        queue.append(block.STONE_BRICK) # block id
        if (len(queue) > (itemsInQueuePerPosition * minimumQueueSize)):
            corner1 = queue.popleft()
            corner2 = queue.popleft()
            blockId = queue.popleft()
            mc.setBlocks(corner1.x, corner1.y, corner1.z, corner2.x, corner2.y, corner2.z, blockId)
            corner1 = queue.popleft()
            corner2 = queue.popleft()
            blockId = queue.popleft()
            mc.setBlocks(corner1.x, corner1.y, corner1.z, corner2.x, corner2.y, corner2.z, blockId)
            #mc.setBlocks(currentPos.x+2, currentPos.y-2, currentPos.z+2, currentPos.x-2, mc.getHeight(currentPos.x, currentPos.z)-2, currentPos.z-2, 45)
    previousPos = currentPos

