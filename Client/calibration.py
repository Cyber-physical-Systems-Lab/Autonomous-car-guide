#import socket
import time
from gpiozero import PWMOutputDevice

pin=26
motor= PWMOutputDevice(pin,frequency=50)

input("sending neutral throtle")
print("nautral throtle sent")

motor.value=0.075
time.sleep(3)
input("sending max throtle")
print("max throtle sent")
motor.value=0.1
time.sleep(3)

input("sending minl throtle")
print("min throtle sent")
motor.value=0.05
time.sleep(3)

print("return to neutral")
motor.value=0.075
time.sleep(3)

print("test")
motor.value=0.085
time.sleep(3)

print("return to neutral")
motor.value=0.075
time.sleep(3)

