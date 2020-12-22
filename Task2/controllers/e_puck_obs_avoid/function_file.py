from controller import Robot, Motor ,DistanceSensor
import math
# create the Robot instance.
robot = Robot()
# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

#initializing the motors
leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))

#setting constants
PI = math.pi
AXLE_LENGHT = 56
MAX_SPEED = 6.28
Sensor_names = ('ps0', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5', 'ps6', 'ps7')
Sensor_Set_1 = {0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7}
Sensor_Set_2 = {0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7}
Sensor_Set_3 = {0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7}
Sensor_Set_4 = {0:0,1:1,2:2,3:3,4:4,5:5,6:6,7:7}

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

def smul_C_turn(Turn_Amount,SPEED,TIME):
    Velocity_Reduction = ((Turn_Amount/100)*SPEED)
    LEFT = SPEED-Velocity_Reduction
    RIGHT = SPEED
    leftMotor.setVelocity(LEFT)
    rightMotor.setVelocity(RIGHT)
    robot.step(TIME)

def smul_AC_turn(Turn_Amount,SPEED,TIME):
    Velocity_Reduction = ((Turn_Amount/100)*SPEED)
    RIGHT = SPEED-Velocity_Reduction
    LEFT = SPEED
    leftMotor.setVelocity(LEFT)
    rightMotor.setVelocity(RIGHT)
    robot.step(TIME)

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
            temp_value = ((1000 * (1 / Distance_Sensor_Values[i3])) - 6)
            if (temp_value>0):
                temp_value = int(((1000 * (1 / Distance_Sensor_Values[i3])) - 5))
            if (temp_value<0):
                temp_value = int(((1000 * (1 / Distance_Sensor_Values[i3])) - 5))
        else:
            temp_value = ((Distance_Sensor_Values[i3]))
        Final_Distance_Sensor_Values.append(temp_value)
        if (Final_Distance_Sensor_Values[i3]>50):
            Final_Distance_Sensor_Values[i3] = 0
    output = Final_Distance_Sensor_Values
    return output

def CHEcK_SENsoR_DiStAnCe(Sensor_Number):
    x = Distance_Of_DistanceSensor()
    output = x[Sensor_Number]
    return output

def SeT_SeNsOr_SeT_1(Sensor_vlaues):
    output = []
    temp_value_1 = 0
    for i in range (8):
        if (Sensor_vlaues[i]!=0):
            temp_value_1 = Sensor_vlaues[i]
            if (Sensor_vlaues[i]>0):
                temp_value_1 = int(Sensor_vlaues[i])
            if (Sensor_vlaues[i]<0):
                temp_value_1 = int(Sensor_vlaues[i])
        else:
            temp_value_1 = Sensor_vlaues[i]
        output.append(temp_value_1)

    return output
def SeT_SeNsOr_SeT_2(Sensor_vlaues):
    output = []
    Altered_Sensor_vlaues = []
    temp_value_1 = 0
    for i in range (8):
        Altered_Sensor_vlaues.append((Sensor_vlaues[i]+Sensor_vlaues[i-1])/2)
        if (Altered_Sensor_vlaues[i]!=0):
            temp_value_1 = Altered_Sensor_vlaues[i]
            if (Altered_Sensor_vlaues[i]>0):
                temp_value_1 = int(Altered_Sensor_vlaues[i])
            if (Altered_Sensor_vlaues[i]<0):
                temp_value_1 = int(Altered_Sensor_vlaues[i])
        else:
            temp_value_1 = Altered_Sensor_vlaues[i]
        output.append(temp_value_1)
    return output
def SeT_SeNsOr_SeT_3(Sensor_vlaues):
    output = []
    Altered_Sensor_vlaues = []
    temp_value_1 = 0
    for i in range (8):
        Altered_Sensor_vlaues.append((Sensor_vlaues[i]+Sensor_vlaues[i-1]+Sensor_vlaues[i-2]+Sensor_vlaues[i-3])/4)
        if (Altered_Sensor_vlaues[i]!=0):
            temp_value_1 = Altered_Sensor_vlaues[i]
            if (Altered_Sensor_vlaues[i]>0):
                temp_value_1 = int(Altered_Sensor_vlaues[i])
            if (Altered_Sensor_vlaues[i]<0):
                temp_value_1 = int(Altered_Sensor_vlaues[i])
        else:
            temp_value_1 = Altered_Sensor_vlaues[i]
        output.append(temp_value_1)
    return output
def SeT_SeNsOr_SeT_4(Sensor_vlaues):
    output = []
    Altered_Sensor_vlaues = []
    temp_value_1 = 0
    for i in range (8):
        Altered_Sensor_vlaues.append((Sensor_vlaues[i]+Sensor_vlaues[i-1]+Sensor_vlaues[i-2]+Sensor_vlaues[i-3]+Sensor_vlaues[i-4]+Sensor_vlaues[i-5]+Sensor_vlaues[i-6]+Sensor_vlaues[i-7])/8)
        if (Altered_Sensor_vlaues[i]!=0):
            temp_value_1 = Altered_Sensor_vlaues[i]
            if (Altered_Sensor_vlaues[i]>0):
                temp_value_1 = (Altered_Sensor_vlaues[i])
            if (Altered_Sensor_vlaues[i]<0):
                temp_value_1 = (Altered_Sensor_vlaues[i])
        else:
            temp_value_1 = Altered_Sensor_vlaues[i]
        output.append(temp_value_1)
    return output

def set_Dictionary_variables()