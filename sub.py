import paho.mqtt.client as mqtt

class Subscriber:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.onSubscribeTopic
        self.client.on_message = self.printMessages
        self.client.connect("localhost", 1883)
        
    def onSubscribeTopic(self, client, userdata, flags, rc):
        self.client.subscribe(self.topic)
        print("Connected. Subscribing to topic", self.topic)
    
    def printMessages(self, client, userdata, msg):
        print("Message received: ", msg.topic, msg.payload)

    def subscribeTopic(self, topic):
        self.client.subscribe(topic)

if __name__ == '__main__':
    sub = Subscriber()
    sub.subscribeTopic("sensor/time")
    sub.subscribeTopic("sensor/status")    

