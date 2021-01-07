"""e-puck controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot, DistanceSensor, Motor
import math
import threading
import time
# create the Robot instance.
robot = Robot()

# get the time step of the current world.
timestep = 16
MAX_SPEED = 6.28
v =  1*MAX_SPEED
dist_sensor_max = 255
L = 52 # axle length in mm
R = 20 # wheel radius in mm

#Initialising motors
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

#Initialising Encoders
left_encoder = robot.getPositionSensor('left wheel sensor')
left_encoder.enable(timestep)
right_encoder = robot.getPositionSensor('right wheel sensor')
right_encoder.enable(timestep)

pi=math.pi

class Tick():

    ang=0

    def setTicks():
        while True:
            #distance = (left_encoder_ticks + right_encoder_ticks) * R / 2
            left_encoder_ticks = left_encoder.getValue()
            right_encoder_ticks = right_encoder.getValue()
            angle = ((left_encoder_ticks - right_encoder_ticks) * R / L) % (2*pi)
            Tick.ang=angle*(180/pi)
            #print(str(Tick.ang)+" degrees")

    def angle():
        return Tick.ang

threading.Thread(target=Tick.setTicks).start()

#Initialising Proximity Sensors
psNames = [
    'ps0', 'ps1', 'ps2', 'ps3',
    'ps4', 'ps5', 'ps6', 'ps7'
]
ps = []
for i in range(8):
    ps.append(robot.getDistanceSensor(psNames[i]))
    ps[i].enable(timestep)

#GO STRAIGHT
def go_straight(t): 
    leftMotor.setVelocity(v)
    rightMotor.setVelocity(v)
    robot.step(int(t))

#GO RIGHT
def soft_right(t):
    leftMotor.setVelocity(v)
    rightMotor.setVelocity(-v)
    robot.step(int(t))

#GO LEFT
def soft_left(t):
    leftMotor.setVelocity(-v)
    rightMotor.setVelocity(v)
    robot.step(int(t))

def a_range(r, t, var):
    if r==t:
        #print(True)
        return True
    else:
        inR=False
        for i in range(var):
            x=r+i
            y=r-i
            if(x>360):
                x=x-360
            if(y<0):
                x=y+360
            if(x==t or y==t):
                inR=True
                break
            
        print(inR, r, t)
        return inR

def setDir(a):
    accuracy=20
    if(Tick.angle()>a):
        #print('A=',a)
        while(a_range(a, round(Tick.angle()), accuracy)==False):
            soft_left(2)
    elif(Tick.angle()<a):
        #print('A=',a)
        while(a_range(a, round(Tick.angle()), accuracy)==False):
            soft_right(2)
    else:
        pass

forTime=0
prevSt=False

while robot.step(timestep) != -1:

    psValues = []

    minVal=60
    
    for i in range(8):
        psValues.append(ps[i].getValue())

    if psValues[0] >= minVal:
        forTime=0
        prevSt=False
        soft_left(30)

    elif psValues[7]>= minVal:
        forTime=0
        prevSt=False
        soft_right(30)
        
    elif psValues[1] >= minVal or psValues[2]>= minVal:
        forTime=0
        prevSt=False
        soft_left(30)
        
    elif psValues[5] >= minVal or psValues[6]>= minVal:
        forTime=0
        prevSt=False
        soft_right(30)
        
    else:
        forTime+=1
        go_straight(100)
    if(forTime>10 and prevSt==False and a_range(0, round(Tick.angle()), 20)==False):
        prevSt=True
        print(forTime)
        setDir(0)
        forTime=0
