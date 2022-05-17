import paho.mqtt.client as mqtt
import sqlite3
import datetime

class Settings: 
    BROKER = "localhost"
    BROKER_PORT = 1883
    BROKER_USER = "rw"
    BROKER_PASSWORD = "readwrite"

    TOPIC_FACTORY = "wissenberg/factory/buttons"

class MqttReader:
    def __init__(self):
        self.motor = 0
        self.forward = 0
        self.backward = 0

    def open_db_connection(self):
        try:
            self.con = sqlite3.connect('wissenberg_dab.db')
            self.cur = self.con.cursor()
        except ConnectionError:
            self.open_db_connection()
    
    def writeKommand(self, motor_id, forward, backward):
        self.cur.execute(f"INSERT INTO command (motor_id, vorwaerts, rueckwaerts, timestamp) VALUES ({motor_id}, {forward}, {backward},'{datetime.datetime.now()}');")
        self.con.commit()

    def getRoboId(self,name,position):
        self.cur.execute(f"SELECT motor_id FROM motor WHERE name = '{name}';")
        id = self.cur.fetchone()
        
        if id == None:
            self.cur.execute(f"INSERT INTO motor (name, position) VALUES ('{name}',{position});")
            self.cur.execute(f"SELECT motor_id FROM motor WHERE name = '{name}';")
            id = self.cur.fetchone()
        
        id = str(id)
        id = id.replace(",)","")
        id = id.replace("(","")
        
        return id

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        client.subscribe(Settings.TOPIC_FACTORY)

    def main(self, client, userdata, msg):

        msg = str(msg.payload)
        
        msg = msg.replace("b", "")
        msg = msg.replace("'", "")
        motor, forward, backward  = msg.split("#")  

        if self.motor != motor or self.forward != forward or self.backward != backward:
            self.writeKommand(motor, forward, backward)

        self.motor = motor
        self.forward = forward
        self.backward = backward 
        
    def openListener(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.main

        self.client.connect(host = Settings.BROKER, keepalive = 60)

        self.client.loop_forever()

if __name__ == "__main__":
    mqttR = MqttReader()
    mqttR.open_db_connection()
    mqttR.openListener()