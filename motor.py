import RPi.GPIO as GPIO
import time
import keyboard

POL_LEFT = 11
PWM_LEFT = 32

POL_RIGHT = 7
PWM_RIGHT = 33

class Wheel():

    def __init__(self, pol, pwm, direction):
        self.pin_pol = pol
        self.pin_pwm = pwm
        self.direction = direction
        self.pwm, self.value_pwm = None, 50

    def setup(self):
        GPIO.setup(self.pin_pwm, GPIO.OUT)
        GPIO.setup(self.pin_pol, GPIO.OUT, initial=self.direction)
        self.pwm = GPIO.PWM(self.pin_pwm, 100)

    def launch(self):
        self.pwm.start(self.value_pwm)

    def add(self):
        self.value_pwm = min(self.value_pwm + 1, 99)
        self.pwm.ChangeDutyCycle(self.value_pwm)
    
    def sub(self):
        self.value_pwm = max(self.value_pwm - 1, 30)
        self.pwm.ChangeDutyCycle(self.value_pwm)


class Robot():

    def __init__(self):
        self.wheel_left = Wheel(POL_LEFT, PWM_LEFT, GPIO.LOW)
        self.wheel_right = Wheel(POL_RIGHT, PWM_RIGHT, GPIO.HIGH)

    def setupAndLaunch(self):
        self.wheel_left.setup()
        self.wheel_right.setup()
        time.sleep(1)
        self.wheel_left.launch()
        self.wheel_right.launch()


    def forward(self, e):
        self.wheel_left.add()
        self.wheel_right.add()

    def backward(self, e):
        self.wheel_left.sub()
        self.wheel_right.sub()

    def left(self, e):
        self.wheel_left.sub()
        self.wheel_right.add()

    def right(self, e):
        self.wheel_left.add()
        self.wheel_right.sub()
    
    def clean(self):
        self.wheel_left.pwm.stop()
        self.wheel_right.pwm.stop()

if __name__ == "__main__":


    GPIO.setmode(GPIO.BOARD)

    robot = Robot()

    robot.setupAndLaunch()

    keyboard.on_press_key("i", robot.forward)
    keyboard.on_press_key("j", robot.left)
    keyboard.on_press_key("k", robot.backward)
    keyboard.on_press_key("l", robot.right)

    try:
        while True:
            time.sleep(1)

    finally:
        robot.clean()
        GPIO.cleanup()


