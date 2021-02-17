#team id - 55
#team name - Sudo

from controller import Robot, DistanceSensor, Motor
from controller import Camera
from vehicle import Driver
import cv2 as cv
import numpy as np
import asyncio
import math

# initializing
TIMESTEP = 16#setting the time step

robot = Robot()#creating robot instance

timestep = int(robot.getBasicTimeStep())  #creating timestep for the sensors

camera = Camera('camera')#creating usable class intance  for the camera

camera.enable(TIMESTEP)#enabling camera by using the enable function

leftMotor = robot.getMotor('left wheel motor')#setting leftmotor class

rightMotor = robot.getMotor('right wheel motor')#setting right  motor class

leftMotor.setPosition(float('inf'))#setting position zero

rightMotor.setPosition(float('inf'))#setting position zero

leftSpeed = 0.0#setting position zero

rightSpeed = 0.0#setting position zero

leftMotor.setVelocity(leftSpeed)#setting position zero

rightMotor.setVelocity(rightSpeed)#setting position zero

multipe_centroid = open('E:\computer\e-ysrc\stuf to upload\Task511\Task5\controllers\e-puck\multiple_centroid.txt','w+')#logging centroids

average_centroid = open('E:\computer\e-ysrc\stuf to upload\Task511\Task5\controllers\e-puck\leverage_centroid.txt','w+')#logging centroids

# constants
PI = math.pi#setting pi for inherited functions

MAX_SPEED = 6.28#setting the max speed for bot

AXLE_LENGHT = 56#setting variabble for inherited functions

Sensor_names_Distance = ('ps0', 'ps1', 'ps2', 'ps3', 'ps4', 'ps5', 'ps6', 'ps7')#setting variabble for inherited functions

Sensor_names_Rotary_encoders = ('left wheel sensor', 'right wheel sensor')#setting variabble for inherited functions

triggered = [0,0,0,0,0,0]#throw away binary trigggers

#functions
def robot_wait(time=1):#simple function to give the robot a small break to finish a function :-)
    robot.step(time)#time.step variable


def stop_robot():#to stop the robot
    leftMotor.setVelocity(0)#stopping left mototr
    rightMotor.setVelocity(0)#stopping  right  motor
    robot_wait()##giving the robot a small break :-)


def move_xcm(time_move, SPEED):#simple function to move  a certain amount of distance using a  certain speed
    cmon = int(8 * time_move * (6.28/SPEED))#converting cm to required time to move the exact cm
    leftMotor.setVelocity(SPEED)#setting left velocity
    rightMotor.setVelocity(SPEED)#setting right velocity
    robot_wait(cmon)#setting the required wait time


def turn_c_degree(angle):#simple function to turn  the bot specif degrees with the  least time
    time_move = int(angle*(20/3))#calculate  amount of time to wait for the turn to complete
    leftMotor.setVelocity((1501/500))#setting  left speed
    rightMotor.setVelocity(-(1501/500))#setting  right speed
    robot_wait(time_move)#waiting the required time


def turn_ac_degree(angle):#simple function to turn  the bot specif degrees with the  least time
    time_move = int( angle *(20/3))#calculate  amount of time to wait for the turn to complete
    leftMotor.setVelocity(-(1501/500))#setting  left speed
    rightMotor.setVelocity((1501/500))#setting  right speed
    robot_wait(time_move)#waiting the required time

def turn_c_radius_degree(time_move, RADI,SPEED):#function to turn  based on a specific radius
    global triggered#throw  away variable
    RaTiO = (((PI*(RADI + (AXLE_LENGHT/2)))/1000)*SPEED)/(((PI*(RADI - (AXLE_LENGHT/2)))/1000)*SPEED)#calculating the ratio of the wheels
    LEFT = SPEED#setting the higher full speed wheel value
    RIGHT = LEFT/RaTiO#setting llower speed for exact movement
    triggered[5] = RIGHT#setting throwaway varialbe
    leftMotor.setVelocity(LEFT)#setting  velocity
    rightMotor.setVelocity(RIGHT)#setting velocity
    robot_wait(time_move)#waiting for completion

def turn_ac_radius_degree(time_move, RADI,SPEED):#function to turn  based on a specific radius
    global triggered#throw  away variable
    RaTiO = (((PI*(RADI + (AXLE_LENGHT/2)))/1000)*SPEED)/(((PI*(RADI - (AXLE_LENGHT/2)))/1000)*SPEED)#calculating the ratio of the wheels
    RIGHT = SPEED#setting the higher full speed wheel value
    LEFT = RIGHT/RaTiO#setting llower speed for exact movement
    triggered[5] = LEFT#setting throwaway varialbe
    leftMotor.setVelocity(LEFT)#setting velocity
    rightMotor.setVelocity(RIGHT)#setting velocity
    robot_wait(time_move)#waiting for completion

def smul_c_turn(Turn_Amount,SPEED,TIME):
    Velocity_Reduction = ((Turn_Amount/100)*SPEED)#calculating the ratio of the wheels
    RIGHT = SPEED-Velocity_Reduction#setting llower speed for exact movement
    LEFT = SPEED#setting the higher full speed wheel value
    leftMotor.setVelocity(LEFT)#setting velocity
    rightMotor.setVelocity(RIGHT)#setting velocity
    robot_wait(TIME)#waiting for completion

def smul_ac_turn(Turn_Amount,SPEED,TIME):#calculating the ratio of the wheels
    Velocity_Reduction = ((Turn_Amount/100)*SPEED)#calculating the ratio of the wheels
    LEFT = SPEED-Velocity_Reduction#setting llower speed for exact movement
    RIGHT = SPEED#setting the higher full speed wheel value
    leftMotor.setVelocity(LEFT)#setting velocity
    rightMotor.setVelocity(RIGHT)#setting velocity
    robot_wait(TIME)#waiting for completion

def distance_of_distance_sensor(sensor_number):#function to extract distance sensor values
    Temporary_Distance_Sensor_Values = (robot.getDistanceSensor(Sensor_names_Distance[sensor_number]))#getting raw aouput
    Temporary_Distance_Sensor_Values.enable(timestep)#enabling timestep
    Distance_Sensor_Values = (Temporary_Distance_Sensor_Values.getValue())#getting readable values
    Distance_Sensor_Values = float(Distance_Sensor_Values)#converting to float to preven errors in future calc
    if (Distance_Sensor_Values != 0):#converting into more interpretible values
        temp_value = (((255 / (Distance_Sensor_Values + 1)) - 0.99609375)*255)
        if (temp_value>0):
            temp_value = int((((255 / (Distance_Sensor_Values + 1)) - 0.99609375)*255))
        if (temp_value<0):
            temp_value = int((((255 / (Distance_Sensor_Values + 1)) - 0.99609375)*255))
    else:
        temp_value = (Distance_Sensor_Values)#if there is a value we dont expect we output direct instead of a  different type of number which may cause issues
    Final_Distance_Sensor_Values = temp_value
    if (Final_Distance_Sensor_Values>8192):#thresholding the max  stable output
        Final_Distance_Sensor_Values = float(0)
    output = Final_Distance_Sensor_Values#returning values
    return output

def angle_of_rotary_encoder(sensor_number):#function to extract rotary encoder  values NOTE:this follows a similar process to distance  sensor so i have not commented here
    Temporary_Distance_Sensor_Values = (robot.getPositionSensor(Sensor_names_Rotary_encoders[sensor_number]))
    Temporary_Distance_Sensor_Values.enable(timestep)
    Distance_Sensor_Values = (Temporary_Distance_Sensor_Values.getValue())
    Distance_Sensor_Values = float(Distance_Sensor_Values)
    temp_value = (Distance_Sensor_Values)
    Final_Distance_Sensor_Values = temp_value
    output = Final_Distance_Sensor_Values
    return output

def sensor_initializer():#to initialize sensors to preven Nan  values
    for i  in range(8):
        distance_of_distance_sensor(i)
    for i in range(2):
        angle_of_rotary_encoder(i)

async def function_asyncer(function):#sothat we can convert sync to async functions without causing potential async blocks
    function

async def thresholder_distance(sensor_number,threshold):#function to check if any sensors or modules may have an obstruction
    await asyncio.sleep(0.0000000000000001)#delay to allow for async to do concurrent processing
    sensor_value = distance_of_distance_sensor(sensor_number)#getting the sensors value
    if ( sensor_value < threshold and sensor_value != 0):#thresholding to give otput
        y_or_n = 1
    elif ( sensor_value > threshold and sensor_value != 0):#thresholding to prevent false positives
        y_or_n = 0
    else:#backup ;-)
        y_or_n = 0
    return y_or_n#returning output

async def module_checker(module_number,threshold):#function to check all modulels or indivigual sensors for the threshold
    await asyncio.sleep(0.0000000000000001)#delay to allow for async to do concurrent processing
    val = await asyncio.gather(thresholder_distance(0,threshold),#gathering the threshold of all snesors
                               thresholder_distance(1,threshold),
                               thresholder_distance(2,threshold),
                               thresholder_distance(3,threshold),
                               thresholder_distance(4,threshold),
                               thresholder_distance(5,threshold),
                               thresholder_distance(6,threshold),
                               thresholder_distance(7,threshold)
                               )
    if (module_number == 1):#checking if there is any obstruction  for  any of the sensors
        output = 0
        output_var_main = float((val[0]+val[1]+val[2]+val[5]+val[6]+val[7])/6)
        if (output_var_main > 0 ):
            output=1
    if (module_number == 2):#checking each indivigual module for obsttruction
        output = [0,0,0,0]
        output_var_front = float((val[7]+val[0])/2)
        if (output_var_front > 0):
            output[0] = 1
        output_var_right =  float((val[1]+val[2])/2)
        if (output_var_right > 0):
            output[1] = 1
        output_var_back =  float((val[3]+val[4])/2)
        if (output_var_back > 0):
            output[2] = 1
        output_var_left =  float((val[5]+val[6])/2)
        if (output_var_left > 0):
            output[3] = 1
    if (module_number == 3):#checking each indivigual sensor
        output = val
    return output

async def move_xcm_smoother(speed,threshold):#function to soft  start the robot to  prevent it from  jumping and hitting a obbstacle
    global triggered
    return_speed = 2.5
    move_xcm(1,return_speed)
    for i in range (int(5*int(speed-return_speed))):
        sense = await module_checker(1,threshold)#backup in case that there is a obstacle so  that the rovbbot dosent crash into it
        move_xcm(1,return_speed+(i/5))
        if (sense == 1):
            break

async def algorithm_distance(module,speed,threshold):#finally the algorithm to do wf
    await asyncio.sleep(0.0000000000000001)#delay to allow for async to do concurrent processing
    response_trigger = 0#throw away variable from heriditory data
    val = await asyncio.gather(thresholder_distance(0,threshold),#getting data  so that the bot is with sync with curent scenario
                               thresholder_distance(1,threshold),
                               thresholder_distance(2,threshold),
                               thresholder_distance(3,threshold),
                               thresholder_distance(4,threshold),
                               thresholder_distance(5,threshold),
                               thresholder_distance(6,threshold),
                               thresholder_distance(7,threshold)
                               )
    module_2 = await module_checker(2,threshold)#checking which module is trigggered
    module_3 = await module_checker(3,threshold)#checking which sensors tripped
    MoDuLe_1 = [1]#setting angle to rotate
    MoDuLe_2 = [1]#setting angle to rotate
    if (module == 0):#checking front module
        if(module_2[0] == 1):#checnking if module  is tripped
            response_trigger = 1#ssetting the value to return
            if (module_3[7] == 1 and module_3[0] == 0):#turning based on the sensor tripped in relation to the other sensor
                await function_asyncer(turn_c_degree(MoDuLe_1[0]))
            if (module_3[7] == 0 and module_3[0] == 1):#turning based on the sensor tripped in relation to the other sensor
                await function_asyncer(turn_ac_degree(MoDuLe_1[0]))
            if (module_3[7] == 1 and module_3[0] == 1):#turning based on the sensor tripped in relation to the other sensor
                if (module_3[6] == 1 and module_3[1] == 0):#turning based on the sensor tripped in relation to the other sensor
                    await function_asyncer(turn_c_degree(MoDuLe_1[0]))
                if (module_3[6] == 0 and module_3[1] == 1):#turning based on the sensor tripped in relation to the other sensor
                    await function_asyncer(turn_ac_degree(MoDuLe_1[0]))
                if (module_3[6] == 1 and module_3[1] == 1):#turning based on the sensor tripped in relation to the other sensor
                    if (module_3[5] == 1 and module_3[2] == 0):#turning based on the sensor tripped in relation to the other sensor
                        await function_asyncer(turn_c_degree(MoDuLe_1[0]))
                    if (module_3[5] == 0 and module_3[2] == 1):#turning based on the sensor tripped in relation to the other sensor
                        await function_asyncer(turn_ac_degree(MoDuLe_1[0]))
                    if (module_3[5] == 0 and module_3[2] == 1):#turning based on the sensor tripped in relation to the other sensor
                        await function_asyncer(turn_c_degree(90))
                        await function_asyncer(move_xcm(250, speed))
                        await function_asyncer(turn_c_degree(90))
                        await function_asyncer(move_xcm(250, speed))
                        await function_asyncer(turn_c_degree(90))

    if (module == 1):#checking right module
        if(module_2[1] == 1):#checnking if module  is tripped
            response_trigger = 1#ssetting the value to return
            if (module_3[1] == 1 and module_3[2] == 0):#turning based on the sensor tripped in relation to the other sensor
                await function_asyncer(turn_ac_degree(MoDuLe_2[0]))
            elif(module_3[1] == 0 and module_3[2] == 1):#turning based on the sensor tripped in relation to the other sensor
                await function_asyncer(turn_ac_degree(MoDuLe_2[0]))
            elif(module_3[1] == 1 and module_3[2] == 1):#turning based on the sensor tripped in relation to the other sensor
                await function_asyncer(turn_ac_degree(MoDuLe_2[0]))
    if (module == 3):#checking left module
        if(module_2[3] == 1):#checnking if module  is tripped
            response_trigger = 1#ssetting the value to return
            if (module_3[6] == 1 and module_3[6] == 0):#turning based on the sensor tripped in relation to the other sensor
                await function_asyncer(turn_c_degree(MoDuLe_2[0]))
            elif (module_3[6] == 0 and module_3[5] == 1):#turning based on the sensor tripped in relation to the other sensor
                await function_asyncer(turn_c_degree(MoDuLe_2[0]))
            elif (module_3[6] == 1 and module_3[5] == 1):#turning based on the sensor tripped in relation to the other sensor
                await function_asyncer(turn_c_degree(MoDuLe_2[0]))
    return response_trigger#returning the output value

async def  run_algorithm_distance(speed,threshold):#running the async (FINALLLLLLYYYYYYY)
    await asyncio.sleep(0.0000000000000001)#delay to allow for async to do concurrent processing
    global triggered#throw away variable to trigger smothener
    module_1 = await module_checker(1,threshold)#checking if any action is needed
    if(module_1 == 1):#conducting  action if module tripped
        triggered[2] = 1#setting variable  to indicate the programm  to conduct  movement smoothening after course correction
        output = await asyncio.gather(#executing all  the module corrections at once
                algorithm_distance(0,speed,threshold),
                algorithm_distance(1,speed,threshold),
                algorithm_distance(3,speed,threshold)
            )
    else:#continueing straight line motion if there is no wall or obstacles
        if(triggered[2] == 1):#using previos trigger activating the smooting to prevent sudden moents
            await move_xcm_smoother(speed,threshold)#running the smoothener
            triggered[2] = 0#reseting the value to prevent false possitives
        else:#running normallyy after smoothening
            move_xcm(1,speed)
    return triggered[2]#returning value for de bbugging

def color_detection(image): #detecting the color of the path in front
    image = cv.resize(image,(500,500))#resizing to make calc easier
    img = cv.cvtColor(image, cv.COLOR_BGR2HSV)#converting to hsv to make detecting color much much easier
    kernel = np.ones((5, 5), np.uint8)
    imge = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)
    contours = []#storing contors
    color =  0#base color
    while (contours == []):#finding the color
        cmon = [255, 255, 50]#base values used by all the functions to find the color
        image_0 = np.array([color, 1, cmon[2]])#testing all values untill we stumble upon the exact color
        image_1 = np.array([color+1, cmon[0], cmon[1]])
        mask_image = cv.inRange(imge, image_0, image_1)
        contours, hierarchy = cv.findContours(mask_image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        color += 1
    return color

def find_centroid(): #finding the average centroid to follow the curved line and straight line
    values = []#loggging and output varible
    data = camera.getImage() #DO NOT MAKE ANY CHANGE TO THIS LINE
    frame = np.frombuffer(data, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
    gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)#cvt  to  grey to find the contours
    ret, thresh = cv.threshold(gray_image, 127, 255, 0)#finding all the required contours
    M = cv.moments(thresh)#finding the inertial moments of pixels
    cX = int(M["m10"] / M["m00"])#finding the x position of the centroid
    cY = int(M["m01"] / M["m00"])#finding  the y position of the centroid
    values.append([cX, cY])#outputing the cordinates
    average_centroid.write(f'v{str(values)}\n')#loggging the output
    return cX#returning theoutput  used to calc the motion

def find_centroid_v2(): #finding  all the centroids in order to  find the 90 degree turn  NOTE: this is almost the same process only differenc is that in this multiple centroids are found ts i have not comented this  one
    values = []
    data = camera.getImage() #DO NOT MAKE ANY CHANGE TO THIS LINE
    frame = np.frombuffer(data, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
    gray_image = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray_image, 127, 255, 0)
    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    i=0
    for c in contours:
        M = cv.moments(c)
        if(M["m00"]!=0):
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX = int(M["m10"])
            cY = int(M["m01"])
        values.append([cX,cY,i])
        i += 1
    multipe_centroid.write(f'v{str(values)}\n')
    return values

def apply_pid(PX,SPEED):#taking centroid values and checking when to do what
    RADI_var = 150#radius of turning to stay on the track
    time_var = 1#the time for one completion
    if(PX<25):#turning right
        turn_c_radius_degree(time_var,RADI_var,SPEED)
        print(f'turning')
    elif (PX > 25):#turningg left
        turn_ac_radius_degree(time_var,RADI_var,SPEED)
        print(f'turning')
    else:#not changing motion  and continueing going  straight
        move_xcm(1,SPEED)

async def when_to_switch():#algorithm to know when  to switch modes
    await asyncio.sleep(0.0000000000000001)#delay to allow for async to do concurrent processing
    data = camera.getImage()  # DO NOT MAKE ANY CHANGE TO THIS LINE
    frame = np.frombuffer(data, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
    return_value = color_detection(frame)#returning the color
    return return_value

async def sub_function_distance():#running the distance function as a asying batch process along side the camera to prevent the camera from stopping the  wall  following
    await asyncio.sleep(0.0000000000000001)#delay to allow for async to do concurrent processing
    return await run_algorithm_distance(MAX_SPEED,40)#running the algorithm

async def sub_function_camera():#running the camera as a seperate async task so that it  can jam up and  let the ret of the code run
    await asyncio.sleep(0.0000000000000001)#delay to allow for async to do concurrent processing
    return await when_to_switch()

async def main_function():#joining both the sub processes allowing for wf to be executed
    await asyncio.sleep(0.0000000000000001)
    output = await asyncio.gather(
            sub_function_distance(),#distance task
            sub_function_camera()#camera task
        )
    return output

move_xcm(1, MAX_SPEED)#starting the motion
while robot.step(TIMESTEP) != -1:#running whe the programm doesnt stop
    value = asyncio.run(main_function())#running athe wf and collecting outputs
    if(value[1] == 1):#checking if we need to switch modes
        print(f'mode switch')
        turn_ac_degree(30)
        move_xcm(400,MAX_SPEED)
        turn_c_degree(15)
        stop_robot()
        break
chords = [[[12, 30, 0], [0, 0, 1], [30, 13, 2]], [[41, 37, 0], [24, 14, 1]], [[11, 25, 0], [34, 13, 1]], [[39, 26, 0], [17, 13, 1]]]#unique chords of each type of instance
while robot.step(TIMESTEP) != -1:#running while the emulation doesnt stop
    centroid_1 = find_centroid()#checking for straight or curbved line
    centroid_2 = find_centroid_v2()#checking for a 90 degree turn
    apply_pid(centroid_1, MAX_SPEED)#dteering to follow the curved line
    if(centroid_2 == chords[0]):#checking for specific 90 degree
        print('0')
        move_xcm(75,MAX_SPEED)
        turn_ac_degree(90)
        move_xcm(265,MAX_SPEED)
        turn_ac_degree(89)
        stop_robot()
    if(centroid_2 == chords[1]):#checking for specific 90 degree
        print('1')
        move_xcm(70,MAX_SPEED)
        turn_c_degree(90)
        move_xcm(255,MAX_SPEED)
        turn_c_degree(89)
        stop_robot()
    if (centroid_2 == chords[2]):#checking for specific 90 degree
        print('1')
        move_xcm(100, MAX_SPEED)
        turn_ac_degree(90)
        move_xcm(255, MAX_SPEED)
        turn_ac_degree(89)
        stop_robot()
    if (centroid_2 == chords[3]):#checking for specific 90 degree
        print('1')
        move_xcm(100, MAX_SPEED)
        turn_c_degree(90)
        move_xcm(255, MAX_SPEED)
        turn_c_degree(89)
        stop_robot()
multipe_centroid.close()#closing the logging file
average_centroid.close()#closing the logging file