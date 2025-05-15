import socket
import time
from threading import Timer
from adafruit_servokit import ServoKit

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Use the PC (server) IP-adress for connection
s.connect(("192.168.0.219", 5000))

kit = ServoKit(channels=8)

servo=14

while True:
    #print(s.recv(1024).decode("utf-8"))
    a = s.recv(1024).decode("utf-8")
    print(a)
    kit.servo[3].angle=int(a)
    kit.servo[0].angle=int(a)