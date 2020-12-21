"""
from controller import Robot, Motor
import math
# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function.
# In order to get the instance the left motor of the robot. Something like:
# left_motor = robot.getMotor('left wheel motor')

##### HERE, WRITE THE CODE that you want to run only once in a sequential manner ##############

# initialize motors
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)

MAX_SPEED = 6.28

#v = 0.75 * MAX_SPEED 
v = 1 * MAX_SPEED 

R=20.5

A=29

pi=math.pi

def stop():
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

def go_straight(len):
    t=len/(v*R)
    leftMotor.setVelocity(v)
    rightMotor.setVelocity(v)
    robot.step(int(t*1000))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

    
def soft_right(t):
    leftMotor.setVelocity(v)
    rightMotor.setVelocity(0)
    robot.step(int(t))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

def soft_left(t):
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(v)
    robot.step(int(t))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

def cir_1():
    r1=150

    vr=v*(r1-A)/1000 * 4
    vl=v*(r1+A)/1000 * 4
    vm=(vl+vr)/2
    t1=((r1/(R*vm))*pi)

    leftMotor.setVelocity(vl)
    rightMotor.setVelocity(vr)

    robot.step(int(t1*1000))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

    pass

def cir_2():
    r2=225

    vr=(v*(r2-A)/1000 * 4)
    vl=(v*(r2+A)/1000 * 4)
    vm=(vl+vr)/2
    t2=((r2/(R*vm))*pi)
    
    leftMotor.setVelocity(vl)
    rightMotor.setVelocity(vr)

    robot.step(int(t2*1000))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

    pass

def cir_3():
    r3=300

    vr=v*(r3-A)/1000 * 3
    vl=v*(r3+A)/1000 * 3
    vm=(vl+vr)/2
    t3=((r3/(R*vm))*pi)

    leftMotor.setVelocity(vl)
    rightMotor.setVelocity(vr)


    robot.step(int(t3*1000))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

    pass

def cir_4():
    r4=150

    vr=v*(r4-A)/1000 * 4
    vl=v*(r4+A)/1000 * 4
    vm=(vl+vr)/2
    t4=((r4/(R*vm))*pi + 0.2)

    leftMotor.setVelocity(vl)
    rightMotor.setVelocity(vr)

    robot.step(int(t4*1000))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

    pass


go_straight(430)
stop()
soft_right(2340)
stop()
go_straight(280)
stop()

cir_1()
stop()
cir_2()
stop()
cir_3()
stop()
cir_4()
stop()

go_straight(430)
stop()
"""
from controller import Robot, Motor
import math
# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

# You should insert a getDevice-like function.
# In order to get the instance the left motor of the robot. Something like:
# left_motor = robot.getMotor('left wheel motor')

##### HERE, WRITE THE CODE that you want to run only once in a sequential manner ##############

# initialize motors
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0)
rightMotor.setVelocity(0)

MAX_SPEED = 6.28

#v = 0.75 * MAX_SPEED 
v = 1 * MAX_SPEED 

R=20.5

A=29

pi=math.pi

def stop():
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

def go_straight(len):
    t=len/(v*R)
    leftMotor.setVelocity(v)
    rightMotor.setVelocity(v)
    robot.step(int(t*1000))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

    
def soft_right(t):
    leftMotor.setVelocity(v)
    rightMotor.setVelocity(0)
    robot.step(int(t))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

def soft_left(t):
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(v)
    robot.step(int(t))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

def cir_1():
    r1=150

    vr=v*(r1-A)/1000 * 4
    vl=v*(r1+A)/1000 * 4
    vm=(vl+vr)/2
    t1=((r1/(R*vm))*pi)

    if(vr>v):
        vr=v
    if(vl>v):
        vl=v

    leftMotor.setVelocity(vl)
    rightMotor.setVelocity(vr)

    robot.step(int(t1*1000))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

    pass

def cir_2():
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
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

    pass

def cir_3():
    r3=300

    vr=v*(r3-A)/1000 * 3
    vl=v*(r3+A)/1000 * 3
    vm=(vl+vr)/2
    t3=((r3/(R*vm))*pi)

    if(vr>v):
        vr=v
    if(vl>v):
        vl=v

    leftMotor.setVelocity(vl)
    rightMotor.setVelocity(vr)


    robot.step(int(t3*1000))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

    pass

def cir_4():
    r4=150

    vr=v*(r4-A)/1000 * 4
    vl=v*(r4+A)/1000 * 4
    vm=(vl+vr)/2
    t4=((r4/(R*vm))*pi + 0.2)

    if(vr>v):
        vr=v
    if(vl>v):
        vl=v

    leftMotor.setVelocity(vl)
    rightMotor.setVelocity(vr)

    robot.step(int(t4*1000))
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)

    pass


go_straight(430)
stop()
soft_right(2340)
stop()
go_straight(280)
stop()

cir_1()
stop()
cir_2()
stop()
cir_3()
stop()
cir_4()
stop()

go_straight(430)
stop()