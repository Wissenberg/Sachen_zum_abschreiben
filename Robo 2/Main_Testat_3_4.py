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

        self.pwmPin1 = GPIO.PWM(PIN_IN_1, 50)
        self.pwmPin2 = GPIO.PWM(PIN_IN_2, 50)
        self.pwmPin3 = GPIO.PWM(PIN_IN_3, 50)
        self.pwmPin4 = GPIO.PWM(PIN_IN_4, 50)

        self.pwmPin1.start(0)
        self.pwmPin2.start(0)
        self.pwmPin3.start(0)
        self.pwmPin4.start(0)

        self.allPwmPins = [self.pwmPin1,self.pwmPin2,self.pwmPin3,self.pwmPin4]

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        client.subscribe(TOPIC_ROBO_MOVEMENT)

    def on_message(self, client, userdata, msg):

        msg = str(msg.payload)
        
        msg = msg.replace("b","")
        msg = msg.replace("'","")
        move1, move2 = msg.split(",")
        move1 = float(move1)
        move1 = min(max(-0.8,move1),0.8)

        print(f"move: {move1}, turn: {move2}")

        if move1 == 0.0:
            #Stop
            self.setPinsFalse(self.allPwmPins)
        #Forward
        elif move1 >= 0.0:
            move1 = move1 * 100
            if move2 == '0':
                self.setPinsFalse([self.pwmPin1, self.pwmPin3])
                self.pwmPin2.ChangeDutyCycle(move1)
                self.pwmPin4.ChangeDutyCycle(move1)
                
            elif move2 == '1':
                #Right
                self.setPinsFalse([self.pwmPin1,self.pwmPin2,self.pwmPin3])
                self.pwmPin4.ChangeDutyCycle(move1)
                
            elif move2 == '-1':
                #Left
                self.setPinsFalse([self.pwmPin1,self.pwmPin3, self.pwmPin4])
                self.pwmPin2.ChangeDutyCycle(move1)
        #Backward
        elif move1 <= 0.0:
            move1 = move1 * -100
            if move2 == '0':
                #Straight
                self.setPinsFalse([self.pwmPin2,self.pwmPin4])
                self.pwmPin1.ChangeDutyCycle(move1)
                self.pwmPin3.ChangeDutyCycle(move1)
            elif move2 == '1':
                #Right
                self.setPinsFalse([self.pwmPin1, self.pwmPin2,self.pwmPin4])
                self.pwmPin3.ChangeDutyCycle(move1)
            elif move2 == '-1':
                #Left
                self.setPinsFalse([self.pwmPin2, self.pwmPin3,self.pwmPin4])
                self.pwmPin1.ChangeDutyCycle(move1)


    def openListener(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(host = BROKER, keepalive = 60)

        self.client.loop_forever()
    
    def setPinsFalse(self, pins):
        for x in pins:
             x.ChangeDutyCycle(0)
            
    
if __name__ == '__main__':
    mqttR = MqttReader()
    mqttR.openListener()