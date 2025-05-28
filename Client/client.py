import socket
from adafruit_servokit import ServoKit

USER = 1
# Use IP from central PC
SERVER_IP = "192.168.0.219"
SERVER_PORT = 5000
STEERING_CHANNEL = 0

kit = ServoKit(channels=8)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP, SERVER_PORT))
s.sendall(str(USER).encode())

# Wrap socket as file-like object for clean line reading
sock_file = s.makefile("r")

try:
    for line in sock_file:
        data = line.strip()
        try:
            angle = int(data)
            if 48 <= angle <= 132:
                kit.servo[STEERING_CHANNEL].angle = angle
                print(f"Steering angle set to {angle}")
            else:
                print(f"Ignored out-of-range angle: {angle}")
        except ValueError:
            print(f"Invalid angle received: {data}")

except Exception as e:
    print("Client error:", e)

finally:
    s.close()



