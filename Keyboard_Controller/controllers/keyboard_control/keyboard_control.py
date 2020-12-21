"""my_controller controller."""

#team ID : 55-Sudo

# You may need to import some classes of the controller module. Ex:
from controller import Robot, Motor, DistanceSensor
from controller import Robot, Motor, Keyboard
from controller import Robot

# create the Robot instance.
robot = Robot()

#initialize keyboard
keyboard = Keyboard()
keyboard.enable(50)

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# time in [ms] of a simulation step
timestep = int(robot.getBasicTimeStep())
MAX_SPEED = 2
MAX_SPEED_MOTION = 6.28

# initialize motors
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftSpeed = 0.0
rightSpeed = 0.0
leftMotor.setVelocity(leftSpeed)
rightMotor.setVelocity(rightSpeed)

# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getMotor('motorname')
#  ds = robot.getDistanceSensor('dsname')
#  ds.enable(timestep)

# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    k = keyboard.getKey()
     
    if k == ord('F'):
        print('forward')
        leftSpeed  = MAX_SPEED_MOTION
        rightSpeed = MAX_SPEED_MOTION

    elif k == ord('R'):
        print("Turn Right")
        leftSpeed  = MAX_SPEED
        rightSpeed = -MAX_SPEED
        
    elif k == ord('L'): 
        print("Turn Left")
        leftSpeed  = -MAX_SPEED
        rightSpeed = MAX_SPEED
    
    elif k == ord('S'):
        print("Stop")
        leftSpeed   = 0
        rightSpeed  = 0

    # write actuators inputs
    leftMotor.setVelocity(leftSpeed)
    rightMotor.setVelocity(rightSpeed)

    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass

# Enter here exit cleanup code.
