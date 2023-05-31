from sshkeyboard import listen_keyboard, stop_listening
import time


def listener(e):
    if (e == "i"): print("Avance")
    if (e == "j"): print("Gauche")
    if (e == "k"): print("Recule")
    if (e == "l"): print("Droite")


listen_keyboard(on_press=listener, sequential=True)
try:
    while True:
        time.sleep(0.25)
finally:
    print("aled") 