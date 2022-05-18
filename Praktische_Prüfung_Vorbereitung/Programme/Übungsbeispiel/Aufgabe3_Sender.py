import paho.mqtt.client as mqtt
import time
import smbus
import RPi.GPIO as GPIO 
import os


class Settings:
    BROKER = "localhost"
    BROKER_PORT = 1884
    BROKER_USER = "rw"
    BROKER_PASSWORD = "readwrite"

    BROKER_TOPIC = f"poti-werte"


class MCP3426:
    def __init__(self, busnumber):
        assert busnumber in [0, 1]
        self.busnumber = busnumber
        self.slave_address = 0x68
        self.smbus = smbus.SMBus(1)

    def _swap_bytes(self, word):
        """ swap the two bytes of the given word
            example: word = 0xABCD -> return 0xCDAB """
        return ((word << 8) & 0xFF00) + (word >> 8)

    def _two_complement(self, word):
        """ convert the given word in two's complement to an integer with 
        sign """
        if (word >= 0x8000):
            return -((0xFFFF - word) + 1)
        else:
            return word

    def read_ch1(self):
        """ read the signal-value of channel 1 from the MCP3426
            and return the voltage in volt """
        rdwo = self.smbus.read_word_data(self.slave_address, 0x00)
        word = self._swap_bytes(rdwo)
        voltage = self._two_complement(word)
        return voltage

class Mqtt_Writer:
    def __init__(self):
        pass
        
    def openPublisher(self):
        self.publisher = mqtt.Client()
        self.publisher.connect(Settings.BROKER, keepalive=60)
        self.publisher.loop_start()

class Main:
    
    def __init__(self):
        self.pub = Mqtt_Writer()
        self.poti = MCP3426(1)
        self.pub.openPublisher()
    
    def calculateSpeed(self):
        #So kriegst du die Spannung vom Poti
        voltage = self.poti.read_ch1()
        print(voltage)
        #                                       Max. Spannung    
        voltagePercent = round(((voltage * 100) / 1687),0)/100
        #voltagePercent = voltage * 100
        #print(voltagePercent)
        #voltagePercent = voltagePercent /1687
        #print(voltagePercent)
        #voltagePercent = round(voltagePercent, 0)
        #print(voltagePercent)
        #voltagePercent = voltagePercent / 100
        #print(voltagePercent)
        return voltagePercent, voltage

    def run(self):
        done = False
        oldVoltage = 0
        while not done: 
            speed, voltage = self.calculateSpeed()      
            
            if oldVoltage != voltage:    
                self.pub.publisher.publish(Settings.BROKER_TOPIC, payload=f"{speed},{voltage}")
                oldVoltage = voltage



if __name__ == '__main__':
    main = Main()
    main.run()