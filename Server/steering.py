import socket
import threading
import keyboard
import time

# Create and bind the server socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", 5000))
s.listen(5)
print("Server is now running, waiting for a connection...")

# Function to listen for keyboard input and send messages
def send_control_signals(clientsocket):
    print("Control keys: [W] Forward, [S] Backward, [A] Left, [D] Right, [Q] Quit")
    try:
        while True:
            if keyboard.is_pressed('w'):
                message = "forward"
                clientsocket.send(bytes(message, "utf-8"))
                print(f"Sent: {message}")
                time.sleep(0.2)

            elif keyboard.is_pressed('s'):
                message = "backward"
                clientsocket.send(bytes(message, "utf-8"))
                print(f"Sent: {message}")
                time.sleep(0.2)

            elif keyboard.is_pressed('x'):
                message = "straight"
                clientsocket.send(bytes(message, "utf-8"))
                print(f"Sent: {message}")
                time.sleep(0.2)

            elif keyboard.is_pressed('a'):
                message = "left"
                clientsocket.send(bytes(message, "utf-8"))
                print(f"Sent: {message}")
                time.sleep(0.2)

            elif keyboard.is_pressed('f'):
                message = "full_left"
                clientsocket.send(bytes(message, "utf-8"))
                print(f"Sent: {message}")
                time.sleep(0.2)

            elif keyboard.is_pressed('d'):
                message = "right"
                clientsocket.send(bytes(message, "utf-8"))
                print(f"Sent: {message}")
                time.sleep(0.2)

            elif keyboard.is_pressed('g'):
                message = "full_right"
                clientsocket.send(bytes(message, "utf-8"))
                print(f"Sent: {message}")
                time.sleep(0.2)

            elif keyboard.is_pressed('q'):
                message = "stop"
                clientsocket.send(bytes(message, "utf-8"))
                print("Quitting control...")
                break
    except Exception as e:
        print(f"Error: {e}")

# Main loop to accept client connections
while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    # Start the keyboard control in a separate thread
    send_control_signals(clientsocket)
