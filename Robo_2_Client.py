import paho.mqtt.client as mqtt
import pygame
import time
import smbus
import RPi.GPIO as GPIO 
import os


class Settings:
    ROBO_NAME = "Wissenberg_Robo"
    IP_ADDRESS = 'localhost'
    
    BROKER = "localhost"
    BROKER_PORT = 1883
    BROKER_USER = "rw"
    BROKER_PASSWORD = "readwrite"

    TOPIC_ROBO_MOVEMENT = "robos/Wissenberg_Robo/movement"

    WIDTH = 854
    HEIGHT = 480

    W_TITLE = "Robo"
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGES_PATH = os.path.join(FILE_PATH, "images")

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
        self.mcp3426 = MCP3426(1)
        self.pub.openPublisher()
        self.pygame = pygame
        self.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
        self.pygame.display.set_caption(Settings.W_TITLE)
        self.background = self.pygame.image.load(os.path.join(Settings.IMAGES_PATH, "background.png")).convert()
        self.background_rect = self.background.get_rect()
        self.clock = pygame.time.Clock()
        self.direction_x = 0
        self.direction_y = 0
    
    def calculateSpeed(self):
        self.voltagePercent = self.mcp3426.read_ch1()
        self.voltagePercent = round(((self.voltagePercent * 100) / 1687),0)/100
        #print(self.voltagePercent)
        return self.voltagePercent

    def run(self):
        done = False
        while not done:           
            for event in self.pygame.event.get():   
                if event.type == self.pygame.QUIT:  
                    done = True
                elif event.type == self.pygame.KEYDOWN:
                    if event.key == self.pygame.K_ESCAPE:
                        done = True
                    if event.key == self.pygame.K_w:
                        self.direction_x = "1"
                    if event.key == self.pygame.K_d:
                            self.direction_y = "1" 
                    if event.key == self.pygame.K_a:
                            self.direction_y = "-1"

                    if event.key == self.pygame.K_s: 
                        self.direction_x = "-1"
                    if event.key == self.pygame.K_d:
                            self.direction_y = "1"
                    if event.key == self.pygame.K_a:
                            self.direction_y = "-1"

                elif event.type == self.pygame.KEYUP:
                    if event.key == self.pygame.K_w:
                        self.direction_x = "0"
                    if event.key == self.pygame.K_s:
                        self.direction_x = "0"
                    if event.key == self.pygame.K_d:
                        self.direction_y = "0"
                    
                    if event.key == self.pygame.K_a:
                        self.direction_y = "0"
                self.sendMsg()
            time.sleep(0.01)
            self.screen.blit(self.background, self.background_rect)
            self.pygame.display.flip()
    
    def sendMsg(self):
        speed = self.calculateSpeed()
        print(speed, self.direction_x, self.direction_y)
        if self.direction_x == "1":
            if self.direction_y == "0":
                self.pub.publisher.publish(Settings.TOPIC_ROBO_MOVEMENT, payload=f"{speed},0")
                print(f"{speed},0")
            elif self.direction_y == "1":
                self.pub.publisher.publish(Settings.TOPIC_ROBO_MOVEMENT, payload=f"{speed},1")
                print(f"{speed},1")
            elif self.direction_y == "-1":
                self.pub.publisher.publish(Settings.TOPIC_ROBO_MOVEMENT, payload=f"{speed},-1")
                print(f"{speed},-1")
        elif self.direction_x == "-1":
            if self.direction_y == "0":
                self.pub.publisher.publish(Settings.TOPIC_ROBO_MOVEMENT, payload=f"-{speed},0")
                print(f"-{speed},0")
            elif self.direction_y == "1":
                self.pub.publisher.publish(Settings.TOPIC_ROBO_MOVEMENT, payload=f"-{speed},1")
                print(f"-{speed},1")
            elif self.direction_y == "-1":   
                self.pub.publisher.publish(Settings.TOPIC_ROBO_MOVEMENT, payload=f"-{speed},-1")
                print(f"-{speed},-1")  
        elif self.direction_x == "0":
            self.pub.publisher.publish(Settings.TOPIC_ROBO_MOVEMENT, payload="0,0")
            print("0,0") 

if __name__ == '__main__':
    main = Main()
    main.run()