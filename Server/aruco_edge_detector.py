import cv2
import cv2.aruco as aruco
import numpy as np
import socket
import threading
import time

# ==== Socket Setup ====
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", 5000))  # Bind to all interfaces on port 5000
server_socket.listen(5)
print("Server started. Waiting for RC vehicles to connect...")

# ==== Changeable Parameters ====
# Minimum angle change required to send a new command
ANGLE_THRESHOLD = 1
# Distance to consider a point "to close"
LOW_THRESHOLD = 40
HIGH_THRESHOLD = 80
# Minimum time between messages to a vehicle (seconds)
SEND_INTERVAL = 0.2 
# Scale for turn intensity
SCALE = 0.2


# ==== State Tracking ====
# Track connected vehicles by ID and store last sent data
user_sockets = {}
last_sent_angles = {}
last_send_times = {}


# ==== Connection Handling ====
def handle_new_connections():
    """
    Listens for and accepts incoming TCP client connections.

    Each connected client is expected to send a user ID as the first message.
    The function maps the client socket to this user ID and stores it in the
    `user_sockets` dictionary.

    This function is designed to run in a background thread and loops indefinitely.
    """
    while True:
        clientsocket, address = server_socket.accept()
        ip = address[0]
        try:
            clientsocket.settimeout(5.0)
            user_data = clientsocket.recv(1024)
            if not user_data:
                raise ValueError("No data received.")
            user_id = int(user_data.decode().strip())
            user_sockets[user_id] = clientsocket
            print(f"Mapped IP {ip} to user ID {user_id}")
        except Exception as e:
            print(f"Failed to receive user ID from {ip}: {e}")
            clientsocket.close()



# ==== Angle and Steering ====
def estimate_heading(corners):
    """
    Estimates the heading angle of an ArUco marker.

    Parameters:
        corners (np.ndarray): Array of 4 marker corners from the
            detector, ordered as [top-left, top-right, bottom-right,
            bottom-left].

    Returns:
        float: The marker's heading angle in degrees. The result is
            in the range [0, 360), where:
            - 0° points right,
            - 90° points up,
            - 180° points left,
            - 270° points down (in image space).

    Description:
        Computes the midpoint of the front (top) and back (bottom)
        edges of the marker, then calculates a vector between them.
        The angle is derived from this vector using arctangent, with
        correction for image coordinate direction.
    """
    top_mid = (corners[0] + corners[1]) / 2
    bottom_mid = (corners[2] + corners[3]) / 2
    heading_vector = top_mid - bottom_mid
    # Calculates the Euclidean distance
    angle = np.degrees(np.arctan2(-heading_vector[1],
                heading_vector[0])) % 360
    return angle

def map_angle_to_servo(relative_angle, dist):
    if abs(relative_angle) > 90:
        return None
    dist = max(LOW_THRESHOLD, min(HIGH_THRESHOLD, dist))
    normalized_dist = (HIGH_THRESHOLD - dist) / (HIGH_THRESHOLD - LOW_THRESHOLD)
    normalized_angle = (90 - abs(relative_angle)) / 90
    weight = (normalized_angle * normalized_dist) ** 0.5
    servo_angle = 90 - weight * 42 if relative_angle > 0 else 90 + weight * 42
    return int(max(48, min(132, servo_angle)))

def send_if_allowed(angle):
    """
    Sends a servo angle to a vehicle if enough time has passed.

    Parameters:
        angle (int): The servo angle to send. Expected range is
                     between 48 (left) and 132 (right), with 90
                     meaning straight.

    Returns:
        None

    Description:
        Sends a TCP message with the servo angle to the RC vehicle
        identified by the global variable marker_id. The function
        enforces a minimum time between messages (SEND_INTERVAL).

        If the vehicle has not received a command recently, the
        angle is sent, and the timestamp and last angle are updated.

        If sending fails (e.g., disconnected socket), the vehicle is
        removed from all tracking dictionaries.
    """
    current_time = time.time()
    last_time = last_send_times.get(marker_id, 0)

    if current_time - last_time >= SEND_INTERVAL:
        try:
            user_sockets[marker_id].send((str(angle) + "\n").encode())
            print(f"[User {marker_id}] Sent angle: {angle}")
            last_sent_angles[marker_id] = angle
            last_send_times[marker_id] = current_time
        except Exception as e:
            print(f"Send error to user {marker_id}: {e}")
            user_sockets.pop(marker_id, None)
            last_sent_angles.pop(marker_id, None)
            last_send_times.pop(marker_id, None)

def compute_point_score(relative_angle, dist):
    if abs(relative_angle) > 90:
        return float('inf')
    dist = max(LOW_THRESHOLD, min(HIGH_THRESHOLD, dist))
    normalized_dist = (dist - LOW_THRESHOLD) / (HIGH_THRESHOLD - LOW_THRESHOLD)
    angle = abs(relative_angle)
    normalized_angle = (angle / 90) ** 2.5
    return 0.6 * normalized_dist + 0.4 * normalized_angle

def dynamic_threshold(relative_angle):
    angle = abs(relative_angle)

    if angle < 15:
        return HIGH_THRESHOLD      # Straight ahead — look far
    elif angle < 30:
        return HIGH_THRESHOLD * 0.75  # Slightly reduced
    elif angle < 60:
        return LOW_THRESHOLD + (HIGH_THRESHOLD - LOW_THRESHOLD) * 0.25
    else:
        return LOW_THRESHOLD       # Sides — look close only
    

# ==== Start of the Program ====
# Start the connection listener in the background
threading.Thread(target=handle_new_connections, daemon=True).start()

# Camera and ArUco setup
cap = cv2.VideoCapture(0)
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

# HSV range for detecting yellow objects
lower_yellow = np.array([18, 80, 60])
upper_yellow = np.array([40, 255, 255])


# ==== Main loop ====
while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break  # Exit if camera frame is not captured

    # Convert to grayscale for ArUco detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = aruco.detectMarkers(
        gray, aruco_dict, parameters=parameters)

    # Detect yellow areas using HSV color thresholding
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    contours, _ = cv2.findContours(
        yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (0, 0, 0), 2)

    # Process each detected ArUco marker
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
        for i, marker_id in enumerate(ids.flatten()):
            c = corners[i][0]  # Extract the 4 corners on the ArUco
            front_point = (c[0] + c[1]) / 2  # Front edge midpoint
            cx, cy = front_point.astype(int)
            center = front_point
            car_heading = estimate_heading(c)

            best_point = None
            best_angle = None
            best_score = float('inf')
            best_dist = None

            # Find closest object point in front of the marker
            for contour in contours:
                for point in contour:
                    direction_vector = point[0] - center
                    dist = np.linalg.norm(direction_vector)
                    angle = np.degrees(np.arctan2(-direction_vector[1],
                                direction_vector[0]))
                    relative_angle = (car_heading - angle + 360) % 360
                    if relative_angle > 180:
                        relative_angle -= 360  # Convert to [-180, 180]
                    
                    if dist < dynamic_threshold(relative_angle):
                        score = compute_point_score(relative_angle, dist)
                        if score < best_score:
                            best_point = point[0]
                            best_angle = relative_angle
                            best_dist = dist
                            best_score = score

            # If a valid point is found, draw it and compute turn
            if best_point is not None:
                # Draw the best point on the shown frame
                cv2.circle(frame, tuple(best_point), 5, (0, 0, 255), -1)
                cv2.line(frame, (cx, cy), tuple(best_point), (0, 0, 255), 2)

                if marker_id in user_sockets:
                    # Convert angle-to-point to a servo angle
                    servo_angle = map_angle_to_servo(best_angle, best_dist)
                    # Angle is None if closest is behind the marker 
                    if servo_angle is not None:
                        last_angle = last_sent_angles.get(marker_id, None)
                        if last_angle is None or abs(servo_angle - last_angle
                            ) >= ANGLE_THRESHOLD:
                            send_if_allowed(servo_angle)

            # If no object found, command vehicle to go straight
            elif last_sent_angles.get(marker_id, None) != 90:
                send_if_allowed(90)

    # Display the processed video frame
    cv2.imshow("Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break  # Exit on pressing 'q'


# Clean up on exit
cap.release()
cv2.destroyAllWindows()
server_socket.close()
for sock in user_sockets.values():
    sock.close()
