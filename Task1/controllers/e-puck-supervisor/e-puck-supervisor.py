"""e-puck-supervisor controller."""

from controller import Supervisor, Robot
import sys
import math
import json
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from zipfile import ZipFile
supervisor = Supervisor()
pi=math.pi
robot = supervisor.getFromDef("my-e-puck") #Handle to the E-Puck Robot
waypoint = supervisor.getFromDef("waypoint") #Handle to the waypoint

if robot is None:
    sys.stderr.write("No DEF my-e-puck node found in the current world file\n")
    sys.exit(1)
if waypoint is None:
    sys.stderr.write("No DEF waypoint node found in the current world file\n")
    sys.exit(1)

# get the time step of the current world.
TIME_STEP=16

MAX_TIME = 180 #Max time in seconds to complete the simulation after which the simulation would stop automatically

trans_field_robot = robot.getField("translation")
trans_field_waypoint = waypoint.getField("translation")

def return_circle_equation(starting, ending, decrement, x_offset, z_offset, radius):
	temp_list = []
	while not starting<ending:
		temp_list.append([radius*math.cos(starting)+x_offset  ,0.02,radius*math.sin(starting)+z_offset])
		starting-=decrement*pi
	return temp_list
waypoints=[]
waypoints.append([0.4,0.02,0])
waypoints.append([0.35 ,0.02,0])
waypoints.append([0.25 ,0.02,0])
waypoints.append([0.15  ,0.02,0])
waypoints+=return_circle_equation(3.5*pi,2.6*pi,0.1,0,0.15,0.15)
waypoints+=return_circle_equation(2.5*pi,1.6*pi,0.1,0,0,0.3)
waypoints+=return_circle_equation(1.5*pi,0.6*pi,0.1,0,-0.075,0.225)
waypoints+=return_circle_equation(0.5*pi,-0.4*pi,0.1,0,0,0.15)
waypoints.append([-0,0.02,-0.15])
waypoints.append([-0.15,0.02,-0.15])
waypoints.append([-0.3,0.02,-0.15])
waypoints.append([-0.3 ,0.02,0.0])
waypoints.append([-0.3 ,0.02,0.15])
waypoints.append([-0.3  ,0.02,0.3])

tolerance = 0.038 #Tolerance in metres within which the robot and waypoint are accepted to have made a contact

robot_position_time = [] #This list stores lists containing simulation time and position of the robot

team_info = {} #This would store team info, primarily the team ID after reading it from the JSON file
try:
	with open('../../teaminfo.json') as team_file:
	    team_info = json.load(team_file) #Read team information from the file and store it
except:
	supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)
	raise Exception("File not found, please make sure teaminfo.json exists in the parent folder")
	
team_id = team_info['team_id'] #Extract the team ID
if team_id == "IE#1234":
	supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE)
	raise Exception("Please first edit the teaminfo.json file and enter your team ID in place of IE#1234")
	
total_waypoints = len(waypoints) #This stores the total number of waypoints the robot can cover
trans_field_waypoint.setSFVec3f(waypoints.pop()) #Set the initial waypoint here
waypoints_reached = 0 # This stores the number of waypoints covered by the robot
run_completed=False
message_sent = False #This stores the fact if the encrypted coordinates file has been stored and the submit button has been enabled 
remaining_time=MAX_TIME
while supervisor.step(TIME_STEP) != -1:

    
    if not run_completed:                
        values = trans_field_robot.getSFVec3f()
        remaining_time = MAX_TIME - supervisor.getTime()
        supervisor.wwiSendText("update_time:"+str(remaining_time))

        robot_position_time.append([supervisor.getTime(),values])
        if remaining_time<=0: #When time has elapsed 
            run_completed=True #end the run
        setpoint = trans_field_waypoint.getSFVec3f()
        if values[0]>setpoint[0]-tolerance and values[0]<setpoint[0]+tolerance and values[2]>setpoint[2]-tolerance and values[2]<setpoint[2]+tolerance: #Check if robot has reached the current waypoint
            print("Waypoint reached")
            waypoints_reached+=1 #Increment number of waypoints reached
            supervisor.wwiSendText("update_waypoints:"+str(waypoints_reached)) #Update number of waypoints reached on the robot window
        
            if waypoints: #If more waypoints are remaining, pop the next waypoint and update location of the waypoint node
                trans_field_waypoint.setSFVec3f(waypoints.pop()) 
            else: #If all waypoints have been reached
                run_completed=True #End the run
    else: #If run has ended
        if not message_sent: #If closing rituals have not been performed yet
            #First we'll store the coordinates in an encrypted file
            with open("coordinates.bin", "wb") as myfile: #First, we'll open the coordinates file

                public_key = RSA.import_key(open("public.pem").read()) #Reading the public RSA Key
                temp_aes_key = get_random_bytes(16) #Actual data would be encrypted with AES because RSA is slow, so we generate a random AES key

                # Encrypt the session key with the public RSA key
                cipher_rsa = PKCS1_OAEP.new(public_key) #Initialize the PKCS Cipher Suit using OAEP Padding mechanism
                enc_session_key = cipher_rsa.encrypt(temp_aes_key) #Encrypt the temporary AES key with RSA instead of the actual data

                # Encrypt the data with the AES session key
                cipher_aes = AES.new(temp_aes_key, AES.MODE_EAX) #Initialize the AES Cipher
                ciphertext, tag = cipher_aes.encrypt_and_digest(json.dumps(robot_position_time).encode('utf8')) #Encrypt UTF 8 encoded sringified JSON with AES
                [ myfile.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ] #Write the data into the file
            #Now we'll automatically zip the files
            with ZipFile("../../"+team_id+".zip",'w') as myzip: #Create the zip file
                myzip.write('coordinates.bin') #Add the coordinates file
                myzip.write('../e-puck/e-puck.py','e-puck.py') #Add the student's controller code
                myzip.write('../../teaminfo.json','team_info.json') #Add the team_info file
            if remaining_time>0:
                supervisor.wwiSendText("stop") #Sent stop message to the robot window so appropriate message can be displayed
            else:
                supervisor.wwiSendText("time_up")
            message_sent=True #Set Message sent to true
        else: #If closing rituals have been performed 
            break #Break out of the loop

supervisor.simulationSetMode(supervisor.SIMULATION_MODE_PAUSE) #Pause the simulation