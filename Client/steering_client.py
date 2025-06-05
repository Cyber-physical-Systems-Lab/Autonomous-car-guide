from threading import Timer
from adafruit_servokit import ServoKit
import time
from gpiozero import PWMOutputDevice
import socket

USER = 1
pin=26
motor= PWMOutputDevice(pin,frequency=50)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Use the PC (server) IP-adress for connection
s.connect(("192.168.0.219", 5000))
s.sendall(str(USER).encode())

kit = ServoKit(channels=8)

servo=14
motor.value = 0.075

turn_min = 50
turn_max = 130
turn_neutral = 90
turn_change = 5
turn = turn_neutral

speed_min = 0.05
speed_max = 0.1
speed_neutral = 0.075
speed_change = 0.005
speed = speed_neutral

try:
    while True:
        print("Looping")
        data=s.recv(1024)
        if not data:
            break
        
        command = data.decode("utf-8").strip()
        
        if command == "forward":
            print(f"Command = {command}")
            if speed + speed_change <= speed_max:
                speed = speed + speed_change
                motor.value = speed
             
        elif command == "backward":
            print(f"Command = {command}")
            if speed - speed_change >= speed_min:
                speed = speed - speed_change
                motor.value = speed
        
        elif command == "left":
            print(f"Command = {command}")
            if turn - turn_change >= turn_min:
                turn = turn - turn_change
                kit.servo[0].angle = turn
        
        elif command == "full_left":
            print(f"Command = {command}")
            turn = turn_min
            kit.servo[0].angle = turn
            
        elif command == "right":
            print(f"Command = {command}")
            if turn + turn_change <= turn_max:
                turn = turn + turn_change
                kit.servo[0].angle = turn
                
        elif command == "full_right":
            print(f"Command = {command}")
            turn = turn_max
            kit.servo[0].angle = turn
            
        elif command == "straight":
            print(f"Command = {command}")
            turn = turn_neutral
            kit.servo[0].angle = turn
        
        elif command == "stop":
            print(f"Command = {command}")
            speed = speed_neutral
            motor.value = speed
        
        else:
            print(f"Unkown command: {command}")

except Exception as e:
    print(f"Error: {e}")
    
finally:
    s.close()
    print("Diconnecting from server")