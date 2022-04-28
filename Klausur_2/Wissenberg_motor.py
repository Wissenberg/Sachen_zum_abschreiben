from turtle import back
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

class Settings: 
    PIN_IN_1 = 17 # Pin 11
    PIN_IN_2 = 27 # Pin 13
    PIN_IN_3 = 23 # Pin 16
    PIN_IN_4 = 24 # Pin 18

    IP_ADDRESS = 'localhost'
    
    BROKER = "localhost"
    BROKER_PORT = 1883
    BROKER_USER = "rw"
    BROKER_PASSWORD = "readwrite"

    TOPIC_FACTORY = "wissenberg/factory/buttons"

class MqttReader:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(Settings.PIN_IN_1, GPIO.OUT)
        GPIO.setup(Settings.PIN_IN_2, GPIO.OUT)
        GPIO.setup(Settings.PIN_IN_3, GPIO.OUT)
        GPIO.setup(Settings.PIN_IN_4, GPIO.OUT)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        client.subscribe(Settings.TOPIC_FACTORY)

    def main(self, client, userdata, msg):

        msg = str(msg.payload)
        
        msg = msg.replace("b", "")
        msg = msg.replace("'", "")
        motor, forward, backward  = msg.split("#")
        #Motor links
        if  motor == '0':
            #Stop
            if forward == "0" and backward == "0" or forward == "1" and backward == "1":
                self.setPinsFalse(Settings.ALL_PINS)
            #Left Forward
            elif forward == "1" and backward == "0":
                self.setPinsFalse([Settings.PIN_IN_1,Settings.PIN_IN_4,Settings.PIN_IN_3])
                GPIO.output(Settings.PIN_IN_2, True)
            #Left Backward
            elif forward == "0" and backward == "1":
                self.setPinsFalse([Settings.PIN_IN_2, Settings.PIN_IN_3, Settings.PIN_IN_4])
                GPIO.output(Settings.PIN_IN_1, True)
        #Motor rechts
        elif motor == "1":
            #Stop
            if forward == "0" and backward == "0" or forward == "1" and backward == "1":
                self.setPinsFalse(Settings.ALL_PINS)
            #Left Forward
            elif forward == "1" and backward == "0":
                self.setPinsFalse([Settings.PIN_IN_1,Settings.PIN_IN_2,Settings.PIN_IN_3])
                GPIO.output(Settings.PIN_IN_4, True)
            #Left Backward
            elif forward == "0" and backward == "1":
                self.setPinsFalse([Settings.PIN_IN_2, Settings.PIN_IN_1, Settings.PIN_IN_4])
                GPIO.output(Settings.PIN_IN_3, True)            
        
    def openListener(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.main

        self.client.connect(host = Settings.BROKER, keepalive = 60)

        self.client.loop_forever()
    
    def setPinsFalse(self, pins):
        for x in pins:
            GPIO.output(x,False)
            
    
if __name__ == '__main__':
    mqttR = MqttReader()
    mqttR.openListener()