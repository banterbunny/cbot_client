#!/usr/bin/python3
import pika
import json
import subprocess
from Driver3 import *

class TopicBased:
    channel = None

    def __init__(self, machine_name):
        self.machine_name = machine_name
        self.getChannel()

        self.channel.queue_bind(exchange='cbot', queue=machine_name, routing_key='cbot.{}'.format(machine_name))
        self.channel.basic_consume(self.on_request, no_ack=True, queue=machine_name)
        self.channel.start_consuming()

    def getChannel(self, returnNone=True):
        # Turn off LED first
        print("Starting connection to server...")
        offLED()

        # Try to connect to the server
        try:
            cred = pika.PlainCredentials(self.machine_name, self.machine_name)
            param = pika.ConnectionParameters("banterbun.com", 5672, "/", cred)
            conn = pika.BlockingConnection(param)
            chan = conn.channel()
            print("Connection established!")
            onLED()
            self.channel = chan
        except Exception as exp:
            if not returnNone:
                print("No connection, rebooting")
                subprocess.call("/sbin/reboot", shell=True)
            else:
                print(type(exp))
                print("Connection error, retrying...")
                self.getChannel()

    def on_request(self, ch, method, props, body):
        returnValue = {}

        print(body)

        # Determine if it is requested from someone
        if props.reply_to is not None:
            resName = props.reply_to
            senses = {}
            senses.update({"leftsense": leftSense()})
            senses.update({"centersense": centerSense()})
            senses.update({"rightsense": rightSense()})
            senses.update({"distance": getDistance()})
            senses.update({"temperature": getTemperature()})
            telemetry = json.dumps(senses)
            self.channel.basic_publish(exchange="", routing_key=resName, body=telemetry)
            return  # Return back to reality

        try:
            exec(body)
            returnValue.update({"status":True})
            print("Command successful")
        except Exception as ex:
            returnValue.update({"status": False, "exception": repr(ex)})
            print(ex)
        self.channel.basic_publish(exchange="cbot", routing_key="cbot.result", body=json.dumps(returnValue))

if __name__ == "__main__":
    tb = TopicBased("cbot1")
    chan = TopicBased.getChannel(True)

