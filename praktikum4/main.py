import numpy as np
import cv2 as cv2
from OmniCore import OmniCore

robot = OmniCore("192.168.125.1")

robot.moveAbsJ([17, 79, -10, -74, -84, -72])
robot.moveL([375, 320, 105], [0.707107, -0.707107, 0.000000, 0.000000], [0, -1, -1, 1])

basePosition = [375, 320, 55]
robot.moveL(basePosition, [0.707107, -0.707107, 0.000000, 0.000000], [0, -1, -1, 1])

image = cv2.imread("./images/winterthur.png", cv2.IMREAD_GRAYSCALE)

height, width = image.shape[:2]

for i in np.arange(0, height, 6):


    upPosition1 = [basePosition[0]+i*0.2, basePosition[1], basePosition[2]+4]
    robot.moveL(upPosition1, [0.707107, -0.707107, 0.000000, 0.000000], [0, -1, -1, 1])

    for j in np.arange(0, width, 6):
        pixel = image[i, j]

        skip = True
        for testPixel in image[i, j:width]:
            if testPixel < 200:
                skip = False

        downPosition = [basePosition[0]+i*0.2, basePosition[1]+j*0.2, basePosition[2]]
        upPosition = [downPosition[0], downPosition[1], downPosition[2] + 4]

        if skip:
            robot.moveL(upPosition, [0.707107, -0.707107, 0.000000, 0.000000], [0, -1, -1, 1])
            break

        if pixel < 200:
            robot.moveL(downPosition, [0.707107, -0.707107, 0.000000, 0.000000], [0, -1, -1, 1])
        else:
            robot.moveL(upPosition, [0.707107, -0.707107, 0.000000, 0.000000], [0, -1, -1, 1])

    upPosition2 = [basePosition[0]+i*0.2, basePosition[1]+width*0.2, basePosition[2]+4]
    robot.moveL(upPosition2, [0.707107, -0.707107, 0.000000, 0.000000], [0, -1, -1, 1])


del robot