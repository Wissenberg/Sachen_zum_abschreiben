import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import datetime
import time
import sqlite3

class Settings:
    SETUP_MODE = GPIO.BCM
    PIN_LED = 17 # Pin 11
    
    BROKER = "localhost"
    BROKER_PORT = 1884
    BROKER_USER = "rw"
    BROKER_PASSWORD = "readwrite"

    BROKER_TOPIC = f"poti-werte"


class DBMapper:
    def __init__(self, databaseName):
        self.databaseName = databaseName
        self.open_db_connection()

    def open_db_connection(self):
        '''Öffnet eine Verbindung zur Datenbank, die beim Objekterzeugen angegeben wurde. (databaseName)'''
        try:
            self.con = sqlite3.connect(self.databaseName)
            self.cur = self.con.cursor()
            print("Erfolgreich Verbunden!")
        except ConnectionError as err:
            print(err)
            self.open_db_connection()   

    def insertIntoDatabase(self, sqlQuery):
        '''Führt eine sqlQuery aus. Die sqlQuery sollte ein INSERT oder UPDATE sein.
            Beispiel: sqlQuery = f"INSERT INTO test (Spalte1, Spalte2, Spalte3) VALUES (Inhalt-Spalte1,Inhalt-Spalte2,Inhalt-Spalte3);"
        '''
        print(sqlQuery)
        self.cur.execute(sqlQuery)
        self.con.commit()
    

    def getFromDatabase(self, sqlQuery):
        ''' Gibt alle Zeilen zurück, die der SQL-Befehl liefert.
            =>  sqlQuery = SQL-Befehl
            Beispiel: sqlQuery = f"SELECT * FROM test  WHERE ID = 5;"        
        '''
        data = []

        self.cur.execute(sqlQuery)
        rows = self.cur.fetchall()

        for x in rows:
            data.append(x)

        return data
            
class MqttReader:
    def __init__(self):
        self.voltage = 1
        self.oldVoltage = 0
        
        GPIO.BCM
        GPIO.setmode(Settings.SETUP_MODE)
        GPIO.setup(Settings.PIN_LED, GPIO.OUT)

        self.ledPWM = GPIO.PWM(Settings.PIN_LED, 50)
        self.ledPWM.start(0)

        self.db = DBMapper("eintrag.db")

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        client.subscribe(Settings.BROKER_TOPIC)

    def on_message(self, client, userdata, msg):

        msg = str(msg.payload)
        print(msg)
        speed, voltage = msg.split(",")
        print(speed, voltage)
        self.ledPWM.ChangeDutyCycle(speed)
        # Wenn die oldVoltage und Voltage unterschiedlich sind, ist die if-Abfrage True und der Code in der if-Abfrage wird ausgeführt.
        if self.oldVoltage != voltage:
            self.db.insertIntoDatabase(f"INSERT INTO command (time_stamp,spannunghoehe) VALUES ('{datetime.datetime.now()}',{voltage});")
            self.oldVoltage = voltage

    def openListener(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(host = Settings.BROKER, keepalive = 60)

        self.client.loop_forever()         
    
if __name__ == '__main__':
    mqttR = MqttReader()
    mqttR.openListener()