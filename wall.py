from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
import random

mc = Minecraft.create()
mc.postToChat("Wall mode!!!")

previousPw
while(True):
    currentPos = mc.player.getTilePos()
    if (previousPos.x != currentPos.x or previousPos.y != currentPos.y or previousPos.z != currentPos.z):
        print(currentPos)
        mc.setBlocks(currentPos.x+1, currentPos.y-2, currentPos.z+1, currentPos.x-1, mc.getHeight(currentPos.x, currentPos.z)-1, currentPos.z-1, 45)
    previousPos = currentPos

