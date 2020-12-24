from controller import Robot, Motor ,DistanceSensor
import math
import asyncio
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

#defining values for each movement
DIST_VARIABLE = (450,320,MAX_SPEED)
TURN_90_Degree = (704, 3.00199999999999999999999999999999999999999999999999999999999999999)
First_circle_radius = (150,1.64 * MAX_SPEED,4993,4850)
Second_circle_radius = (225,1.2 * MAX_SPEED,6450)
Third_circle_radius = (300,0.96 * MAX_SPEED,8300)

#defining syyc functions
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
                temp_value = int(((1000 * (1 / Distance_Sensor_Values[i3])) - 6))
            if (temp_value<0):
                temp_value = int(((1000 * (1 / Distance_Sensor_Values[i3])) - 6))
        else:
            temp_value = ((Distance_Sensor_Values[i3]))
        Final_Distance_Sensor_Values.append(temp_value)
        if (Final_Distance_Sensor_Values[i3]>45):
            Final_Distance_Sensor_Values[i3] = 0.0
    output = Final_Distance_Sensor_Values
    return output

def CHEcK_SENsoR_DiStAnCe(Sensor_Number):
    x = Distance_Of_DistanceSensor()
    output = x[Sensor_Number]
    return output

def SeT_SeNsOr_SeT_1(Sensor_vlaues):
    output = {}
    output_temp = []
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
        output_temp.append(temp_value_1)
    for i in range (8):
        output[i] = output_temp[i]
    return output

def SeT_SeNsOr_SeT_2(Sensor_vlaues):
    output = {}
    output_temp = []
    Altered_Sensor_vlaues = []
    temp_value_1 = 0
    x = 0
    for i in range (4):
        Altered_Sensor_vlaues.append((Sensor_vlaues[x]+Sensor_vlaues[x-1])/2)
        if (Altered_Sensor_vlaues[i]!=0):
            temp_value_1 = Altered_Sensor_vlaues[i]
            if (Altered_Sensor_vlaues[i]>0):
                temp_value_1 = (Altered_Sensor_vlaues[i])
            if (Altered_Sensor_vlaues[i]<0):
                temp_value_1 = (Altered_Sensor_vlaues[i])
        else:
            temp_value_1 = Altered_Sensor_vlaues[i]
        output_temp.append(temp_value_1)
        x += 2
    for i in range (4):
        output[i] = output_temp[i]
    return output

def SeT_SeNsOr_SeT_3(Sensor_vlaues):
    output = {}
    output_temp = []
    Altered_Sensor_vlaues = []
    temp_value_1 = 0
    x = 0
    for i in range (2):
        Altered_Sensor_vlaues.append((Sensor_vlaues[x]+Sensor_vlaues[x+1]+Sensor_vlaues[x+2]+Sensor_vlaues[x+3])/4)
        if (Altered_Sensor_vlaues[i]!=0):
            temp_value_1 = Altered_Sensor_vlaues[i]
            if (Altered_Sensor_vlaues[i]>0):
                temp_value_1 = (Altered_Sensor_vlaues[i])
            if (Altered_Sensor_vlaues[i]<0):
                temp_value_1 = (Altered_Sensor_vlaues[i])
        else:
            temp_value_1 = Altered_Sensor_vlaues[i]
        output_temp.append(temp_value_1)
        x += 4
    for i in range (2):
        output[i] = output_temp[i]
    return output

def SeT_SeNsOr_SeT_4(Sensor_vlaues):
    output = {}
    output_temp = []
    Altered_Sensor_vlaues = []
    temp_value_1 = 0
    x=0
    for i in range (1):
        Altered_Sensor_vlaues.append((Sensor_vlaues[x]+Sensor_vlaues[x-1]+Sensor_vlaues[x-2]+Sensor_vlaues[x-3]+Sensor_vlaues[x-4]+Sensor_vlaues[x-5]+Sensor_vlaues[x-6]+Sensor_vlaues[x-7])/8)
        if (Altered_Sensor_vlaues[i]!=0):
            temp_value_1 = Altered_Sensor_vlaues[i]
            if (Altered_Sensor_vlaues[i]>0):
                temp_value_1 = (Altered_Sensor_vlaues[i])
            if (Altered_Sensor_vlaues[i]<0):
                temp_value_1 = (Altered_Sensor_vlaues[i])
        else:
            temp_value_1 = Altered_Sensor_vlaues[i]
        output_temp.append(temp_value_1)
    for i in range (1):
        output[i] = output_temp[i]
    return output

def SeTs_VaLuEs_1():
    Sensor_Set_1 = SeT_SeNsOr_SeT_1(Distance_Of_DistanceSensor())
    return Sensor_Set_1

def SeTs_VaLuEs_2():
    Sensor_Set_2 = SeT_SeNsOr_SeT_2(Distance_Of_DistanceSensor())
    return Sensor_Set_2

def SeTs_VaLuEs_3():
    Sensor_Set_3 = SeT_SeNsOr_SeT_3(Distance_Of_DistanceSensor())
    return Sensor_Set_3

def SeTs_VaLuEs_4():
    Sensor_Set_4 = SeT_SeNsOr_SeT_4(Distance_Of_DistanceSensor())
    return Sensor_Set_4

def ChEcK_PaRaMeTeR(Value,threshhold):
    Value_count = len(Value)
    x = {}
    for i in range (Value_count):
        if (Value[i]<threshhold and Value[i]>0):
            x[i] = 1
        else:
            x[i] = 0
    return x
#defining asyyc functions
async def AsYnC_SeNsOr_If(v):
    asyncio.sleep(0.0000000000000001)
    x = ChEcK_PaRaMeTeR(SeTs_VaLuEs_1(),40)
    if(v == -1):
        v = 7
    if (x[v] == 1):
        print("issue@",v)
async def execution_StEp_3_indivigual(indivigual):
    asyncio.sleep(0.0000000000000001)
    module = ChEcK_PaRaMeTeR(SeTs_VaLuEs_2(),40)
    distinguisher_1 = indivigual*2
    distinguisher_2 = distinguisher_1-1
    if(module[indivigual]==1):
        await asyncio.gather(
        AsYnC_SeNsOr_If(distinguisher_1),
        AsYnC_SeNsOr_If(distinguisher_2)
        )
async def execution_StEp_2_1():
    asyncio.sleep(0.0000000000000001)
    module = ChEcK_PaRaMeTeR(SeTs_VaLuEs_3(),40)
    if (module[0]==1):
        await asyncio.gather(
            execution_StEp_3_indivigual(0),
            execution_StEp_3_indivigual(1),
            execution_StEp_3_indivigual(2)
        )
async def execution_StEp_2_2():
    asyncio.sleep(0.0000000000000001)
    module = ChEcK_PaRaMeTeR(SeTs_VaLuEs_3(),40)
    if (module[1]==1):
        await asyncio.gather(
            execution_StEp_3_indivigual(0),
            execution_StEp_3_indivigual(3),
            execution_StEp_3_indivigual(2)
        )
async def execution_StEp_1():
    module = ChEcK_PaRaMeTeR(SeTs_VaLuEs_4(),40)
    if (module[0]==1):
        await asyncio.gather(
            execution_StEp_2_1(),
            execution_StEp_2_2()
        )