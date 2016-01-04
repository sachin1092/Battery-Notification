import sys
import pyttsx
import time
import requests
import json
from constants import *

path = "/sys/class/power_supply/BAT1/"
level = "capacity"
status = "status"
headers = {
            'Authorization': 'key=%s' % API_KEY,
            'Content-Type': 'application/json'
        }

def notify(charge, bat_level):
	msg = charge[0].upper() + charge[1:] + " at " + str(bat_level) + "%"
	print "[" + str(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())) + "]:"
	print msg
	print "*"*50
	engine = pyttsx.init()
	engine.say(msg)
	engine.runAndWait()
	data = {'title': 'Jarvis Status', 'body': msg}
	message = {'registration_ids': [reg_id], 'data': data}
	r = requests.post('https://android.googleapis.com/gcm/send', headers=headers, data=json.dumps(message))

if __name__ == "__main__":
	while True:
		bat_level = 0
		charge = ""
		with open(path + level, 'r') as f:
			bat_level = int(f.readline().strip())
		with open(path + status, 'r') as f:
			charge = f.readline().strip()
		if bat_level == 35 or bat_level == 20 or bat_level <= 15:
			notify(charge, bat_level)

		time.sleep(900)
