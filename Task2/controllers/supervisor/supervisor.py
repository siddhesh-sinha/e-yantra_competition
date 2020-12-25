from controller import Supervisor, Robot
import sys
import math
import json
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from zipfile import ZipFile
import requests
import random
robot = Supervisor()

team_info = {} #This would store team info, primarily the team ID after reading it from the JSON file
try:
	with open('../../teaminfo.json') as team_file:
	    team_info = json.load(team_file) #Read team information from the file and store it
except:
	robot.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)
	raise Exception("File not found, please make sure teaminfo.json exists in the parent folder")
	
team_id = team_info['team_id'] #Extract the team ID
email = team_info['email']
password = team_info['password']
if team_id == "IE#1234" or email == "" or password == "": #If team hasn't changed the default parameters in the teaminfo.json file, show an error
	robot.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)
	raise Exception("Please first edit the teaminfo.json file and enter your team ID in place of IE#1234")

coordinates = {'robot_position_time':[],'box_position':[]}

def normalize(vector):
    length = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2])
    if length == 0:
        return [0, 1, 0]
    else:
        return [vector[0] / length, vector[1] / length, vector[2] / length]

def randomlyPlaceObject(node):
    translationField = node.getField("translation")
    rotationField = node.getField("rotation")

    newPosition = [random.uniform(-0.8,0.8), random.uniform(0.1,0.5), random.uniform(-1.2,1.2)]
    newRotation = normalize([random.random(), random.random(), random.random()]) + [random.random() * math.pi * 2]

    translationField.setSFVec3f(newPosition)
    rotationField.setSFRotation(newRotation)

random.seed()
epuck = robot.getFromDef("EPuck")

timestep = 16

cubeObstaclesGroup = robot.getFromDef("BoxGroup")
cubeObstaclesField = cubeObstaclesGroup.getField("children")
cubeObstaclesCount = cubeObstaclesField.getCount()
cubeObstacles = []
trans_field_robot = epuck.getField("translation")

for x in range(0, cubeObstaclesCount):
    cubeObstacles.append(cubeObstaclesField.getMFNode(x))

running = True
stopMessageSent = False
i = 0
time_remaining=180
progress = 0
while robot.step(timestep) != -1:
    if i < cubeObstaclesCount:
        randomlyPlaceObject(cubeObstacles[i])
        i += 1

    if running:
        time = robot.getTime()
        values = trans_field_robot.getSFVec3f()
        coordinates['robot_position_time'].append([time,values])
        

        # If the robot has collided with something that isn't the ground or has
        # reached the goal or has even run out of time, record final time and
        # terminate simulation.
        progress = (abs(trans_field_robot.getSFVec3f()[2]-1.5)/3.7)*100
        numberofContactPoints = epuck.getNumberOfContactPoints()
        if progress>=100 or time >= 180:
        	running=False
        for x in range(0, numberofContactPoints):
            contactPoint = epuck.getContactPoint(x)
            if contactPoint[1] > 0.02 :
                time = 180
                running = False
                break
        time_remaining = 180 - time
        robot.wwiSendText("update_time:"+str(time_remaining))
        robot.wwiSendText("update_progress:"+str(progress))
    else:  # Wait for record message.
        if not stopMessageSent:
        	#First, let's store position and orientation of all the boxes in the box_position field
            token = ""
            role = ""
            try:
                http_response = requests.post("https://eysrc.e-yantra.org/checkLogin",data=json.dumps({'email':email,'password':password})).json()
                token = http_response['token']
                role = http_response['role']
                if not role == 1:
                    robot.wwiSendText("http_error:Please check your credentials. Please make sure that only team leader's credentials are used")
            except:
                robot.wwiSendText("http_error:Cannot Login, please check your internet connection or credentials")
            if token!= "" and role == 1:
                try:
                    leaderboard_response = requests.post("https://eysrc.e-yantra.org/getTask2Score",data=json.dumps({'hash':token,'score':str(progress+time_remaining)})).text
                    if leaderboard_response=="Done":
                        robot.wwiSendText("http_success:Score submitted")
                    else:
                        robot.wwiSendText("http_error:Some error occured. Please check")
                except:
                    robot.wwiSendText("http_error:Please check your internet connection")
            for cube in cubeObstacles:
                translationField = cube.getField("translation")
                rotationField = cube.getField("rotation")
                translation = translationField.getSFVec3f()
                rotation = rotationField.getSFRotation()
                coordinates['box_position'].append([translation,rotation])
            #Next, we'll store the coordinates in an encrypted file
            with open("coordinates.bin", "wb") as myfile: #First, we'll open the coordinates file
                print("Saving coordinates.bin file")
                public_key = RSA.import_key(open("public.pem").read()) #Reading the public RSA Key
                temp_aes_key = get_random_bytes(16) #Actual data would be encrypted with AES because RSA is slow, so we generate a random AES key

                # Encrypt the session key with the public RSA key
                cipher_rsa = PKCS1_OAEP.new(public_key) #Initialize the PKCS Cipher Suit using OAEP Padding mechanism
                enc_session_key = cipher_rsa.encrypt(temp_aes_key) #Encrypt the temporary AES key with RSA instead of the actual data

                # Encrypt the data with the AES session key
                cipher_aes = AES.new(temp_aes_key, AES.MODE_EAX) #Initialize the AES Cipher
                ciphertext, tag = cipher_aes.encrypt_and_digest(json.dumps(coordinates).encode('utf8')) #Encrypt UTF 8 encoded sringified JSON with AES
                [ myfile.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ] #Write the data into the file
            #Now we'll automatically zip the files
            with ZipFile("../../"+team_id+".zip",'w') as myzip: #Create the zip file
                myzip.write('coordinates.bin') #Add the coordinates file
                myzip.write('../e-puck/e-puck.py','e-puck.py') #Add the student's controller code
                myzip.write('../../teaminfo.json','team_info.json') #Add the team_info file
            if time_remaining>0:
                robot.wwiSendText("stop") #Sent stop message to the robot window so appropriate message can be displayed
            else:
                robot.wwiSendText("time_up")
            stopMessageSent = True
        else:
        	break

robot.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE)
