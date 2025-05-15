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

    # Detect ArUco markers
    corners, ids, _ = aruco.detectMarkers(grayFrame, aruco_dict, parameters=parameters)

    # Optional: draw markers for visualization
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)

        # Create a copy of the grayscale image to mask out markers
        maskedGray = grayFrame.copy()

        # For each detected marker, fill its region with black before thresholding
        for marker_corners in corners:
            pts = np.int32(marker_corners[0])
            cv2.fillConvexPoly(maskedGray, pts, 0)  # Fill with black

    else:
        maskedGray = grayFrame.copy()

    # Threshold the image to isolate white areas (tape border)
    _, blackAndWhiteFrame = cv2.threshold(maskedGray, 230, 255, cv2.THRESH_BINARY)  # High threshold for white


    # Find contours of the white border
    contours, _ = cv2.findContours(blackAndWhiteFrame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours for visualization
    cv2.drawContours(frame, contours, -1, (255, 0, 0), 2)
    # cv2.drawContours(maskedGray, contours, -1, (255, 0, 0), 2)

    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
        for i, marker_id in enumerate(ids.flatten()):
            c = corners[i][0]
            cx = int(c[:, 0].mean())
            cy = int(c[:, 1].mean())
            center = np.array([cx, cy])

            # Draw marker center
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
            cv2.putText(frame, f"ID: {marker_id}", (cx + 10, cy),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Check distance to all border contours
            too_close = False
            for contour in contours:
                for point in contour:
                    distance = np.linalg.norm(center - point[0])
                    if distance < DIST_THRESHOLD:
                        too_close = True
                        break
                if too_close:
                    break

            if too_close:
                cv2.putText(frame, "TOO CLOSE!", (cx, cy - 20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 0, 255), 2)
                print(f"Marker {marker_id} too close to border!")

    # Display
    # cv2.imshow("ArUco + Border Detection", frame)
    # cv2.imshow("ArUco + Border Detection", grayFrame)
    cv2.imshow("ArUco + Border Detection", maskedGray)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
