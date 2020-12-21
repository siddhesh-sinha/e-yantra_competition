# TEAM-55 (SUDO)
# DOCUMENTED

#                               START

#importing required packages
from controller import Robot, Motor
import math

# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# initialize motors
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)

MAX_SPEED = 6.28 # Maximum angular velocity of wheels

v = 1 * MAX_SPEED # Variable for controlling angular velocity of wheel

R=20.5 # Radius of wheel (un-modified)

A=29 # Axle length (modified to fulfil needs)

pi=math.pi

# Drive Control Code

def go_straight(len):
    t=len/(v*R)
    leftMotor.setVelocity(v)
    rightMotor.setVelocity(v)
    robot.step(int(t*1000))
    
def soft_right(t):
    leftMotor.setVelocity(v)
    rightMotor.setVelocity(0)
    robot.step(int(t))

def semi_cir_1():

    r1=150

    vr=v*(r1-A)/1000 * 5.2
    vl=v*(r1+A)/1000 * 5.2
    vm=(vl+vr)/2
    t1=((r1/(R*vm))*pi)

    if(vr>v):
        vr=v
    if(vl>v):
        vl=v

    leftMotor.setVelocity(vl)
    rightMotor.setVelocity(vr)

    robot.step(int(t1*1000))

    pass

def semi_cir_2():

    r2=225

    vr=(v*(r2-A)/1000 * 4)
    vl=(v*(r2+A)/1000 * 4)
    vm=(vl+vr)/2
    t2=((r2/(R*vm))*pi)

    if(vr>v):
        vr=v
    if(vl>v):
        vl=v
    
    leftMotor.setVelocity(vl)
    rightMotor.setVelocity(vr)

    robot.step(int(t2*1000))

    pass

def semi_cir_3():

    r3=300

    vr=v*(r3-A)/1000 * 3
    vl=v*(r3+A)/1000 * 3
    vm=(vl+vr)/2
    t3=((r3/(R*vm))*pi)+0.85

    if(vr>v):
        vr=v
    if(vl>v):
        vl=v

    leftMotor.setVelocity(vl)
    rightMotor.setVelocity(vr)


    robot.step(int(t3*1000))

    pass

def semi_cir_4():

    r4=150

    vr=v*(r4-A)/1000 * 5
    vl=v*(r4+A)/1000 * 5
    vm=(vl+vr)/2
    t4=((r4/(R*vm))*pi)

    if(vr>v):
        vr=v
    if(vl>v):
        vl=v

    leftMotor.setVelocity(vl)
    rightMotor.setVelocity(vr)

    robot.step(int(t4*1000))

    pass

# vl - velocity of left wheel
# vr - velocity of right wheel
# vm - velocity of imaginary wheel in the middle of the axle
# t  - time required for a particular part of course
# r1, r2, r3, r4 - radius of each of the semi-circular courses respectively

# FOLLOW COURSE (function calls)
go_straight(430) #argument in mm
soft_right(2340) #argument in miliseconds
go_straight(280) #argument in mm
semi_cir_1() # semi-circular course 1
semi_cir_2() # semi-circular course 2
semi_cir_3() # semi-circular course 3
semi_cir_4() # semi-circular course 4
go_straight(430) #argument in mm

# STOP COURSE
leftMotor.setVelocity(0) #argument in rad/sec
rightMotor.setVelocity(0) #argument in rad/sec

#                                END