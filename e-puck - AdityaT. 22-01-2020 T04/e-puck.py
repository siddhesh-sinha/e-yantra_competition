from controller import Robot, Motor
from controller import Camera
import cv2
import numpy as np
import math

timestep = 32
MAX_SPEED = 6.28
v = 1*MAX_SPEED #You can tweak it if you want
R = 20.5 # In mm
pi=math.pi

TURN_90_Degree = (703, 3.00199999999999999999999999999999999999999999999999999999999999999)

robot = Robot()

camera = Camera('camera') #Use this to get image from the camera using getImage Function
camera.enable(timestep)

leftMotor = robot.getMotor('left wheel motor')
rightMotor = robot.getMotor('right wheel motor')
leftMotor.setPosition(float('inf'))
rightMotor.setPosition(float('inf'))
leftMotor.setVelocity(0.0)
rightMotor.setVelocity(0.0)

def go_back(length):
    t = length / (v*R)
    leftMotor.setVelocity(-v)
    rightMotor.setVelocity(-v)
    robot.step(int(t*1000))

#go_back(5)

def go_straight(length):
    t = length / (v*R)
    leftMotor.setVelocity(v)
    rightMotor.setVelocity(v)
    robot.step(int(t*1000))

def turn_c_degree(time_move, SPEED):#to turn clockwise
    leftMotor.setVelocity(SPEED)
    rightMotor.setVelocity(-SPEED)
    print (SPEED)
    robot.step(time_move)

def turn_ac_degree(time_move, SPEED):#to turn anti-clockwise
    leftMotor.setVelocity(-SPEED)
    rightMotor.setVelocity(SPEED)
    print (SPEED)
    robot.step(time_move)

def MorphAsClosing(src, n):
    kernel = np.ones((n,n),np.uint8)
    morph = cv2.morphologyEx(src,cv2.MORPH_CLOSE,kernel) 
    return morph

def color_detection(src): #Remember to put actual argument names in place  of arg1 arg2, you can have more or less than 2 arguments

    src=cv2.resize(src,(600,600))
    morph=MorphAsClosing(src, 5)

    img_hsv=cv2.cvtColor(morph, cv2.COLOR_BGR2HSV)

    # DETECTING GREEN 
    lower_green = np.array([45, 150, 50])
    upper_green = np.array([65, 255, 255])
    mask_green=cv2.inRange(img_hsv, lower_green, upper_green)
    contours, _ = cv2.findContours(mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
            area = cv2.contourArea(contour) 
            if(area > 300): 
                print('GREEN')
                return 'GREEN'

    # DETECTING BLUE
    lower_blue = np.array([95, 150, 0])
    upper_blue = np.array([120, 255, 255])
    mask_blue=cv2.inRange(img_hsv, lower_blue, upper_blue)
    contours, _ = cv2.findContours(mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours: 
            area = cv2.contourArea(contour) 
            if(area > 300): 
                print('BLUE')
                return 'BLUE'

def shape_detection(src): #Remember to put actual argument names in place  of arg1 arg2, you can have more or less  than 2 arguments

    src=cv2.resize(src,(800,800))
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    morph=MorphAsClosing(gray, 5)
    
    _ , threshold = cv2.threshold(morph, 140, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:

        approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)

        sides=len(approx)
        
        if sides == 3:
            print("Triangle")
            return 3
        elif sides == 4:
            print("Square")
            return 4
        elif sides == 5:
            print("Pentagon")
            return 5
        elif 8 <= sides < 15:
            print("Circle")
            return 2

def move_epuck(shape,color):
    """
    Write your actuator code here
    """  

    n=shape

    if color!=None:
        if color=='BLUE':
            turn_ac_degree(TURN_90_Degree[0], TURN_90_Degree[1])
        elif color=='GREEN':
            turn_c_degree(TURN_90_Degree[0], TURN_90_Degree[1])
    
    if n!=None:
        if n>=2 and n<=5:
            dist = 0.15 * n
            go_straight(dist)

    return True  
            
            
###################################################
#Here write the code you want to execute just once
##################################################

while robot.step(timestep) != -1:
    frame = camera.getImage(); 
    img = np.frombuffer(frame, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4)) #img contains the image obtained from the camera, use this to write rest of your code
    #DO NOT MODIFY THE ABOVE 2 LINES
    ##############################################
    #Here write code you want to execute repeatedly
    color = color_detection(img) #Remember to pass the necessary arguments as defined in the function definition 
    shape = shape_detection(img) #Remember to pass the necessary arguments as defined in the function definition 
    move_epuck(shape,color)
    ###############################################
       
        