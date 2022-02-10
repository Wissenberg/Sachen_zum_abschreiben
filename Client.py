import paho.mqtt.client as mqtt
import pygame
import time
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



class Mqtt_Writer:
    def __init__(self):
        pass
        
    def openPublisher(self):
        self.publisher = mqtt.Client()
        self.publisher.connect(Settings.BROKER, Settings.BROKER_PORT, keepalive=60)
        self.publisher.loop_start()

class Main:
    
    def __init__(self):
        #self.pub = Mqtt_Writer()
        #self.pub.openPublisher()
        self.pygame = pygame
        self.screen = pygame.display.set_mode((Settings.WIDTH, Settings.HEIGHT))
        self.pygame.display.set_caption(Settings.W_TITLE)
        self.background = self.pygame.image.load(os.path.join(Settings.IMAGES_PATH, "background.png")).convert()
        self.background_rect = self.background.get_rect()
        self.clock = pygame.time.Clock()
        self.direction_x = 0
        self.direction_y = 0

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
            time.sleep(0.1)
            self.screen.blit(self.background, self.background_rect)
            self.pygame.display.flip()
    
    def sendMsg(self):
        if self.direction_x == "1":
            if self.direction_y == "0":
                #self.pub.publisher.publish(Settings.TOPIC_ROBO_MOVEMENT, payload="1,0")
                print("1,0")
            elif self.direction_y == "1":
                #self.pub.publisher.publish(Settings.TOPIC_ROBO_MOVEMENT, payload="1,1")
                print("1,1")
            elif self.direction_y == "-1":
                #self.pub.publisher.publish(Settings.TOPIC_ROBO_MOVEMENT, payload="1,-1")
                print("1,-1")
        elif self.direction_x == "-1":
            if self.direction_y == "0":
                #self.pub.publisher.publish(Settings.TOPIC_ROBO_MOVEMENT, payload="-1,0")
                print("-1,0")
            elif self.direction_y == "1":
                #self.pub.publisher.publish(Settings.TOPIC_ROBO_MOVEMENT, payload="-1,1")
                print("-1,1")
            elif self.direction_y == "-1":   
                #self.pub.publisher.publish(Settings.TOPIC_ROBO_MOVEMENT, payload="-1,-1")
                print("-1,-1")  
        elif self.direction_x == "0":
            #self.pub.publisher.publish(Settings.TOPIC_ROBO_MOVEMENT, payload="0,0")
            print("0,0") 

if __name__ == '__main__':
    main = Main()
    main.run()