import time
import datetime
import RPi.GPIO as GPIO
import smbus

class Settings:
    	tasterPin = 17


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

class Taster:
    def __init__(self):
        self.pin = Settings.tasterPin

    def get_is_pressed(self):
        return GPIO.input(self.pin)


class Controller:
    def __init__(self):
        self.taster = Taster()
        self.poti = MCP3426(1)
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)     
        GPIO.setup(Settings.tasterPin,GPIO.IN)
    
    def caclulateTurn(self):
        voltage = self.poti.read_ch1()
        voltagePercent = round(((voltage * 100) / 1701),0)/100
        return voltagePercent

    def run(self):
        pressFlag = False
        while True:
            is_pressed = self.taster.get_is_pressed()
            if is_pressed == True and pressFlag == False:
                print("1")
                pressFlag = True
                startTime = time.time()
            elif is_pressed == True and pressFlag == True:
                endTime = time.time()
                if endTime - startTime >= 0.05:
                    startTime = time.time()
                    turn = self.caclulateTurn()
                    print(turn)
            elif is_pressed == False and pressFlag == True:
                pressFlag = False
                print("0")
if __name__ == '__main__':
    main = Controller()
    main.run()
