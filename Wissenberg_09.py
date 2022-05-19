import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import datetime
import time
import sqlite3

class Settings:
    SETUP_MODE = GPIO.BCM
    PIN_LED = 17 # Pin 11
    
    BROKER_PORT = 1884
    BROKER_USER = "rw"
    BROKER_PASSWORD = "readwrite"

    CAR_NAME = "car_Wissenberg"
    BROKER = "localhost"
    BROKER_TOPIC = f"cars/{CAR_NAME}/movement"
            
class MqttReader:
    def __init__(self):
        pass

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        client.subscribe(Settings.BROKER_TOPIC)

    def on_message(self, client, userdata, msg):

        msg = str(msg.payload)
        msg = msg.replace("b'","")
        msg = msg.replace("'","")
        direction, turn = msg.split(",")
        direction = int(direction)
        turn = float(turn) 
        if direction == 0:
            print("stopped")
        elif direction == 1:
            print(f"moving {round(turn,1)}")

    def openListener(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(host = Settings.BROKER, keepalive = 60)

        self.client.loop_forever()         
    
if __name__ == '__main__':
    mqttR = MqttReader()
    mqttR.openListener()