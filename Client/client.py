import socket
import time
from threading import Timer

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("",5000))

while True:
    print(s.recv(1024).decode("utf-8"))