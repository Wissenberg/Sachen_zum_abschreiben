import RPi.GPIO as GPIO

class Settings:
    SETUP_MODE = GPIO.BCM
    PIN_IN_1 = 17 # Pin 11
    PIN_IN_2 = 27 # Pin 13
    PIN_IN_3 = 23 # Pin 16
    PIN_IN_4 = 24 # Pin 18

class Main:
    def __init__(self):
        GPIO.cleanup()
        GPIO.setmode(Settings.SETUP_MODE)
        GPIO.setup(Settings.PIN_IN_1, GPIO.OUT)
        GPIO.setup(Settings.PIN_IN_2, GPIO.OUT)
        GPIO.setup(Settings.PIN_IN_3, GPIO.OUT)
        GPIO.setup(Settings.PIN_IN_4, GPIO.OUT)

    def straightForward(self):
        GPIO.output(Settings.PIN_IN_2, True)
        GPIO.output(Settings.PIN_IN_4, True)

    def right(self):
        GPIO.output(Settings.PIN_IN_4, True)

    def left(self):
        GPIO.output(Settings.PIN_IN_2, True)
        
    def back(self):
        GPIO.output(Settings.PIN_IN_1, True)
        GPIO.output(Settings.PIN_IN_3, True)
    
    def turn(self):
        GPIO.output(Settings.PIN_IN_4, True)
        GPIO.output(Settings.PIN_IN_1, True)
    
    def stop(self):
        GPIO.output(Settings.PIN_IN_1, False)
        GPIO.output(Settings.PIN_IN_2, False)
        GPIO.output(Settings.PIN_IN_3, False)
        GPIO.output(Settings.PIN_IN_4, False)

    def askForInput(self):
        userInput = input("sf = Vorwärts | r = rechts Kurve | l = links Kurve | b = rückwärts | Drehen = d | s = stop: ")

        if userInput == "sf":
            self.straightForward()
        elif userInput == "r":
            self.right()
        elif userInput == "l":
            self.left()
        elif userInput == "b":
            self.back()
        elif userInput == "s":
            self.stop()
        elif userInput == "d":
            self.turn()
    
    def run(self):
        try:
            while True:
                self.askForInput()
        
        except KeyboardInterrupt:
            self.stop()
            GPIO.cleanup()

if __name__ == '__main__':
    main = Main()
    main.run()