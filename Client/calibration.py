#import socket
import time
from gpiozero import PWMOutputDevice

pin=26
motor= PWMOutputDevice(pin,frequency=50)

input("Press enter to send neutral throtle")
print("Nautral throtle sent")
motor.value=0.075
time.sleep(3)

input("Press enter to send max throtle")
print("Max throtle sent")
motor.value=0.1
time.sleep(3)

input("Presss enter to send min throtle")
print("Min throtle sent")
motor.value=0.05
time.sleep(3)

print("Return to neutral")
motor.value=0.075
time.sleep(3)