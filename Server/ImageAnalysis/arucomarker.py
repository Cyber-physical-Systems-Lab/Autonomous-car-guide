# website for aruco marker create: https://chev.me/arucogen/


import cv2
import cv2.aruco as aruco

# opening main webcam
cap  = cv2.VideoCapture(0)
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detecting ArUco markers
    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # identifying detected markers and their IDs
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
        for i, marker_id in enumerate(ids.flatten()):
            c = corners[i][0]
            cx = int(c[:, 0].mean())
            cy = int(c[:, 1].mean())
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
            # print(f"Detected ID: {marker_id}, Position: ({cx}, {cy})")
   
    cv2.imshow("ArUco Marker Detection", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()