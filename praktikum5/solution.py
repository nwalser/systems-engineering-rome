import OmniCore
from OmniCore import OmniCore
import positions

TOOL_RELEASE = True
TOOL_CLAMP = False

AIR_ENABLE = False
AIR_DISABLE = True

GRIPPER_CLOSE = True
GRIPPER_OPEN = False


robot = OmniCore("192.168.125.1")

robot.moveJ(*positions.position1)
robot.moveJ(*positions.position2)
robot.moveJ(*positions.position3)
robot.moveJ(*positions.position4)
robot.moveJ(*positions.position5)

del robot
input()
