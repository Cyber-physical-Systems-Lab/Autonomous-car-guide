#import time
#from adafruit_servokit import ServoKit

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
#kit = ServoKit(channels=8)

#servo=14
#while True:
    #a=input("enter:")
    #kit.servo[0].angle=int(a)
#kit.servo[0].angle = 180
#kit.continuous_servo[1].throttle = 1
#time.sleep(1)
#kit.continuous_servo[1].throttle = -1
#time.sleep(1)
#kit.servo[0].angle = 0
#kit.continuous_servo[1].throttle = 0

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

