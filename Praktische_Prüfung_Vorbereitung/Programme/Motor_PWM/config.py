from RPi.GPIO import BCM

ROBO_NAME = "Wissenberg_Robo"
    
BROKER = "localhost"
BROKER_PORT = 1884
BROKER_USER = "rw"
BROKER_PASSWORD = "readwrite"

TOPIC_ROBO_MOVEMENT = f"robos/{ROBO_NAME}/movement"

SETUP_MODE = BCM
PIN_IN_1 = 17 # Pin 11
PIN_IN_2 = 27 # Pin 13
PIN_IN_3 = 23 # Pin 16
PIN_IN_4 = 24 # Pin 18

ALL_PINS = [PIN_IN_1, PIN_IN_2, PIN_IN_3, PIN_IN_4]
    