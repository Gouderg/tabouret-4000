from pwm import PWM_CONTROLLER
from gpio import GPIO_CONTROLLER
from fileWriter import FileWriter
import time
import RPi.GPIO as GPIO

pin_left = 7
pin_right = 11
pwm_left = 33
pwm_right = 32

def main():
    GPIO.setmode(GPIO.BOARD)

    pin_left_controller = GPIO_CONTROLLER(pin_left)
    pin_right_controller = GPIO_CONTROLLER(pin_right)
    pin_left_controller.set_UP() # init Up
    pwm_left_controller = PWM_CONTROLLER(pwm_left)
    pwm_right_controller = PWM_CONTROLLER(pwm_right)
    fileR = FileWriter("coucou")

    lastSaved = None
    
    while(True):
        time.sleep(0.4)
        list = fileR.readFile()
        if len(list) > 0:
            print(list)
            lastElement = list[-1] # [val1(avancer / reculer), val2(gauche / droite)]

            if notTheSame(lastElement, lastSaved):
                speed_left = 0
                speed_right = 0
                direction = 1

                if lastElement[0] == 0:
                    "stop"
                elif lastElement[0] > 0:
                    "avancer"
                    speed_left = 33*lastElement[0]
                    speed_right = 33*lastElement[0]
                else:
                    "reculer"
                    speed_left = abs(33*lastElement[0])
                    speed_right = abs(33*lastElement[0])
                    direction = 0
                

                if lastElement[1] == 0:
                    "ahead"
                elif lastElement[1] > 0:
                    "right"
                    if direction == 1:
                        speed_left -= 15*lastElement[1]
                        speed_right += 15*lastElement[1]
                    else:
                        speed_left += 15*lastElement[1]
                        speed_right -= 15*lastElement[1]
                else:
                    "left"
                    if direction == 1:
                        speed_left += abs(15*lastElement[1])
                        speed_right -= abs(15*lastElement[1])
                    else:
                        speed_left -= abs(15*lastElement[1])
                        speed_right += abs(15*lastElement[1])

                if lastElement[0] == 0 and (speed_left != 0 or speed_right != 0):
                    "stop"
                    speed_left *= 2
                    speed_right *= 2

                reverse_left = 0
                reverse_right = 0

                if speed_left < 0:
                    speed_left = 30 + abs(speed_left)
                    reverse_left = 1
                if speed_right < 0:
                    speed_right = 30 + abs(speed_right)
                    reverse_right = 1
                
                if direction == 1:
                    if reverse_left == 1:
                        pin_left_controller.set_UP()
                    else:
                        pin_left_controller.set_DOWN()

                    if reverse_right == 1:
                        pin_right_controller.set_DOWN()
                    else:
                        pin_right_controller.set_UP()

                else:
                    if reverse_left == 1:
                        pin_left_controller.set_DOWN()
                    else:
                        pin_left_controller.set_UP()

                    if reverse_right == 1:
                        pin_right_controller.set_UP()
                    else:
                        pin_right_controller.set_DOWN()

                if speed_left > 100:
                    speed_left = 100
                if speed_right > 100:
                    speed_right = 100 

                pwm_left_controller.run(speed_left)
                pwm_right_controller.run(speed_right)

                lastSaved = lastElement





def notTheSame(el1, el2):
    if el1 != None and el2 != None:
        if el1[0] == el2[0] and el1[1] == el2[1]:
            return False
        else:
            return True
    else:
        return True

main()