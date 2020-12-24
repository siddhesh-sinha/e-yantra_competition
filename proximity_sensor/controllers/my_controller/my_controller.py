#team-ID = 55


from controller import Robot, Motor ,DistanceSensor
import math
import function_file as ff
import time

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
for yoooooooo in range(1000):
    ff.ChEcK_ObStAcLe(3,40)
ff.stop_robot()