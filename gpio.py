import Jetson.GPIO as GPIO

class GPIO_CONTROLLER():

    def __init__(self, pin):
        self.output_pin = pin
        if self.output_pin is None:
            raise Exception('PWM not supported on this board')
        pass
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin,GPIO.OUT, initial=GPIO.LOW)

    def set_UP(self):
        GPIO.output(self.output_pin, GPIO.HIGH)
    def set_DOWN(self):
        GPIO.output(self.output_pin, GPIO.LOW)
    
    def clean(self):
        GPIO.cleanup()
        GPIO.setmode(GPIO.BOARD)