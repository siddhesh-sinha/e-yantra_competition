#team-ID = 55 (sudo)


from controller import Robot, Motor
import math
import time
# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function.
# In order to get the instance the left motor of the robot. Something like:
# left_motor = robot.getMotor('left wheel motor')

##### HERE, WRITE THE CODE that you want to run only once in a sequential manner ##############
#definitions
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
MAX_SPEED = 6.28
Dist_Speed = MAX_SPEED * 1
Rot_Speed = 3
leftSpeed = 1.0
rightSpeed = 1.0
#functions
def move_xcm(x):
	leftMotor.setVelocity(Dist_Speed)
	rightMotor.setVelocity(Dist_Speed)
	robot.step(x)
	leftMotor.setVelocity(0)
	rightMotor.setVelocity(0)


def turn_90():
	leftMotor.setVelocity(Rot_Speed)
	rightMotor.setVelocity(-Rot_Speed)
	robot.step(707)
	leftMotor.setVelocity(0)
	rightMotor.setVelocity(0)


def turn_xyz(x, y, z):
	leftMotor.setVelocity(x)
	rightMotor.setVelocity(y)
	robot.step(z)
	leftMotor.setVelocity(0)
	rightMotor.setVelocity(0)
#execution

move_xcm(3555)
turn_90()
move_xcm(2500)
turn_xyz(3,2.05,9400)
turn_xyz(4.5,3.48,8800)
turn_xyz(3,2.48,17000)
turn_xyz(3,2.05,9400)
move_xcm(4000)

##############################################################################################

# Main loop:
# - perform simulation steps until Webots is stopping the controller
#while robot.step(timestep) != -1:
#	pass
##### HERE, write the code that you want to be executed repeatedly, in a loop #############################
###########################################################################################################
