from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
import random

mc = Minecraft.create()
mc.postToChat("House time!!!")
pos = mc.player.getPos()

mc.setBlock(pos.x-3, pos.y+0, pos.z-1, 201)
mc.setBlock(pos.x-4, pos.y+0, pos.z-1, 24)
mc.setBlock(pos.x-4, pos.y+0, pos.z-2, 4)
mc.setBlock(pos.x-4, pos.y+0, pos.z-2, 4)
mc.setBlock(pos.x-3, pos.y+0, pos.z-2, 211)
mc.setBlock(pos.x-3, pos.y+0, pos.z-3, 2)
mc.setBlock(pos.x-4, pos.y+0, pos.z-3, 24)
mc.setBlock(pos.x+2, pos.y+0, pos.z-1, 201)
mc.setBlock(pos.x-2, pos.y+0, pos.z-1, 41)
