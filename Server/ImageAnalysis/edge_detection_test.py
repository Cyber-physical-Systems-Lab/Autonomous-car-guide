import cv2
import cv2.aruco as aruco
import numpy as np

# Initialize webcam
cap = cv2.VideoCapture(0)

# ArUco dictionary and detector parameters
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

# Distance threshold (in pixels)
DIST_THRESHOLD = 100

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold the image to isolate white areas (tape border)
    _, blackAndWhiteFrame = cv2.threshold(grayFrame, 230, 255, cv2.THRESH_BINARY)

    # Find contours of the white border
    contours, _ = cv2.findContours(blackAndWhiteFrame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(frame, contours, -1, (255, 0, 0), 2)

    # Detect ArUco markers
    corners, ids, _ = aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
        for i, marker_id in enumerate(ids.flatten()):
            c = corners[i][0]
            cx = int(c[:, 0].mean())
            cy = int(c[:, 1].mean())
            center = np.array([cx, cy])

            # Draw marker center
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
            cv2.putText(frame, f"ID: {marker_id}", (cx + 10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Orientation vector: front = average of corners[0] and corners[1], back = average of corners[2] and corners[3]
            front = (c[0] + c[1]) / 2
            back = (c[2] + c[3]) / 2
            direction_vector = front - back

            # Find closest point on border
            min_dist = float('inf')
            closest_point = None
            for contour in contours:
                for point in contour:
                    point = point[0]
                    dist = np.linalg.norm(center - point)
                    if dist < min_dist:
                        min_dist = dist
                        closest_point = point

            if closest_point is not None and min_dist < DIST_THRESHOLD:
                border_vector = closest_point - center

                # 2D cross product to determine relative direction
                z = direction_vector[0] * border_vector[1] - direction_vector[1] * border_vector[0]

                if z > 0:
                    print(f"Marker {marker_id} is too close — TURN RIGHT")
                else:
                    print(f"Marker {marker_id} is too close — TURN LEFT")

                cv2.putText(frame, "TOO CLOSE!", (cx, cy - 20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 0, 255), 2)

    cv2.imshow("ArUco + Border Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
