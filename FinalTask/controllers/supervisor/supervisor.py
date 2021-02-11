"""e-puck-supervisor controller."""
from controller import Supervisor, Robot
import requests
import json

try:
	server_data = requests.get("https://eysrc.e-yantra.org/images/supervisor/task5/data.json").json()
	current_data = {}
	with open('data.json') as json_file:
		current_data=json.load(json_file)
	if server_data['version']>current_data['version']:
		print("New supervisor available, now updating.")
		pyc_data = requests.get(server_data["url"])
		with open('supervisor_module.py','wb') as pyc_file:
			pyc_file.write(pyc_data.content)
		with open('data.json','w') as json_file:
			json.dump(server_data,json_file)
except:
	pass
from supervisor_module import (
	Supervisor_Controller
	)

supervisor = Supervisor()

supervisor_controller = Supervisor_Controller(supervisor) 

while not supervisor.step(32) == -1:
	if not supervisor_controller.check_and_update():
		break

supervisor.simulationSetMode(Supervisor.SIMULATION_MODE_PAUSE)