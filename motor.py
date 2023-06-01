import RPi.GPIO as GPIO
import time
from sshkeyboard import listen_keyboard, stop_listening

POL_LEFT = 7
PWM_LEFT = 33

POL_RIGHT = 11
PWM_RIGHT = 32

class Wheel():

    def __init__(self, pol, pwm, direction):
        self.pin_pol = pol
        self.pin_pwm = pwm
        self.direction = direction
        self.pwm = None 
        self.value_pwm = 20

    def setup(self):
        GPIO.setup(self.pin_pwm, GPIO.OUT)
        GPIO.setup(self.pin_pol, GPIO.OUT, initial=self.direction)
        self.pwm = GPIO.PWM(self.pin_pwm, 100)

    def launch(self):
        self.pwm.start(self.value_pwm)

    def add(self):
        self.value_pwm = min(self.value_pwm + 10, 99)
        self.pwm.ChangeDutyCycle(self.value_pwm)
    
    def sub(self):
        self.value_pwm = max(self.value_pwm - 10, 30)
        self.pwm.ChangeDutyCycle(self.value_pwm)
    
    def forward(self):
        self.value_pwm = 50
        GPIO.output(self.pin_pol, self.direction)
        self.pwm.ChangeDutyCycle(self.value_pwm)
    
    def backward(self):
        self.value_pwm = 50
        GPIO.output(self.pin_pol, 1 if self.direction == 0 else 0)
        self.pwm.ChangeDutyCycle(self.value_pwm)

    def arret(self):
        self.value_pwm = 20
        self.pwm.ChangeDutyCycle(self.value_pwm)


class Robot():

    def __init__(self):
        self.wheel_left = Wheel(POL_LEFT, PWM_LEFT, GPIO.LOW)
        self.wheel_right = Wheel(POL_RIGHT, PWM_RIGHT, GPIO.HIGH)

    def setupAndLaunch(self):
        self.wheel_left.setup()
        self.wheel_right.setup()
        time.sleep(0.5)
        self.wheel_left.launch()
        self.wheel_right.launch()

    def listener(self, e):
        if (e == "i"): self.forward()
        if (e == "j"): self.left()
        if (e == "k"): self.backward()
        if (e == "l"): self.right()
        if (e == "o"): self.stop()

        if (e == "w"): self.forward_auto()
        if (e == "a"): self.left_auto()
        if (e == "s"): self.backward_auto()
        if (e == "d"): self.right_auto()


    def forward(self):
        self.wheel_left.forward()
        self.wheel_right.forward()
        time.sleep(0.3)
        self.stop()

        # self.wheel_left.add()
        # self.wheel_right.add()

    def backward(self):
        self.wheel_left.backward()
        self.wheel_right.backward()
        time.sleep(0.3)
        self.stop()
        # self.wheel_left.sub()
        # self.wheel_right.sub()

    def left(self):
        self.wheel_left.backward()
        self.wheel_right.forward()
        time.sleep(0.2)
        self.stop()
        # self.wheel_left.sub()
        # self.wheel_right.add()

    def right(self):
        self.wheel_left.forward()
        self.wheel_right.backward()
        time.sleep(0.2)
        self.stop()
        # self.wheel_left.add()
        # self.wheel_right.sub()

    def forward_auto(self):
        self.wheel_left.add()
        self.wheel_right.add()

    def backward_auto(self):
        self.wheel_left.sub()
        self.wheel_right.sub()

    def left_auto(self):
        self.wheel_left.sub()
        self.wheel_right.add()

    def right_auto(self):
        self.wheel_left.add()
        self.wheel_right.sub()

    def stop(self):
        self.wheel_left.arret()
        self.wheel_right.arret()

    def clean(self):
        self.wheel_left.pwm.stop()
        self.wheel_right.pwm.stop()

if __name__ == "__main__":


    GPIO.setmode(GPIO.BOARD)

    robot = Robot()

    robot.setupAndLaunch()
    time.sleep(1)
    listen_keyboard(on_press=robot.listener, sequential=True)

    try:
        while True:
            time.sleep(0.4)

    finally:
        robot.clean()
        GPIO.cleanup()


