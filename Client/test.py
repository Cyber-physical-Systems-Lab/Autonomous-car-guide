import time
from gpiozero import PWMOutputDevice
pin=26
motor= PWMOutputDevice(pin,frequency=50)
print("return to neutral")
motor.value=0.075
time.sleep(3)
print("forward")
motor.value=0.080
time.sleep(3)


print("return to neutral")
motor.value=0.075
time.sleep(4)

print("reverse")
motor.value=0.065
time.sleep(3)


print("return to neutral")
motor.value=0.075
time.sleep(3)

