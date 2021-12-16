import paho.mqtt.client as mqtt
import time

publisher = mqtt.Client()
publisher.connect("localhost", 1883, keepalive=60)
publisher.loop_start()

while True:
    publisher.publish(topic="sensor/time",payload= time.time())
    publisher.publish(topic="sensor/status",payload="ok")
