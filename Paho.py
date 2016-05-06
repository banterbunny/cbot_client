#!/usr/bin/python3
import sys
import paho.mqtt.client as mqtt
import json
from Driver3 import *

if len(sys.argv) == 2:
    MACHINE_NAME = sys.argv[1]
else:
    print("Usage\nPaho.py machine_name")
    quit()

def on_connect(client, userdata, rc):
    print("Connected!")
    # Connect to CBOT exchange 
    client.subscribe("cbot." + MACHINE_NAME, 0)

def on_message(client, userdata, msg):
    command = msg.payload.decode('utf-8')

    try:
        json.loads(command)
        return
    except Exception:
        pass

    if "@telemetry" in command:
        # Client request telemetry signals
        data = {}
        data['distance'] = getDistance()
        data['temperature'] = getTemperature()
        data['leftsense'] = leftSense()
        data['centersense'] = centerSense()
        data['rightsense'] = rightSense()
        data = json.dumps(data)
        client.publish(MACHINE_NAME + "telemetry", data, 1, True)
    else:
        result = {}
        result['command'] = command
        try:
            exec(command)
            result['status'] = "OK"
            print("Command successful")
        except Exception as ex:
            result['status'] = ex
            print(ex)
        result = json.dumps(result)
        client.publish("result", result, 1, True)

client = mqtt.Client(MACHINE_NAME, False)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(MACHINE_NAME,MACHINE_NAME)
client.connect("banterbun.com", 1883, 60)

client.loop_forever()
