from controller import Robot, DistanceSensor, Motor
from controller import Camera
from vehicle import Driver
import cv2
import numpy

TIMESTEP = 16 #timestep = int(driver.getBasicTimeStep())
MAX_SPEED = 6.28
robot = Robot()

# Initialize Camera
camera = Camera('camera')
camera.enable(TIMESTEP)
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftSpeed = 0.0
rightSpeed = 0.0
leftMotor.setVelocity(leftSpeed)
rightMotor.setVelocity(rightSpeed)

while robot.step(TIMESTEP) != -1:
    data = camera.getImage()
    frame = numpy.frombuffer(data, numpy.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
