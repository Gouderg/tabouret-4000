import Jetson.GPIO as GPIO

class PWM_CONTROLLER():

    def __init__(self, pin):
        self.output_pin = pin
        if self.output_pin is None:
            raise Exception('PWM not supported on this board')
        pass
        self.consigne = 0
        # Pin Setup:
        # Board pin-numbering scheme
        
        GPIO.setmode(GPIO.BOARD)
        # set pin as an output pin with optional initial state of HIGH
        GPIO.setup(self.output_pin, GPIO.OUT, initial=GPIO.HIGH)
        self.setup()

    def run(self, consigne):
        if consigne == -1 :
            print("Fin du programme")
            self.p.stop()
            GPIO.cleanup()
            return
        else:
            self.consigne = consigne      
            self.p.ChangeDutyCycle(self.consigne)
            
    def setup(self):
        self.p = GPIO.PWM(self.output_pin, 30)
        self.p.start(0)
        print("Setup GPIO terminé\n")

