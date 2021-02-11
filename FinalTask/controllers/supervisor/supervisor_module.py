"""e-puck-supervisor controller."""
from controller import Supervisor, Robot
import sys
import math
import json
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from zipfile import ZipFile
import random
pi=math.pi

MAX_TIME = 180
tolerance = 0.1
class Supervisor_Controller():
    
    def generate_circular_waypoints(self,starting_angle, ending_angle, number_of_waypoints, center_x, center_z, radius,y_offset,clockwise=True):
        temp_list = []
        multiplier = 1 if clockwise else -1

        for i in range(number_of_waypoints):
            temp_list.append([radius*math.cos(starting_angle + (ending_angle-starting_angle)*i/number_of_waypoints)+center_x , y_offset, multiplier*radius*math.sin(starting_angle + (ending_angle-starting_angle)*i/number_of_waypoints)+center_z])
            
        return temp_list
    def generate_straight_waypoints(self,starting_x, starting_z, ending_x, ending_z, y_offset, number_of_waypoints):
        temp_list = []
        for i in range(number_of_waypoints):
            temp_list.append([starting_x+i*(ending_x-starting_x)/number_of_waypoints,y_offset,starting_z+i*(ending_z-starting_z)/number_of_waypoints])
        return temp_list
    def init_waypoints(self, arena) -> list:
        self.waypoints += self.generate_straight_waypoints(starting_x=0.1,starting_z=2,ending_x=0.1,ending_z=1.5,y_offset=0.175,number_of_waypoints=5)
        self.waypoints += self.generate_circular_waypoints(starting_angle=pi,ending_angle=2*pi,number_of_waypoints=5,center_x=0.5,center_z=1.5,radius=0.35,y_offset=0.175)
        self.waypoints += self.generate_straight_waypoints(starting_x=0.9,starting_z=1.5,ending_x=0.9,ending_z=1.75,y_offset=0.175,number_of_waypoints=5)
        self.waypoints += self.generate_circular_waypoints(starting_angle=0,ending_angle=0.5*pi,number_of_waypoints=5,center_x=0.725,center_z=1.75,radius=0.175,y_offset=0.175)
        #self.waypoints += self.generate_straight_waypoints(starting_x=0.75,starting_z=1.9,ending_x=0.55,ending_z=1.9,y_offset=0.075,number_of_waypoints=5)
        self.waypoints += self.generate_circular_waypoints(starting_angle=0.5*pi,ending_angle=pi,number_of_waypoints=5,center_x=0.525,center_z=1.75,radius=0.175,y_offset=0.1)
        self.waypoints += self.generate_straight_waypoints(starting_x=0.4,starting_z=1.75,ending_x=0.4,ending_z=1.6,y_offset=0.1,number_of_waypoints=5)
        self.waypoints += self.generate_circular_waypoints(starting_angle=pi,ending_angle=1.5*pi,number_of_waypoints=5,center_x=0.5,center_z=1.6,radius=0.1,y_offset=0.1)
        self.waypoints += self.generate_straight_waypoints(starting_x=0.5,starting_z=1.55,ending_x=1.05,ending_z=1.55,y_offset=0.1,number_of_waypoints=5)
        self.waypoints += self.generate_circular_waypoints(starting_angle=1.5*pi,ending_angle=2*pi,number_of_waypoints=5,center_x=1.05,center_z=1.65,radius=0.1,y_offset=0.1)
        self.waypoints += self.generate_circular_waypoints(starting_angle=pi,ending_angle=2*pi+pi/6,number_of_waypoints=5,center_x=1.35,center_z=1.65,radius=0.2,y_offset=0.1,clockwise=False)
        self.waypoints += self.generate_straight_waypoints(starting_x=1.4+math.cos(pi/6)/10-0.025,starting_z=1.65-math.sin(pi/6)/10+0.025,ending_x=1.75-3*math.cos(pi/6)/10-1.5*math.cos(pi/6)/10-0.05,ending_z=1.3+1.25*math.cos(pi/6)/10+0.025,y_offset=0.1,number_of_waypoints=5)
        self.waypoints += self.generate_circular_waypoints(starting_angle=0.5*pi+pi/3,ending_angle=1.5*pi+pi/3,number_of_waypoints=5,center_x=1.75-3*math.cos(pi/6)/10,center_z=1.3,radius=0.1,y_offset=0.1)
        self.waypoints += self.generate_circular_waypoints(starting_angle=pi+pi/6,ending_angle=2*pi,number_of_waypoints=5,center_x=1.75,center_z=1.3-3*math.sin(pi/6)/10,radius=0.2,y_offset=0.1, clockwise=False)
        self.waypoints += self.generate_straight_waypoints(starting_x=1.9,starting_z=1.3-3*math.sin(pi/6)/10,ending_x=1.9,ending_z=1,y_offset=0.1,number_of_waypoints=5)
        
        if arena==1:
            self.waypoints += self.generate_straight_waypoints(starting_x=1.92,starting_z=1,ending_x=1.92,ending_z=0.41,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_circular_waypoints(starting_angle=0,ending_angle=0.5*pi,number_of_waypoints=5,center_x=1.67,center_z=0.41,radius=0.25,y_offset=0.1,clockwise=False)
            self.waypoints += self.generate_straight_waypoints(starting_x=1.67,starting_z=0.16,ending_x=1.17,ending_z=0.16,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_circular_waypoints(starting_angle=0.5*pi,ending_angle=pi,number_of_waypoints=5,center_x=1.17,center_z=0.31,radius=0.15,y_offset=0.1,clockwise=False)
            self.waypoints += self.generate_straight_waypoints(starting_x=1.17,starting_z=0.46,ending_x=1.52,ending_z=0.46,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_circular_waypoints(starting_angle=1.5*pi,ending_angle=2.5*pi,number_of_waypoints=5,center_x=1.52,center_z=0.61,radius=0.15,y_offset=0.1,clockwise=True)
            self.waypoints += self.generate_straight_waypoints(starting_x=1.52,starting_z=0.76,ending_x=1.02,ending_z=0.76,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_circular_waypoints(starting_angle=0.5*pi,ending_angle=pi,number_of_waypoints=5,center_x=1.02,center_z=0.46,radius=0.3,y_offset=0.1,clockwise=True)
            self.waypoints += self.generate_straight_waypoints(starting_x=0.72,starting_z=0.46,ending_x=0.72,ending_z=0.16,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_straight_waypoints(starting_x=0.72,starting_z=0.16,ending_x=0.42,ending_z=0.16,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_straight_waypoints(starting_x=0.42,starting_z=0.16,ending_x=0.42,ending_z=0.76,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_straight_waypoints(starting_x=0.42,starting_z=0.76,ending_x=0.12,ending_z=0.76,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_straight_waypoints(starting_x=0.12,starting_z=0.76,ending_x=0.12,ending_z=0.05,y_offset=0.1,number_of_waypoints=5)
        
        else:
            self.waypoints += self.generate_straight_waypoints(starting_x=1.92,starting_z=1,ending_x=1.92,ending_z=0.3,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_circular_waypoints(starting_angle=0,ending_angle=pi,number_of_waypoints=5,center_x=1.77,center_z=0.3,radius=0.15,y_offset=0.1,clockwise=False)
            self.waypoints += self.generate_straight_waypoints(starting_x=1.62,starting_z=0.3,ending_x=1.62,ending_z=0.65,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_circular_waypoints(starting_angle=0,ending_angle=pi,number_of_waypoints=5,center_x=1.47,center_z=0.65,radius=0.15,y_offset=0.1,clockwise=True)
            self.waypoints += self.generate_straight_waypoints(starting_x=1.32,starting_z=0.65,ending_x=1.32,ending_z=0.45,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_circular_waypoints(starting_angle=0,ending_angle=0.5*pi,number_of_waypoints=5,center_x=1.07,center_z=0.45,radius=0.25,y_offset=0.1,clockwise=False)
            self.waypoints += self.generate_straight_waypoints(starting_x=1.07,starting_z=0.2,ending_x=0.42,ending_z=0.2,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_straight_waypoints(starting_x=0.42,starting_z=0.2,ending_x=0.42,ending_z=0.5,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_straight_waypoints(starting_x=0.42,starting_z=0.5,ending_x=1.02,ending_z=0.5,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_straight_waypoints(starting_x=1.02,starting_z=0.5,ending_x=1.02,ending_z=0.8,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_straight_waypoints(starting_x=1.02,starting_z=0.8,ending_x=0.42,ending_z=0.8,y_offset=0.1,number_of_waypoints=5)
            self.waypoints += self.generate_circular_waypoints(starting_angle=0.5*pi,ending_angle=pi,number_of_waypoints=5,center_x=0.42,center_z=0.5,radius=0.3,y_offset=0.1,clockwise=True)
            self.waypoints += self.generate_straight_waypoints(starting_x=0.12,starting_z=0.5,ending_x=0.12,ending_z=0.05,y_offset=0.1,number_of_waypoints=5)
        

        self.waypoints.reverse()
        return self.waypoints
    # def init_waypoints(self) -> list:
    #     self.waypoints += self.generate_straight_waypoints(starting_x=0.1,starting_z=2,ending_x=0.1,ending_z=1.5,y_offset=0.075,number_of_waypoints=5)
    #     self.waypoints += self.generate_circular_waypoints(starting_angle=pi,ending_angle=2*pi,number_of_waypoints=5,center_x=0.5,center_z=1.5,radius=0.4,y_offset=0.075)
    #     self.waypoints += self.generate_straight_waypoints(starting_x=0.9,starting_z=1.5,ending_x=0.9,ending_z=1.75,y_offset=0.075,number_of_waypoints=5)
    #     self.waypoints += self.generate_circular_waypoints(starting_angle=0,ending_angle=0.5*pi,number_of_waypoints=5,center_x=0.75,center_z=1.75,radius=0.15,y_offset=0.075)
    #     #self.waypoints += self.generate_straight_waypoints(starting_x=0.75,starting_z=1.9,ending_x=0.55,ending_z=1.9,y_offset=0.075,number_of_waypoints=5)
    #     self.waypoints += self.generate_circular_waypoints(starting_angle=0.5*pi,ending_angle=pi,number_of_waypoints=5,center_x=0.55,center_z=1.75,radius=0.15,y_offset=0.02)
    #     self.waypoints += self.generate_straight_waypoints(starting_x=0.4,starting_z=1.75,ending_x=0.4,ending_z=1.6,y_offset=0.02,number_of_waypoints=5)
    #     self.waypoints += self.generate_circular_waypoints(starting_angle=pi,ending_angle=1.5*pi,number_of_waypoints=5,center_x=0.5,center_z=1.6,radius=0.1,y_offset=0.02)
    #     self.waypoints += self.generate_straight_waypoints(starting_x=0.5,starting_z=1.5,ending_x=1.05,ending_z=1.5,y_offset=0.02,number_of_waypoints=5)
    #     self.waypoints += self.generate_circular_waypoints(starting_angle=1.5*pi,ending_angle=2*pi,number_of_waypoints=5,center_x=1.05,center_z=1.65,radius=0.15,y_offset=0.02)
    #     self.waypoints += self.generate_circular_waypoints(starting_angle=pi,ending_angle=2*pi+pi/6,number_of_waypoints=5,center_x=1.35,center_z=1.65,radius=0.15,y_offset=0.02,clockwise=False)
    #     self.waypoints += self.generate_straight_waypoints(starting_x=1.4+math.cos(pi/6)/10,starting_z=1.65-math.sin(pi/6)/10,ending_x=1.75-3*math.cos(pi/6)/10-1.5*math.cos(pi/6)/10,ending_z=1.3+1.5*math.cos(pi/6)/10,y_offset=0.02,number_of_waypoints=5)
    #     self.waypoints += self.generate_circular_waypoints(starting_angle=0.5*pi+pi/3,ending_angle=1.5*pi+pi/3,number_of_waypoints=5,center_x=1.75-3*math.cos(pi/6)/10,center_z=1.3,radius=0.15,y_offset=0.02)
    #     self.waypoints += self.generate_circular_waypoints(starting_angle=pi+pi/6,ending_angle=2*pi,number_of_waypoints=5,center_x=1.75,center_z=1.3-3*math.sin(pi/6)/10,radius=0.15,y_offset=0.02, clockwise=False)
    #     self.waypoints += self.generate_straight_waypoints(starting_x=1.9,starting_z=1.3-3*math.sin(pi/6)/10,ending_x=1.9,ending_z=1,y_offset=0.02,number_of_waypoints=5)
    #     self.waypoints.reverse()
    #     return self.waypoints
    
    def get_robot_fields(self):
        self.robot = self.supervisor.getFromDef("my-e-puck")
        
        if self.robot is None:
            sys.stderr.write("No DEF my-e-puck node found in the current world file\n")
            sys.exit(1)
        
        self.translation_field_robot = self.robot.getField("translation")
        
    def get_waypoint_fields(self):
        self.waypoint = self.supervisor.getFromDef("waypoint")
        
        if self.waypoint is None:
            sys.stderr.write("No DEF waypoint node found in the current world file\n")
            sys.exit(1)
        
        self.translation_field_waypoint = self.waypoint.getField("translation")
 
    def get_team_info(self):
        self.team_info = {} #This would store team info, primarily the team ID after reading it from the JSON file
        try:
            with open('../../teaminfo.json') as team_file:
                self.team_info = json.load(team_file) #Read team information from the file and store it
        except:
            self.supervisor.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE)
            raise Exception("File not found, please make sure teaminfo.json exists in the parent folder")
            
        self.team_id = self.team_info['team_id'] #Extract the team ID
        self.email = self.team_info['email']
        self.password = self.team_info['password']
        if self.team_id == "IE#1234" or self.email == "" or self.password == "": #If team hasn't changed the default parameters in the teaminfo.json file, show an error
            self.supervisor.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE)
            raise Exception("Please first edit the teaminfo.json file and enter your team ID in place of IE#1234")

    def update_waypoint(self, new_position) -> list:
        self.translation_field_waypoint.setSFVec3f(new_position)
        self.waypoint_location=new_position
        return self.waypoint_location 

    def init_random_lf_arena(self) -> int:
        self.arena = random.randint(1,3)
        floor = self.supervisor.getFromDef("LFFloorApr").getField("url")
        if self.arena == 1:
            floor.setMFString(0,'textures/LF_1.png')
        else:
            floor.setMFString(0,'textures/LF_2.png')
        return self.arena

    def __init__(self,supervisor):
        self.supervisor=supervisor
        self.remaining_time = MAX_TIME
        self.waypoints_reached = 0
        self.run_completed = False
        self.message_sent = False #Represents message sent to robot window
        self.robot_position_time=[]
        self.waypoints = []
        self.init_waypoints(self.init_random_lf_arena())
        self.get_robot_fields()
        self.get_waypoint_fields()
        self.get_team_info()
        self.update_waypoint(self.waypoints.pop())
    

    def update_remaining_time(self,time) -> float:
        self.remaining_time = MAX_TIME-time
        return self.remaining_time

    def check_waypoint_reached(self) -> bool:
        if self.robot_location[0]>self.waypoint_location[0]-tolerance and self.robot_location[0]<self.waypoint_location[0]+tolerance and self.robot_location[2]>self.waypoint_location[2]-tolerance and self.robot_location[2]<self.waypoint_location[2]+tolerance: #Check if robot has reached the current waypoint
            print("Waypoint reached")
            self.waypoints_reached+=1 #Increment number of waypoints reached
            return True
        else:
            return False

    def check_collission(self) -> bool:
        numberofContactPoints = self.robot.getNumberOfContactPoints()
        for x in range(0, numberofContactPoints):
            contactPoint = self.robot.getContactPoint(x)
            
            if contactPoint[1] > 0.005+self.robot_location[1]:# - 0.013 :

                return True
        return False

   
    def update_robot_location(self) -> list:
        self.robot_location = self.translation_field_robot.getSFVec3f()
        return self.robot_location

    def update_robot_window(self,error_message="", success_message = ""):
        self.supervisor.wwiSendText("update_waypoints:"+str(self.waypoints_reached))
        self.supervisor.wwiSendText("update_time:"+str(self.remaining_time))
        if error_message:
            self.supervisor.wwiSendText("error:"+error_message)
        if success_message:
            self.supervisor.wwiSendText("success:"+success_message) 

    def save_coordinates_file(self,data):
        with open("coordinates.bin", "wb") as myfile: #First, we'll open the coordinates file
            public_key = RSA.import_key(open("public.pem").read()) #Reading the public RSA Key
            temp_aes_key = get_random_bytes(16) #Actual data would be encrypted with AES because RSA is slow, so we generate a random AES key
            # Encrypt the session key with the public RSA key
            cipher_rsa = PKCS1_OAEP.new(public_key) #Initialize the PKCS Cipher Suit using OAEP Padding mechanism
            enc_session_key = cipher_rsa.encrypt(temp_aes_key) #Encrypt the temporary AES key with RSA instead of the actual data
            # Encrypt the data with the AES session key
            cipher_aes = AES.new(temp_aes_key, AES.MODE_EAX) #Initialize the AES Cipher
            ciphertext, tag = cipher_aes.encrypt_and_digest(json.dumps(data).encode('utf8')) #Encrypt UTF 8 encoded sringified JSON with AES
            [ myfile.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext) ] #Write the data into the file
    
    def save_zip_file(self):
        with ZipFile("../../"+self.team_id+".zip",'w') as myzip: #Create the zip file
            myzip.write('coordinates.bin') #Add the coordinates file
            myzip.write('../e-puck/e-puck.py','e-puck.py') #Add the student's controller code
            myzip.write('../../teaminfo.json','teaminfo.json') #Add the team_info file
    
    def check_remaining_time(self) -> bool:
        if self.remaining_time<=0:
            return False
        else:
            return True
    
    def check_and_update(self) -> bool:
        self.success_message = ""
        self.error_message = ""
        if not self.run_completed:
            self.robot_position_time.append([self.update_robot_location(),self.update_remaining_time(self.supervisor.getTime())])
            if not self.check_remaining_time():
                self.run_completed=True
            if self.check_waypoint_reached():
                if self.waypoints:
                    self.update_waypoint(self.waypoints.pop())
                else:
                    self.run_completed=True
            if self.check_collission():
                self.update_remaining_time(MAX_TIME)
                self.run_completed=True
        else:
            if not self.message_sent:
                self.save_coordinates_file(self.robot_position_time)
                self.save_zip_file()
                if self.remaining_time>0:
                    self.success_message = "Zip file successfully saved to the parent folder"
                else:
                    self.error_message = "Time is up"
                self.message_sent=True
            else:
                return False
        self.update_robot_window(self.error_message,self.success_message)        
        return True