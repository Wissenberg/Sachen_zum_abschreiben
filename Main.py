import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
from config import *

class Settings:
    ROBO_NAME = "Wissenberg_Robo"
    
    BROKER = "localhost"
    BROKER_PORT = 1884
    BROKER_USER = "rw"
    BROKER_PASSWORD = "readwrite"

    TOPIC_ROBO_MOVEMENT = f"robos/{ROBO_NAME}/movement"

    SETUP_MODE = GPIO.BCM
    PIN_IN_1 = 17 # Pin 11
    PIN_IN_2 = 27 # Pin 13
    PIN_IN_3 = 23 # Pin 16
    PIN_IN_4 = 24 # Pin 18
    
    ALL_PINS = [PIN_IN_1, PIN_IN_2, PIN_IN_3, PIN_IN_4]

class MqttReader:
    def __init__(self):
        GPIO.setmode(SETUP_MODE)
        GPIO.setup(PIN_IN_1, GPIO.OUT)
        GPIO.setup(PIN_IN_2, GPIO.OUT)
        GPIO.setup(PIN_IN_3, GPIO.OUT)
        GPIO.setup(PIN_IN_4, GPIO.OUT)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        client.subscribe(TOPIC_ROBO_MOVEMENT)

    def on_message(self, client, userdata, msg):

        msg = str(msg.payload)
        
        msg = msg.replace("b","")
        msg = msg.replace("'","")
        move1, move2 = msg.split(",")
        if move1 == '0':
            #Stop
            self.setPinsFalse(ALL_PINS)
        #Forward
        elif move1 == '1':
            if move2 == '0':
                self.setPinsFalse([PIN_IN_1, PIN_IN_3])
                GPIO.output(PIN_IN_2, True)
                GPIO.output(PIN_IN_4, True)
                
            elif move2 == '1':
                #Right
                self.setPinsFalse([PIN_IN_1,PIN_IN_2,PIN_IN_3])
                GPIO.output(PIN_IN_4, True)
                
            elif move2 == '-1':
                #Left
                self.setPinsFalse([PIN_IN_1, PIN_IN_3, PIN_IN_4])
                GPIO.output(PIN_IN_2, True)
        #Backward
        elif move1 == '-1':
            if move2 == '0':
                #Straight
                self.setPinsFalse([PIN_IN_2, PIN_IN_4])
                GPIO.output(PIN_IN_1, True)
                GPIO.output(PIN_IN_3, True)
            elif move2 == '1':
                #Right
                self.setPinsFalse([PIN_IN_1, PIN_IN_2, PIN_IN_4])
                GPIO.output(PIN_IN_3,True)
            elif move2 == '-1':
                #Left
                self.setPinsFalse([PIN_IN_2, PIN_IN_3, PIN_IN_4])
                GPIO.output(PIN_IN_1, True)


    def openListener(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(host = BROKER, keepalive = 60)

        self.client.loop_forever()
    
    def setPinsFalse(self, pins):
        for x in pins:
            GPIO.output(x,False)
            
    
if __name__ == '__main__':
    mqttR = MqttReader()
    mqttR.openListener()