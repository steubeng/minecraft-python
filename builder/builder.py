from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
import random
import copy
import time

from house import house
from christmasTree import christmasTree
from maisonHouses import house1, house2, house3, house4, house5
from utils import getGroundHeight, circle

mc = Minecraft.create()
mc.postToChat("Builder!!!")

def commandList():
    print(' 0) EXIT')
    print(' 1) Christmas Tree')
    print(' 2) House-0')
    print(' 3) House-1')
    print(' 4) Bulldozer')
    print(' 5) 10x10 Village')
    print(' 6) House-2')
    print(' 7) Ground height here')
    print(' 8) House-3')
    print(' 9) House-4')
    print('10) Circle')
    print('11) House-5')
    
while(True):
    print()
    command = input('What do you want to build: ')
    pos = mc.player.getPos()
    pos.z += 5
    if (command == ''):
        commandList()
    elif (command == '0'):
        exit()
    elif (command == '1'):
        print('Let''s build a Christmas Tree!')
        christmasTree(mc, pos)
    elif (command == '2'):
        print('Let''s build a House!')
        width = int(input('How wide: '))
        length = int(input('How long: '))
        house(mc, pos, width, length)
    elif (command == '3'):
        house1(mc, pos)
    elif (command == '4'):
        mc.setBlocks(pos.x-200, pos.y, pos.z-200, pos.x+200, pos.y+35, pos.z+200, 0)
    elif (command == '5'):
        for x in range(10):
            housePos = copy.copy(pos)
            housePos.x += (10 * x)
            for z in range(10):
                housePos.z += 10
                houseStyle = random.randrange(5) + 1
                if (houseStyle == 1):
                    house1(mc, housePos)
                elif (houseStyle == 2):
                    house2(mc, housePos)
                elif (houseStyle == 3):
                    house3(mc, housePos)
                elif (houseStyle == 4):
                    house4(mc, housePos)
                elif (houseStyle == 5):
                    house5(mc, housePos)
                time.sleep(1)
    elif (command == '6'):
        house2(mc, pos)
    elif (command == '7'):
        here = copy.copy(pos)
        here.z -= 5
        print(getGroundHeight(mc, here))
    elif (command == '8'):
        house3(mc, pos)
    elif (command == '9'):
        house4(mc, pos)
    elif (command == '10'):
        circle(mc, pos, 10)
    elif (command == '11'):
        house5(mc, pos)
    else:
        print('That option is not supported yet:', command)
        
#   I   LOVE    DAddY.        

