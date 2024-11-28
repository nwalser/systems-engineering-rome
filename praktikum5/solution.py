import math
import time
from OmniCore import OmniCore
import positions

TOOL_RELEASE = True
TOOL_CLAMP = False

AIR_ENABLE = False
AIR_DISABLE = True

GRIPPER_CLOSE = True
GRIPPER_OPEN = False

params = [[0, -math.sqrt(2)/2, -math.sqrt(2)/2, 0],
          [15, 40, 15, 0, 35, 15],
          7000, 0]

toolSwitch1Down = [[54.24, -452.62, -80.58], *params]
toolSwitch1Up = [[54.24, -452.62, 0.0], *params]
toolSwitch2Down = [[-50.5, -452.62, -80.58], *params]
toolSwitch2Up = [[-50.5, -452.62, 0.0], *params]

tool1 = [toolSwitch1Up, toolSwitch1Down]
tool2 = [toolSwitch2Up, toolSwitch2Down]


def release_tool(upPos, downPos):
    robot.moveJ(*upPos)

    robot.moveL(*downPos)
    robot.air(AIR_ENABLE)
    robot.tool(TOOL_RELEASE)
    time.sleep(0.5)
    robot.moveL(*upPos)
    robot.air(AIR_DISABLE)


def load_tool(upPos, downPos):
    robot.moveJ(*upPos)
    robot.air(AIR_ENABLE)
    robot.tool(TOOL_RELEASE)
    time.sleep(0.5)
    robot.moveL(*downPos)
    robot.tool(TOOL_CLAMP)
    time.sleep(0.5)
    robot.air(AIR_DISABLE)

    robot.moveL(*upPos)


robot = OmniCore("192.168.125.1")

robot.home()

input()
while True:
    #load_tool(*tool1)
    robot.moveJ([350,120,-30], [0,0,1,0], [0,90,0,0,5,0], 7000, 0)

    for i in range(10):
        robot.egmMoveL([515,-90,42], [[0,0,1],[1,0,0],[0,1,0]],
        [0,90,0,0,5,0], 7000, 0)
        robot.egmMoveL([515,120,42], [[0,0,1],[1,0,0],[0,1,0]],
        [0,90,0,0,5,0], 7000, 0)

    #release_tool(*tool1)
    input()


del robot
input()
