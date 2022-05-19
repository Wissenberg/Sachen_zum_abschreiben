import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import datetime
import time
import sqlite3

class Settings:
    SETUP_MODE = GPIO.BCM
    
    CAR_NAME = "car_Wissenberg"
    BROKER = "localhost"
    BROKER_TOPIC = f"cars/{CAR_NAME}/movement"

    PIN_IN_1 = 22 # Pin 11
    PIN_IN_2 = 27 # Pin 13
    PIN_IN_3 = 23 # Pin 16
    PIN_IN_4 = 24 # Pin 18

    ALL_PINS = [PIN_IN_1, PIN_IN_2, PIN_IN_3, PIN_IN_4]
            
class MqttReader:
    def __init__(self):
        GPIO.setmode(Settings.SETUP_MODE)
        GPIO.setup(Settings.PIN_IN_1, GPIO.OUT)
        GPIO.setup(Settings.PIN_IN_2, GPIO.OUT)
        GPIO.setup(Settings.PIN_IN_3, GPIO.OUT)
        GPIO.setup(Settings.PIN_IN_4, GPIO.OUT)

        self.pwmPin1 = GPIO.PWM(Settings.PIN_IN_1, 50)
        self.pwmPin2 = GPIO.PWM(Settings.PIN_IN_2, 50)
        self.pwmPin3 = GPIO.PWM(Settings.PIN_IN_3, 50)
        self.pwmPin4 = GPIO.PWM(Settings.PIN_IN_4, 50)

        self.pwmPin1.start(0)
        self.pwmPin2.start(0)
        self.pwmPin3.start(0)
        self.pwmPin4.start(0)

        self.allPwmPins = [self.pwmPin1,self.pwmPin2,self.pwmPin3,self.pwmPin4]

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
        motorL = min((2*turn),1)
        motorR = min((-2*turn+2),1)
        print(f"Motor-Links: {motorL} | Motor-Rechts: {motorR}")
        if direction == 0:
            #Stop
            self.setPinsFalse(self.allPwmPins)
        #Forward
        elif direction == 1:
            self.setPinsFalse([self.pwmPin1, self.pwmPin3])
            self.pwmPin2.ChangeDutyCycle((motorL*100))
            self.pwmPin4.ChangeDutyCycle((motorR*100))

    def setPinsFalse(self, pins):
        for x in pins:
             x.ChangeDutyCycle(0)        

    def openListener(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(host = Settings.BROKER, keepalive = 60)

        self.client.loop_forever()         
    
if __name__ == '__main__':
    mqttR = MqttReader()
    mqttR.openListener()