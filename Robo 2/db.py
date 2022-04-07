import paho.mqtt.client as mqtt
import sqlite3
import datetime
from config import *

class Settings:
    ROBO_NAME = "Robo"
    IP_ADDRESS = '10.1.48.69'
    
    BROKER = "localhost"
    BROKER_PORT = "1884"
    BROKER_USER = "rw"
    BROKER_PASSWORD = "readwrite"

    TOPIC_ROBO_MOVEMENT = f"robos/{ROBO_NAME}/movement"

    PIN_IN_1 = 17 # Pin 11
    PIN_IN_2 = 27 # Pin 13
    PIN_IN_3 = 23 # Pin 16
    PIN_IN_4 = 24 # Pin 18
    
    ALL_PINS = [PIN_IN_1, PIN_IN_2, PIN_IN_3, PIN_IN_4]

class DBMapper:
    def __init__(self):
        self.open_db_connection()

    def open_db_connection(self):
        try:
            self.con = sqlite3.connect('robo.db')
            self.cur = self.con.cursor()
        except ConnectionError:
            self.open_db_connection()   

    def writeKommand(self, robo_id, move, turn):
        self.cur.execute(f"INSERT INTO kommando (robo_id, received_at, move, turn) VALUES ({robo_id},'{datetime.datetime.now()}',{move},{turn});")
        self.con.commit()
    
    def getRoboId(self,name,topic):
        self.cur.execute(f"SELECT robo_id FROM robo WHERE name = '{name}';")
        id = self.cur.fetchone()
        
        if id == None:
            self.cur.execute(f"INSERT INTO robo (name, topic) VALUES ('{name}','{topic}');")
            self.cur.execute(f"SELECT robo_id FROM robo WHERE name = '{name}';")
            id = self.cur.fetchone()
            
        return id

    def getKommandos(self):
        data = []

        self.cur.execute(f"SELECT * FROM kommando;")
        rows = self.cur.fetchall()

        for x in rows:
            data.append(x)

        return data

class MqttReader:
    def __init__(self):
        self.db = DBMapper()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        client.subscribe(TOPIC_ROBO_MOVEMENT)

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        msg = str(msg.payload)
        
        msg = msg.replace("b", "")
        msg = msg.replace("'", "")
        move1, move2 = msg.split(",")
        
        move1 = float(move1)
        robo_id = self.db.getRoboId(ROBO_NAME, topic)
        self.db.writeKommand(robo_id, move1, move2)


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