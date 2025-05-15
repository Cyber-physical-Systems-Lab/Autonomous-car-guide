import socket
import time
from threading import Timer

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("",5000))
s.listen(5)
print("server is now running")

def background_controller():
    message = input("enter:")
    print(message)
    clientsocket.send(bytes(message, "utf-8"))   
    Timer(1, background_controller).start()

# def speed_controller():


while True:
    clientsocket, address=s.accept()
    print(f"connection from {address} has been established")
    background_controller()
    # speed_controller()