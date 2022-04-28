import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

class Settings:
    LED_1_PIN = 25
    LED_2_PIN = 8

    TASTER_1_PIN = 0
    TASTER_2_PIN = 5
    TASTER_3_PIN = 6

    IP_ADDRESS = 'localhost'
    
    BROKER = "localhost"
    BROKER_PORT = 1883
    BROKER_USER = "rw"
    BROKER_PASSWORD = "readwrite"

    TOPIC_FACTORY = "wissenberg/factory/buttons"



class Led:
    def __init__(self):
        self.led_1_pin = Settings.LED_1_PIN
        self.led_2_pin = Settings.LED_2_PIN 
        self.led_1_on = True
        self.led_2_on = False

        GPIO.output(self.led_1_pin, True)

    def toggle_led(self):
        if self.led_1_on == True:
            self.led_1_on = False
            GPIO.output(self.led_1_pin, False)
        elif self.led_1_on == False:
            self.led_1_on = True
            GPIO.output(self.led_1_pin, True)

        if self.led_2_on == True and:
            self.led_2_on = False
            GPIO.output(self.led_2_pin, False)
        elif self.led_2_on == False:
            self.led_2_on = True
            GPIO.output(self.led_2_pin, True)            

    def get_led_on(self):
        return self.led_1_on, self.led_2_on

class Taster:
    def __init__(self):
        self.pin_1 = Settings.TASTER_1_PIN
        self.pin_2 = Settings.TASTER_2_PIN
        self.pin_3 = Settings.TASTER_3_PIN
        self.pins = [self.pin_1, self.pin_2, self.pin_3]
        self.is_pressed = []
    
    def get_is_pressed(self):
        self.is_pressed = []
        for x in self.pins:
            taster_value = GPIO.input(x)
            self.is_pressed.append(taster_value)
            return self.is_pressed

class Mqtt_Writer:
    def __init__(self):
        pass
        
    def openPublisher(self):
        self.publisher = mqtt.Client()
        self.publisher.connect(Settings.BROKER, keepalive=60)
        self.publisher.loop_start()

class Controller:
    def __init__(self):
        self.led = Led()
        self.taster = Taster()
        self.mqttW = Mqtt_Writer()
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led.led_1_pin,GPIO.OUT)
        GPIO.setup(self.led.led_2_pin,GPIO.OUT)
        GPIO.setup(self.taster.pin_1, GPIO.IN)


    def run(self):
        done = False
        self.mqttW.openPublisher()
        oldCommands = "0#0#0"
        engine = 1

        while not done:
            is_pressed = self.taster.get_is_pressed()
            indexOfx = 0
            engine = 0
            forward = 0
            backward = 0
            for x in is_pressed:
                if indexOfx == 0:
                    if x == True and engine == 0:
                        self.led.toggle_led()
                        commands = "1#"
                        engine = 1
                    elif x == True and engine == 1:
                        self.led.toggle_led()
                        commands = "0#" 
                        engine = 0
                elif indexOfx == 1:
                    if x == True and forward == 0:
                        commands = f"{commands}1#"
                        forward = 1
                    elif x == True and forward == 1: 
                        commands = f"{commands}0#"
                        forward = 0
                elif indexOfx == 2:
                    if x == True and backward == 0:
                        commands = f"{commands}1"
                        backward = 1
                    elif x == True and backward == 1: 
                        commands = f"{commands}0"   
                        backward = 0                 
                indexOfx += 1
    
            if oldCommands != commands:
                self.mqttW.publisher.publish(Settings.TOPIC_FACTORY, payload=commands)
            
            oldCommands = commands
   
if __name__ == '__main__':
    main = Controller()
    main.run()
