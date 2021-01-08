"""e-puck controller."""
#team-ID = 55


from controller import Robot, Motor ,DistanceSensor, Keyboard
from pynput.keyboard import Key, Listener
import math
import asyncio
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

#initialize keyboard
keyboard = Keyboard()
keyboard.enable(1)

#setting constants
PI = math.pi
AXLE_LENGHT = 56
MAX_SPEED = 6.28
Sensor_names_Distance = ('ps0', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5', 'ps6', 'ps7')
Sensor_names_Rotary_encoders = ('left wheel sensor', 'right wheel sensor')
KeY_VaRiAbLe = {"'f'": 0, "'g'": 0, "'s'": 0, "'d'": 0, "'u'": 0, "'r'": 0, "'k'": 0, "'y'": 0, "'t'": 0, "'o'": 0, "'e'": 0, "'p'": 0, "'w'": 0, "'i'": 0, "'q'": 0, "'l'": 0, "'v'": 0, "'x'": 0, "'n'": 0, "'c'": 0, "'m'": 0, "'z'": 0, "'b'": 0, "'h'": 0, "'j'": 0, "'a'": 0}
KeY_VaRiAbLe_P = {"'f'": 0, "'g'": 0, "'s'": 0, "'d'": 0, "'u'": 0, "'r'": 0, "'k'": 0, "'y'": 0, "'t'": 0, "'o'": 0, "'e'": 0, "'p'": 0, "'w'": 0, "'i'": 0, "'q'": 0, "'l'": 0, "'v'": 0, "'x'": 0, "'n'": 0, "'c'": 0, "'m'": 0, "'z'": 0, "'b'": 0, "'h'": 0, "'j'": 0, "'a'": 0}
MoVeMeNt_VaRiAbLe = {'Right_Motor' : 0 , 'Left_Motor' : 0 , 'Threshhold' : 6.28 }

#defining values for each movement
DIST_VARIABLE = (450,320,MAX_SPEED)
TURN_90_Degree = (627, 3.00199999999999999999999999999999999999999999999999999999999999999,1255)
First_circle_radius = (150,1.64 * MAX_SPEED,4993,4850)
Second_circle_radius = (225,1.2 * MAX_SPEED,6450)
Third_circle_radius = (300,0.96 * MAX_SPEED,8300)

#defining syyc functions
def BHAIBHAIBHAI():#to provide enough time to stabalize the robot
    robot.step(1)

def stop_robot():#to stop the robot
    leftMotor.setVelocity(0)
    rightMotor.setVelocity(0)
    BHAIBHAIBHAI()

def move_xcm(time_move, SPEED):#to move in a straight line for x distance
    cmon = int(8 * time_move)
    leftMotor.setVelocity(SPEED)
    rightMotor.setVelocity(SPEED)
    robot.step(cmon)

def move_x_y_speed(Left , Right , time_move):
    cmon = int(8 * time_move)
    leftMotor.setVelocity(Left)
    rightMotor.setVelocity(Right)
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

def smul_AC_turn(Turn_Amount,SPEED,TIME):#variable turn (anti-clockwise)
    Velocity_Reduction = ((Turn_Amount/100)*SPEED)
    LEFT = SPEED-Velocity_Reduction
    RIGHT = SPEED
    leftMotor.setVelocity(LEFT)
    rightMotor.setVelocity(RIGHT)
    robot.step(TIME)

def smul_C_turn(Turn_Amount,SPEED,TIME):#variable turn (clockwise)
    Velocity_Reduction = ((Turn_Amount/100)*SPEED)
    RIGHT = SPEED-Velocity_Reduction
    LEFT = SPEED
    leftMotor.setVelocity(LEFT)
    rightMotor.setVelocity(RIGHT)
    robot.step(TIME)

def Distance_Of_DistanceSensor():#getting distance from the distance sensors
    Final_Distance_Sensor_Values = []
    Distance_Sensor_Values = []
    Temporary_Distance_Sensor_Values = []
    for i1 in range (len(Sensor_names_Distance)):
        Temporary_Distance_Sensor_Values.append(robot.getDistanceSensor(Sensor_names_Distance[i1]))
        Temporary_Distance_Sensor_Values[i1].enable(timestep)
    for i2 in range (len(Sensor_names_Distance)):
        Distance_Sensor_Values.append(Temporary_Distance_Sensor_Values[i2].getValue())
        Distance_Sensor_Values[i2] = float(Distance_Sensor_Values[i2])
    for i3 in range (len(Sensor_names_Distance)):
        if (Distance_Sensor_Values[i3]!=0):
            temp_value = ((1000 * (1 / Distance_Sensor_Values[i3])) - 0.5)
            if (temp_value>0):
                temp_value = int(((1000 * (1 / Distance_Sensor_Values[i3])) - 0.5))
            if (temp_value<0):
                temp_value = int(((1000 * (1 / Distance_Sensor_Values[i3])) - 0.5))
        else:
            temp_value = ((Distance_Sensor_Values[i3]))
        Final_Distance_Sensor_Values.append(temp_value)
        if (Final_Distance_Sensor_Values[i3]>50):
            Final_Distance_Sensor_Values[i3] = 0.0
    output = Final_Distance_Sensor_Values
    return output

InItIaLiZeR =  Distance_Of_DistanceSensor()

def AnGlE_Of_RoTaRy_EnCoDeRs():
    Final_Angle_Sensor_Values = []
    Angle_Sensor_Values = []
    Temporary_Angle_Sensor_Values = []
    for i1 in range (len(Sensor_names_Rotary_encoders)):
        Temporary_Angle_Sensor_Values.append(robot.getPositionSensor(Sensor_names_Rotary_encoders[i1]))
        Temporary_Angle_Sensor_Values[i1].enable(timestep)
    for i2 in range (len(Sensor_names_Rotary_encoders)):
        Angle_Sensor_Values.append(Temporary_Angle_Sensor_Values[i2].getValue())
        Angle_Sensor_Values[i2] = float(Angle_Sensor_Values[i2])
    for i3 in range (len(Sensor_names_Rotary_encoders)):
        if (Angle_Sensor_Values[i3]!=0):
            temp_value = Angle_Sensor_Values[i3]
            if (temp_value>0):
                temp_value = Angle_Sensor_Values[i3]
            if (temp_value<0):
                temp_value = Angle_Sensor_Values[i3]
        else:
            temp_value = ((Angle_Sensor_Values[i3]))
        Final_Angle_Sensor_Values.append(temp_value)
        if (Final_Angle_Sensor_Values[i3]>5000):
            Final_Angle_Sensor_Values[i3] = 0.0
    output = Final_Angle_Sensor_Values
    return output

InItIaLiZeR =  AnGlE_Of_RoTaRy_EnCoDeRs()

#sequencers
def CHEcK_SENsoR_DiStAnCe(Sensor_Number):#function to make calling the Distance_Of_DistanceSensor() easier
    x = Distance_Of_DistanceSensor()
    output = x[Sensor_Number]
    return output

def SeT_SeNsOr_DiStAnCe_SeT_1(Sensor_vlaues):#making the 1st set of the tree approach used in this code
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

def SeT_SeNsOr_DiStAnCe_SeT_2(Sensor_vlaues):#making the 2nd set of the tree approach used in this code
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

def SeT_SeNsOr_DiStAnCe_SeT_4(Sensor_vlaues):#making the 3rd set of the tree approach used in this code
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

def SeTs_VaLuEs_DiStAnCe_1():#making calling the set easier
    Sensor_Set_1 = SeT_SeNsOr_DiStAnCe_SeT_1(Distance_Of_DistanceSensor())
    return Sensor_Set_1

def SeTs_VaLuEs_DiStAnCe_2():#making calling the set easier
    Sensor_Set_2 = SeT_SeNsOr_DiStAnCe_SeT_2(Distance_Of_DistanceSensor())
    return Sensor_Set_2

def SeTs_VaLuEs_DiStAnCe_4():#making calling the set easier
    Sensor_Set_4 = SeT_SeNsOr_DiStAnCe_SeT_4(Distance_Of_DistanceSensor())
    return Sensor_Set_4

def ChEcK_PaRaMeTeR_DiStAnCe(Value, threshhold):#turning the inputs into binary to make detection easier
    Value_count = len(Value)
    x = {}
    for i in range (Value_count):
        if (Value[i]<threshhold and Value[i]>0):
            x[i] = 1
        else:
            x[i] = 0
    return x

def CHEcK_SENsoR_rotary(side):
    x_temp = InItIaLiZe_tHe_rOtArY_SeNsOr()
    x = x_temp[side]
    return x

def InItIaLiZe_tHe_rOtArY_SeNsOr():
    Angle_Sensor_Values = []
    temp_value = AnGlE_Of_RoTaRy_EnCoDeRs()
    for i in range (len(Sensor_names_Rotary_encoders)):
        temp_value_1 = (temp_value[i]/(2*PI))
        temp_value_2 = 100*temp_value_1
        temp_value_3 = int(temp_value_2)
        Angle_Sensor_Values.append(temp_value_3)
    return Angle_Sensor_Values

def SeT_SeNsOr_Rotary_Encoders(number):
    temp_value = InItIaLiZe_tHe_rOtArY_SeNsOr()
    temp_value_4 = []
    for i in range(2):
        temp_value_1 = temp_value[i]/100
        temp_value_2 = (temp_value_1 - int(temp_value_1))
        temp_value_3 = int(100 * temp_value_2)
        temp_value_4.append(temp_value_3)

    return temp_value_4[number]

def on_press(key):
    key = str (key)
    KeY_VaRiAbLe[key] = 1
    return False

def on_release(key):
    key = str(key)
    KeY_VaRiAbLe[key] = 0
    return False

def GeT_ReSpOnSe():
    with Listener(on_press=on_press,on_release=on_release) as listener:
        listener.join()
    return KeY_VaRiAbLe

def SeT_VaLuEs_Ds4(which):
    abstact = KeY_VaRiAbLe
    R = {'R1' : abstact["'d'"] , 'R2' : abstact["'g'"]  , 'R3' : abstact["'j'"] }
    L = {'L1' : abstact["'s'"] , 'L2' : abstact["'f'"]  , 'L3' : abstact["'h'"] }
    D_PAD = {'UP' : abstact["'u'"] , 'DOWN' : abstact["'i'"]  , 'RIGHT' : abstact["'p'"] , 'LEFT' : abstact["'o'"] }
    BUTTONS = {'Triangle' : abstact["'r'"] , 'Cross' : abstact["'q'"]  , 'Circle' : abstact["'w'"] , 'Square' : abstact["'e'"] }
    L_ANALOG = {'UP' : abstact["'l'"] , 'DOWN' : abstact["'z'"]  , 'RIGHT' : abstact["'c'"] , 'LEFT' : abstact["'x'"] }
    R_ANALOG = {'UP' : abstact["'v'"] , 'DOWN' : abstact["'b'"]  , 'RIGHT' : abstact["'m'"] , 'LEFT' : abstact["'n'"] }
    OTHER = {'Share' : abstact["'y'"] , 'Options' : abstact["'t'"]  , 'Touchpad' : abstact["'k'"] , 'PS' : abstact["'a'"] }
    if  (which == 0):
        return R
    if  (which == 1):
        return L
    if  (which == 2):
        return D_PAD
    if  (which == 3):
        return BUTTONS
    if  (which == 4):
        return L_ANALOG
    if  (which == 5):
        return R_ANALOG
    if  (which == 6):
        return OTHER

#defining aysnc functions
async def AsYnC_SeNsOr_indivigual_DiStAnCe(v):#part 3 of the tree formation where  sensors are checked
    output = 0
    x = ChEcK_PaRaMeTeR_DiStAnCe(SeTs_VaLuEs_DiStAnCe_1(), 40)
    if(v == -1):
        v = 7
    if (x[v] == 1):
        await asyncio.sleep(0.0000000000000001)
        output = 1
        return (output)

    else:
        await asyncio.sleep(0.0000000000000001)
        return (output)

async def execution_StEp_3_indivigual_DiStAnCe(indivigual):#part 2 of the tree formation where modules(front,right,left,back are checked
    output = 0
    module = ChEcK_PaRaMeTeR_DiStAnCe(SeTs_VaLuEs_DiStAnCe_2(), 40)
    distinguisher_1 = indivigual*2
    distinguisher_2 = distinguisher_1-1
    if(module[indivigual]==1):
        await asyncio.sleep(0.0000000000000001)
        output = await asyncio.gather(
        AsYnC_SeNsOr_indivigual_DiStAnCe(distinguisher_2),
        AsYnC_SeNsOr_indivigual_DiStAnCe(distinguisher_1)
        )
        return (output)
    else:
        await asyncio.sleep(0.0000000000000001)
        return [output,output]

async def execution_StEp_1_DiStAnCe():#part 1 of the tree formation where the tree formation starts and narrows down where the issue is and puts it in a proper order so it can be read and executed
    output = 0
    module = ChEcK_PaRaMeTeR_DiStAnCe(SeTs_VaLuEs_DiStAnCe_4(), 40)
    if (module[0]==1):
        output = await asyncio.gather(
            execution_StEp_3_indivigual_DiStAnCe(0),
            execution_StEp_3_indivigual_DiStAnCe(1),
            execution_StEp_3_indivigual_DiStAnCe(2),
            execution_StEp_3_indivigual_DiStAnCe(3)
        )
        return (output)
    else:
        return [[output,output],[output,output],[output,output],[output,output]]

async def AsYnC_GeT_VaLuE_DiStAnCe(MoDuLe, VaRiAbLe):
    await asyncio.sleep(0.0000000000000001)
    SeT_MaIn = await execution_StEp_1_DiStAnCe()
    if(SeT_MaIn[MoDuLe]!=0):
        SeT_MoDuLe = SeT_MaIn[MoDuLe]
        SeT_VaRiAbLe = SeT_MoDuLe[VaRiAbLe]
        return SeT_VaRiAbLe
    else:
        return 0

async def AsYnCeR_FuNcTiOnS(input):#turning syncronus functions into asyncronas tasks
    await asyncio.sleep(0.0000000000000001)
    input

async def AlGoRiThM_MoDuLe_actions_DiStAnCe(module, Speed):#setting the desired output when a certain module detects some thing
    await asyncio.sleep(0.0000000000000001)
    RoTaRy_TrIgGeR = 0
    SeNsOr = await asyncio.gather(AsYnC_GeT_VaLuE_DiStAnCe(0, 0),  #sensor 7
                                  AsYnC_GeT_VaLuE_DiStAnCe(0, 1),  #sensor 0
                                  AsYnC_GeT_VaLuE_DiStAnCe(1, 0),  #sensor 1
                                  AsYnC_GeT_VaLuE_DiStAnCe(1, 1),  #sensor 2
                                  AsYnC_GeT_VaLuE_DiStAnCe(2, 0),  #sensor 3
                                  AsYnC_GeT_VaLuE_DiStAnCe(2, 1),  #sensor 4
                                  AsYnC_GeT_VaLuE_DiStAnCe(3, 0),  #sensor 5
                                  AsYnC_GeT_VaLuE_DiStAnCe(3, 1)  #sensor 6
                                  )
    SeNsOr__VaR_0 = SeNsOr[1]
    SeNsOr__VaR_1 = SeNsOr[2]
    SeNsOr__VaR_2 = SeNsOr[3]
    SeNsOr__VaR_3 = SeNsOr[4]
    SeNsOr__VaR_4 = SeNsOr[5]
    SeNsOr__VaR_5 = SeNsOr[6]
    SeNsOr__VaR_6 = SeNsOr[7]
    SeNsOr__VaR_7 = SeNsOr[0]
    MoDuLe_1 ={0:100,1:100}
    MoDuLe_2 = {0:100,1:50,2:100,3:25,4:100,5:10}
    if(module == 0):
        if(SeNsOr__VaR_7 == 1 or SeNsOr__VaR_0 == 1):
            RoTaRy_TrIgGeR = 1
            if (SeNsOr__VaR_7>SeNsOr__VaR_0):
                await AsYnCeR_FuNcTiOnS(smul_C_turn(MoDuLe_1[0], Speed, MoDuLe_1[1]))
            elif(SeNsOr__VaR_7<SeNsOr__VaR_0):
                await AsYnCeR_FuNcTiOnS(smul_AC_turn(MoDuLe_1[0], Speed, MoDuLe_1[1]))
            if(SeNsOr__VaR_7 ==1 and SeNsOr__VaR_0 == 1):
                await AsYnCeR_FuNcTiOnS(turn_c_degree(TURN_90_Degree[2], TURN_90_Degree[1]))
                await AsYnCeR_FuNcTiOnS(move_xcm(250, Speed))
                await AsYnCeR_FuNcTiOnS(turn_c_degree(TURN_90_Degree[0], TURN_90_Degree[1]))
                await AsYnCeR_FuNcTiOnS(move_xcm(250, Speed))
                await AsYnCeR_FuNcTiOnS(turn_c_degree(TURN_90_Degree[0], TURN_90_Degree[1]))

    if(module == 1):
        if(SeNsOr__VaR_1 == 1 or SeNsOr__VaR_2 == 1):
            RoTaRy_TrIgGeR = 1
            if (SeNsOr__VaR_1>SeNsOr__VaR_2):
                await AsYnCeR_FuNcTiOnS(smul_AC_turn(MoDuLe_2[0],Speed,MoDuLe_2[1]))
            elif(SeNsOr__VaR_1<SeNsOr__VaR_2):
                await AsYnCeR_FuNcTiOnS(smul_AC_turn(MoDuLe_2[2], Speed, MoDuLe_2[3]))
            if(SeNsOr__VaR_1 == SeNsOr__VaR_2):
                await AsYnCeR_FuNcTiOnS(smul_AC_turn(MoDuLe_2[4], Speed, MoDuLe_2[5]))

    if(module == 3):
        if(SeNsOr__VaR_6 == 1 or SeNsOr__VaR_5 == 1):
            RoTaRy_TrIgGeR = 1
            if (SeNsOr__VaR_6 > SeNsOr__VaR_5):
                await AsYnCeR_FuNcTiOnS(smul_C_turn(MoDuLe_2[0], Speed, MoDuLe_2[1]))
            elif (SeNsOr__VaR_6 < SeNsOr__VaR_5):
                await AsYnCeR_FuNcTiOnS(smul_C_turn(MoDuLe_2[2], Speed, MoDuLe_2[3]))
            if (SeNsOr__VaR_6 == SeNsOr__VaR_5):
                await AsYnCeR_FuNcTiOnS(smul_C_turn(MoDuLe_2[4], Speed, MoDuLe_2[5]))#
    return RoTaRy_TrIgGeR

async def AlGoRiThM_ExEcUtIoN_DiStAnCe(SpeeD):#main execution file
    move_xcm(1,SpeeD)
    TrIgGeR  = await asyncio.gather(
        AlGoRiThM_MoDuLe_actions_DiStAnCe(0, SpeeD),
        AlGoRiThM_MoDuLe_actions_DiStAnCe(1, SpeeD),
        AlGoRiThM_MoDuLe_actions_DiStAnCe(3, SpeeD)
    )
    TrIgGeR_1 = (TrIgGeR[0]+TrIgGeR[1]+TrIgGeR[2])/3
    if (TrIgGeR_1> 0):
        TrIgGeR_1 = 1
    return TrIgGeR_1

async def AlGoRiThM_ExEcUtIoN_Rotary_Encoders(SPeeD):
    VaRiAbLe = await AlGoRiThM_ExEcUtIoN_DiStAnCe(SPeeD)
    if(SeT_SeNsOr_Rotary_Encoders(0) != 0 and  SeT_SeNsOr_Rotary_Encoders(1) != 0):
        if(VaRiAbLe == 0):
            tf_is_you_doin = [CHEcK_SENsoR_rotary(0),CHEcK_SENsoR_rotary(1)]
            if (tf_is_you_doin[0] > tf_is_you_doin[1]):
                VaRiAbLe_1 = 2 * (tf_is_you_doin[0] / (tf_is_you_doin[1] + 1))
                if (VaRiAbLe_1 <= 1):
                    VaRiAbLe_2 = VaRiAbLe_1 * 100
                elif (VaRiAbLe_1 <= 10):
                    VaRiAbLe_2 = VaRiAbLe_1 * 10
                elif (VaRiAbLe_1 <= 100):
                    VaRiAbLe_2 = VaRiAbLe_1 * 1
                smul_AC_turn(99, SPeeD, 10)
            if (CHEcK_SENsoR_rotary(0) < CHEcK_SENsoR_rotary(1)):
                VaRiAbLe_1 = 2 * (tf_is_you_doin[1] / (tf_is_you_doin[0] + 1))
                if (VaRiAbLe_1 <= 1):
                    VaRiAbLe_2 = VaRiAbLe_1 * 100
                elif (VaRiAbLe_1 <= 10):
                    VaRiAbLe_2 = VaRiAbLe_1 * 10
                elif (VaRiAbLe_1 <= 100):
                    VaRiAbLe_2 = VaRiAbLe_1 * 1
                smul_C_turn(99, SPeeD, 10)
            if (CHEcK_SENsoR_rotary(0) == CHEcK_SENsoR_rotary(1)):
                move_xcm(1, SPeeD)

async def StEp_MaNuAl_CoNtRoLl_DeSiGnAtIoN(which):
    await AsYnCeR_FuNcTiOnS(stop_robot())
    if(which == 0):
        print('by wire')
        GeT_ReSpOnSe()
        Abort_key_recieve = SeT_VaLuEs_Ds4(3)
        Abort_key = Abort_key_recieve['Circle']
        GeT_ReSpOnSe()
        while (Abort_key == 0):
            print('Abort key')
            GeT_ReSpOnSe()
            Abort_key_recieve = SeT_VaLuEs_Ds4(3)
            Abort_key = Abort_key_recieve['Circle']
            print('Abort status',Abort_key)
            GeT_ReSpOnSe()
            MoVeMeNt_VaRiAbLe['Left_Motor'] *= 10
            MoVeMeNt_VaRiAbLe['Right_Motor'] *= 10
            print('Right')
            GeT_ReSpOnSe()
            Increment_key_Right_recieve = SeT_VaLuEs_Ds4(0)
            Increment_key_Right = Increment_key_Right_recieve['R2']
            DIncrement_key_Right_recieve = SeT_VaLuEs_Ds4(0)
            DIncrement_key_Right = DIncrement_key_Right_recieve['R1']
            print('R2', Increment_key_Right)
            print('R1', DIncrement_key_Right)
            if (Increment_key_Right == 1 and DIncrement_key_Right == 0):
                MoVeMeNt_VaRiAbLe['Right_Motor'] += 1
            if (DIncrement_key_Right == 1 and Increment_key_Right == 0):
                MoVeMeNt_VaRiAbLe['Right_Motor'] -= 1
            GeT_ReSpOnSe()
            print('Left')
            GeT_ReSpOnSe()
            Increment_key_left_recieve = SeT_VaLuEs_Ds4(1)
            Increment_key_left = Increment_key_left_recieve['L2']
            DIncrement_key_left_recieve = SeT_VaLuEs_Ds4(1)
            DIncrement_key_left = DIncrement_key_left_recieve['L1']
            print('l2',Increment_key_left)
            print('l1', DIncrement_key_left)
            if (Increment_key_left == 1 and DIncrement_key_left == 0):
                MoVeMeNt_VaRiAbLe['Left_Motor'] += 1
            if (DIncrement_key_left == 1 and Increment_key_left == 0):
                MoVeMeNt_VaRiAbLe['Left_Motor'] -= 1
            GeT_ReSpOnSe()
            MoVeMeNt_VaRiAbLe['Left_Motor'] /= 10
            MoVeMeNt_VaRiAbLe['Right_Motor'] /= 10
            print(MoVeMeNt_VaRiAbLe['Left_Motor'] , MoVeMeNt_VaRiAbLe['Right_Motor'])
        await AsYnCeR_FuNcTiOnS(move_x_y_speed(MoVeMeNt_VaRiAbLe['Left_Motor'] , MoVeMeNt_VaRiAbLe['Right_Motor'], 10))
    if(which == 1):
        print('pre set')
        print('Abort key')
        GeT_ReSpOnSe()
        Abort_key_recieve = SeT_VaLuEs_Ds4(3)
        Abort_key = Abort_key_recieve['Circle']
        print('Abort status', Abort_key)
        GeT_ReSpOnSe()
        while (Abort_key == 0):
            print('Abort key')
            GeT_ReSpOnSe()
            Abort_key_recieve = SeT_VaLuEs_Ds4(3)
            Abort_key = Abort_key_recieve['Circle']
            print('Abort status', Abort_key)
            if (Abort_key == 1):
                await AsYnCeR_FuNcTiOnS(stop_robot())
            GeT_ReSpOnSe()
            GeT_ReSpOnSe()
            Increment_key_up_recieve = SeT_VaLuEs_Ds4(2)
            Increment_key_up = Increment_key_up_recieve['UP']
            print('UP', Increment_key_up)
            if (Increment_key_up == 1):
                await AsYnCeR_FuNcTiOnS(move_xcm(1, MoVeMeNt_VaRiAbLe['Threshhold']))
                print('move front')
            GeT_ReSpOnSe()
            GeT_ReSpOnSe()
            Increment_key_down_recieve = SeT_VaLuEs_Ds4(2)
            Increment_key_down = Increment_key_down_recieve['DOWN']
            print('DOWN', Increment_key_down)
            if (Increment_key_down == 1):
                await AsYnCeR_FuNcTiOnS(move_xcm(1, -MoVeMeNt_VaRiAbLe['Threshhold']))
                print('move back')
            GeT_ReSpOnSe()
            GeT_ReSpOnSe()
            Increment_key_Right_recieve = SeT_VaLuEs_Ds4(2)
            Increment_key_Right = Increment_key_Right_recieve['RIGHT']
            print('RIGHT', Increment_key_Right)
            if (Increment_key_Right == 1):
                await AsYnCeR_FuNcTiOnS(turn_c_degree(1,1))
                print('move right')
            GeT_ReSpOnSe()
            GeT_ReSpOnSe()
            Increment_key_left_recieve = SeT_VaLuEs_Ds4(2)
            Increment_key_left = Increment_key_left_recieve['LEFT']
            print('LEFT', Increment_key_left)
            if (Increment_key_left == 1):
                await AsYnCeR_FuNcTiOnS(turn_ac_degree(1,1))
                print('move left')
            GeT_ReSpOnSe()

async def StEp_CoNtRoLl_DeSiGnAtIoN():
    omgbruhlol = 1
    await AsYnCeR_FuNcTiOnS(stop_robot())
    print('options')
    GeT_ReSpOnSe()
    Options_recieve = SeT_VaLuEs_Ds4(6)
    Options = Options_recieve['Options']
    print(Options)
    GeT_ReSpOnSe()
    print('Share')
    GeT_ReSpOnSe()
    Share_recieve = SeT_VaLuEs_Ds4(6)
    Share = Share_recieve['Share']
    print(Share)
    GeT_ReSpOnSe()
    print('key1')
    GeT_ReSpOnSe()
    Activate_key_1_recieve = SeT_VaLuEs_Ds4(0)
    Activate_key_1 = Activate_key_1_recieve['R3']
    print(Activate_key_1)
    GeT_ReSpOnSe()
    print('key2')
    GeT_ReSpOnSe()
    Activate_key_2_recieve = SeT_VaLuEs_Ds4(1)
    Activate_key_2 = Activate_key_2_recieve['L3']
    print(Activate_key_2)
    GeT_ReSpOnSe()
    while (omgbruhlol == 1):
        if (Options == 1 and Share == 1):
            print('manual')
            while (Activate_key_1 == 1 and Activate_key_2 == 0):
                print('key1')
                GeT_ReSpOnSe()
                Activate_key_1_recieve = SeT_VaLuEs_Ds4(0)
                Activate_key_1 = Activate_key_1_recieve['R3']
                GeT_ReSpOnSe()
                print('key2')
                GeT_ReSpOnSe()
                Activate_key_2_recieve = SeT_VaLuEs_Ds4(1)
                Activate_key_2 = Activate_key_2_recieve['L3']
                GeT_ReSpOnSe()
                print('choose mode')
                print ('by wire = up or pre_set = down')
                GeT_ReSpOnSe()
                Activate_key_up_recieve = SeT_VaLuEs_Ds4(2)
                Activate_key_up = Activate_key_up_recieve['UP']
                GeT_ReSpOnSe()
                GeT_ReSpOnSe()
                Activate_key_down_recieve = SeT_VaLuEs_Ds4(2)
                Activate_key_down = Activate_key_down_recieve['DOWN']
                GeT_ReSpOnSe()
                if(Activate_key_up == 1 and Activate_key_down == 0):
                    await StEp_MaNuAl_CoNtRoLl_DeSiGnAtIoN(0)
                    await AsYnCeR_FuNcTiOnS(print((MoVeMeNt_VaRiAbLe['Left_Motor'])))#leftMotor.setVelocity(MoVeMeNt_VaRiAbLe['Left_Motor']))
                    await AsYnCeR_FuNcTiOnS(print((MoVeMeNt_VaRiAbLe['Right_Motor'])))#rightMotor.setVelocity(MoVeMeNt_VaRiAbLe['Right_Motor']))
                elif(Activate_key_up == 0 and Activate_key_down == 1):
                    await StEp_MaNuAl_CoNtRoLl_DeSiGnAtIoN(1)
                elif(Activate_key_up == 1 and Activate_key_down == 1):
                    await AsYnCeR_FuNcTiOnS(stop_robot())
                    break

            omgbruhlol = 0
        elif (Options == 1 and Share == 0):
            print('AI1')
            await AsYnCeR_FuNcTiOnS(stop_robot())
            while (Activate_key_1 == 1 and Activate_key_2 == 0):
                print('key1')
                GeT_ReSpOnSe()
                Activate_key_1_recieve = SeT_VaLuEs_Ds4(0)
                Activate_key_1 = Activate_key_1_recieve['R3']
                print(Activate_key_1)
                GeT_ReSpOnSe()
                print('key2')
                GeT_ReSpOnSe()
                Activate_key_2_recieve = SeT_VaLuEs_Ds4(1)
                Activate_key_2 = Activate_key_2_recieve['L3']
                print(Activate_key_2)
                GeT_ReSpOnSe()
                print('AI1 operational')
                await AlGoRiThM_ExEcUtIoN_DiStAnCe(MoVeMeNt_VaRiAbLe['Threshhold'])
            stop_robot()
            omgbruhlol = 0
        elif (Options == 0 and Share == 1):
            print('AI2')
            await AsYnCeR_FuNcTiOnS(stop_robot())
            while (Activate_key_1 == 1 and Activate_key_2 == 0):
                print('key1')
                GeT_ReSpOnSe()
                Activate_key_1_recieve = SeT_VaLuEs_Ds4(0)
                Activate_key_1 = Activate_key_1_recieve['R3']
                print(Activate_key_1)
                GeT_ReSpOnSe()
                print('key2')
                GeT_ReSpOnSe()
                Activate_key_2_recieve = SeT_VaLuEs_Ds4(1)
                Activate_key_2 = Activate_key_2_recieve['L3']
                print(Activate_key_2)
                GeT_ReSpOnSe()
                print('ai2 operational')
                await AlGoRiThM_ExEcUtIoN_Rotary_Encoders(MoVeMeNt_VaRiAbLe['Threshhold'])
            stop_robot()
            omgbruhlol = 0
        elif (Options == 0 and Share == 0):
            print('yea nope')
            omgbruhlol = 0
    print(KeY_VaRiAbLe)
    print('restart')
    return 1

async def StEp_start_CoNtRoLl_Ds4():
    GeT_ReSpOnSe()
    omg = SeT_VaLuEs_Ds4(6)
    if (omg['PS'] == 1):
        GeT_ReSpOnSe()
        x = 1
        while (x == 1):
            print("controller start")
            x = await StEp_CoNtRoLl_DeSiGnAtIoN()
    else:
        print('abort')

asyncio.run(StEp_start_CoNtRoLl_Ds4())
stop_robot()