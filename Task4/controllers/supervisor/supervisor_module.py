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
tolerance = 0.038
class Supervisor_Controller():
        
    def init_random_configuration(self) -> list:
        self.shapes = [2,3,4,5,2,4] # 2 = circle, 3 = triangle, 4 = square, 5 = pentagon
        self.configuration.append({'waypoint_position':[0,0,0],'box_position':[0,0.025,-0.15],'box_rotation':[0,1,0,-math.pi/2],'box_texture':""})
        horizontal_left = -1
        vertical_left = 1
        while self.shapes:
            distance = self.shapes.pop(random.randrange(len(self.shapes)))
            configuration = self.configuration[-1]
            direction = random.choice([-1,1])
            self.configuration[-1]['box_texture'] = self.texture_folder+str(int(direction*distance))+'.jpg'
            if configuration['waypoint_position'][0] == configuration['box_position'][0]:
                vertical_left = direction*horizontal_left
                self.configuration.append({'waypoint_position':[configuration['waypoint_position'][0]-direction*horizontal_left*distance*0.15,configuration['waypoint_position'][1],configuration['waypoint_position'][2]],'box_position':[configuration['waypoint_position'][0]-direction*horizontal_left*(distance+1)*0.15,configuration['waypoint_position'][1],configuration['waypoint_position'][2]],'box_rotation':[0,1,0,configuration['box_rotation'][3]-direction*math.pi/2],'box_texture':""}) 
            else:
                horizontal_left = -1*direction*vertical_left
                self.configuration.append({'waypoint_position':[configuration['waypoint_position'][0],configuration['waypoint_position'][1],configuration['waypoint_position'][2]-direction*vertical_left*distance*0.15],'box_position':[configuration['waypoint_position'][0],configuration['waypoint_position'][1],configuration['waypoint_position'][2]-direction*vertical_left*(distance+1)*0.15],'box_rotation':[0,1,0,configuration['box_rotation'][3]-direction*math.pi/2],'box_texture':""})
        self.configuration.reverse()                    
        return self.configuration

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

    def get_box_fields(self):
        self.box = self.supervisor.getFromDef("box")
        self.texture_box = self.supervisor.getFromDef("texture_shape")
        
        if self.box is None:
            sys.stderr.write("No DEF box node found in the current world file\n")
            sys.exit(1)
        
        self.translation_field_box = self.box.getField("translation")
        self.rotation_field_box = self.box.getField("rotation")
        self.texture_field_box = self.texture_box.getField("textureUrl")
 
    def get_team_info(self) -> dict:
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
        return self.team_info

    def update_waypoint(self, new_position) -> list:
        self.translation_field_waypoint.setSFVec3f(new_position)
        self.waypoint_location=new_position
        return self.waypoint_location 

    def update_box_position_rotation_texture(self,position:list,rotation:list,texture:str):
        self.translation_field_box.setSFVec3f(position)
        self.rotation_field_box.setSFRotation(rotation)
        self.texture_field_box.setMFString(0,texture)

    def __init__(self,supervisor):
        self.supervisor=supervisor
        self.remaining_time = MAX_TIME
        self.waypoints_reached = 0
        self.run_completed = False
        self.message_sent = False #Represents message sent to robot window
        self.waypoints = []
        self.configuration = []
        self.texture_folder = "textures/"
        self.coordinates = {'robot_position_time':[],'configuration':self.init_random_configuration().copy()}
        self.get_robot_fields()
        self.get_waypoint_fields()
        self.get_box_fields()
        self.get_team_info()
        self.update_waypoint(self.configuration[-1]['waypoint_position'])
    

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
            myzip.write('../../teaminfo.json','team_info.json') #Add the team_info file
    
    def check_remaining_time(self) -> bool:
        if self.remaining_time<=0:
            return False
        else:
            return True
    
    def check_and_update(self) -> bool:
        self.success_message = ""
        self.error_message = ""
        if not self.run_completed:
            self.coordinates['robot_position_time'].append([self.update_robot_location(),self.update_remaining_time(self.supervisor.getTime())])
            if not self.check_remaining_time():
                self.run_completed=True
            if self.check_waypoint_reached():
                if self.configuration and self.configuration[-1]['box_texture']:
                    configuration = self.configuration.pop()
                    self.update_box_position_rotation_texture(configuration['box_position'],configuration['box_rotation'],configuration['box_texture'])
                    self.update_waypoint(self.configuration[-1]['waypoint_position'])
                else:
                    self.run_completed=True
            if self.check_collission():
                self.update_remaining_time(MAX_TIME)
                self.run_completed=True
        else:
            if not self.message_sent:
                self.save_coordinates_file(self.coordinates)
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