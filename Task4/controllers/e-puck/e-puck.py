from controller import Robot, Motor
from controller import Camera
import cv2
import numpy as np
import math

timestep = 32
MAX_SPEED = 6.28
w = 0.75 * MAX_SPEED  # You can tweak it if you want
R = 20.5  # In mm

robot = Robot()

# Use this to get image from the camera using getImage Function
camera = Camera('camera')
camera.enable(timestep)

leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)


# Remember to put actual argument names in place  of arg1 arg2, you can have more or less than 2 arguments
def color_detection(arg1, arg2):
    """
    Write your color detection code here
    """
    return


# Remember to put actual argument names in place  of arg1 arg2, you can have more or less  than 2 arguments
def shape_detection(arg1, arg2):
    """
    Write your shape detection code here
    """
    return


def move_epuck(shape, color):  # You may have different arguments in your code
    """
    Write your actuator code here
    """
    return


###################################################
# Here write the code you want to execute just once
##################################################

while robot.step(timestep) != -1:
    frame = camera.getImage()
    # img contains the image obtained from the camera, use this to write rest of your code
    img = np.frombuffer(frame, np.uint8).reshape(
        (camera.getHeight(), camera.getWidth(), 4))
    # DO NOT MODIFY THE ABOVE 2 LINES
    ##############################################
    # Here write code you want to execute repeatedly
    # Remember to pass the necessary arguments as defined in the function definition
    color = color_detection()
    # Remember to pass the necessary arguments as defined in the function definition
    shape = shape_detection()
    move_epuck(shape, color)
    ###############################################
