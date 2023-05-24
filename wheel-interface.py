from pwm import PWM_CONTROLLER
from gpio import GPIO_CONTROLLER
from fileWriter import FileWriter

pin_left = 7
pin_right = 11
pwm_left = 32
pwm_right = 33

def main():
    pin_left_controller = GPIO_CONTROLLER(pin_left)
    pin_right_controller = GPIO_CONTROLLER(pin_right)
    pin_right_controller.set_UP() # init Up
    pwm_left_controller = GPIO_CONTROLLER(pwm_left)
    pwm_right_controller = GPIO_CONTROLLER(pwm_right)
    fileR = FileWriter("coucou")

    lastSaved = None
    
    while(True):
        list = fileR.readFile()

        lastElement = list[-1] # [val1(avancer / reculer), val2(gauche / droite)]

        if notTheSame(lastElement, lastSaved):
            if lastElement[0] == 0:
                "stop"
            elif lastElement[0] > 0:
                "avancer"
            else:
                "reculer"

            
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