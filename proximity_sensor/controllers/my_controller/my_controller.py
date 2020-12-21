#team-ID = 55


from controller import Robot, Motor ,DistanceSensor
import math
import time
# create the Robot instance.
robot = Robot()
# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

#initializing the motors
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
ps = []

#setting constants
PI = math.pi
AXLE_LENGHT = 56
MAX_SPEED = 6.28
Sensor_names = ('ps0', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5', 'ps6', 'ps7')


#defining values for each movement
DIST_VARIABLE = (450,320,MAX_SPEED)
TURN_90_Degree = (704, 3.00199999999999999999999999999999999999999999999999999999999999999)
First_circle_radius = (150,1.64 * MAX_SPEED,4993,4850)
Second_circle_radius = (225,1.2 * MAX_SPEED,6450)
Third_circle_radius = (300,0.96 * MAX_SPEED,8300)

#defining functions
def BHAIBHAIBHAI():#to provide enough time to stabalize the robot
    robot.step(1)

def stop_robot():#to stop the robot
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

def move_xcm(time_move, SPEED):#to move in a straight line for x distance
    cmon = int(8 * time_move)
    leftMotor.setVelocity(SPEED)
    rightMotor.setVelocity(SPEED)
    robot.step(cmon)

def turn_c_degree(time_move, SPPED):#to turn clockwise
    leftMotor.setVelocity(SPPED)
    rightMotor.setVelocity(-SPPED)
    robot.step(time_move)

def turn_ac_degree(time_move, SPEED):#to turn anti-clockwise
    leftMotor.setVelocity(-SPEED)
    rightMotor.setVelocity(SPEED)
    robot.step(time_move)

def turn_C_RADI_degree(time_move, RADI,SPEED):#to follow the circle with radi x(clockwise)
    LEFT = ((PI*(RADI + (AXLE_LENGHT/2)))/1000)*SPEED
    RIGHT = ((PI*(RADI - (AXLE_LENGHT/2)))/1000)*SPEED
    leftMotor.setVelocity(LEFT)
    rightMotor.setVelocity(RIGHT)
    robot.step(time_move)

def turn_AC_RADI_degree(time_move, RADI,SPEED):#to follow the circle with radi x(anti-clockwise)
    LEFT = ((PI*(RADI - (AXLE_LENGHT/2)))/1000)*SPEED
    RIGHT = ((PI*(RADI + (AXLE_LENGHT/2)))/1000)*SPEED
    leftMotor.setVelocity(LEFT)
    rightMotor.setVelocity(RIGHT)
    robot.step(time_move)

def Distance_Of_DistanceSensor():
    Final_Distance_Sensor_Values = []
    Distance_Sensor_Values = []
    Temporary_Distance_Sensor_Values = []
    for i1 in range (len(Sensor_names)):
        Temporary_Distance_Sensor_Values.append(robot.getDistanceSensor(Sensor_names[i1]))
        Temporary_Distance_Sensor_Values[i1].enable(timestep)
    for i2 in range (len(Sensor_names)):
        Distance_Sensor_Values.append(Temporary_Distance_Sensor_Values[i2].getValue())
        Distance_Sensor_Values[i2] = float(Distance_Sensor_Values[i2])
    for i3 in range (len(Sensor_names)):
        if (Distance_Sensor_Values[i3]!=0):
            temp_value = ((1000 * (1 / Distance_Sensor_Values[i3])) - 10)
            if (temp_value>0):
                temp_value = int(((1000 * (1 / Distance_Sensor_Values[i3])) - 10))
            Final_Distance_Sensor_Values.append(temp_value)
        else:
            temp_value = ((Distance_Sensor_Values[i3]))
            Final_Distance_Sensor_Values.append(temp_value)
        if (Final_Distance_Sensor_Values[i3]>100):
            Final_Distance_Sensor_Values[i3] = 0
    print(Final_Distance_Sensor_Values)

#execution
"""
move_xcm(DIST_VARIABLE[0],DIST_VARIABLE[2])
BHAIBHAIBHAI()
turn_c_degree(TURN_90_Degree[0], TURN_90_Degree[1])
BHAIBHAIBHAI()
move_xcm(DIST_VARIABLE[1],DIST_VARIABLE[2])
turn_C_RADI_degree(First_circle_radius[2],First_circle_radius[0],First_circle_radius[1])
BHAIBHAIBHAI()
turn_C_RADI_degree(Second_circle_radius[2],Second_circle_radius[0],Second_circle_radius[1])
BHAIBHAIBHAI()
turn_C_RADI_degree(Third_circle_radius[2],Third_circle_radius[0],Third_circle_radius[1])
BHAIBHAIBHAI()
turn_C_RADI_degree(First_circle_radius[3],First_circle_radius[0],First_circle_radius[1])
BHAIBHAIBHAI()
move_xcm(DIST_VARIABLE[0],DIST_VARIABLE[2])
move_xcm(200,DIST_VARIABLE[2])
BHAIBHAIBHAI()
stop_robot()
"""
move_xcm(150,-DIST_VARIABLE[2])
for i in range(100):
    move_xcm(0.125,DIST_VARIABLE[2])
    Distance_Of_DistanceSensor()
BHAIBHAIBHAI()
stop_robot()