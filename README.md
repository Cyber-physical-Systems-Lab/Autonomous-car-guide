# AutonomousCarGuide

----------------------------------------------------------------------
## Overview
----------------------------------------------------------------------
This project implements a cyber-physical system (CPS) for smart 
mobility using an autonomous RC car. The system uses ArUco marker 
detection to identify and localize the car, and edge detectionvia 
thresholding and contour analysis to prevent collisions with 
physicalboundaries (e.g., white tape borders). It demonstrates 
real-time control, sensing, and feedback in a medium-cost hardware 
platform.

----------------------------------------------------------------------
## Table of Contents
----------------------------------------------------------------------
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Simulations / Demos](#simulations--demos)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Data Logging & Evaluation](#data-logging--evaluation)
- [Contributing](#contributing)
- [License](#license)

----------------------------------------------------------------------
## System Architecture
----------------------------------------------------------------------

This CPS architecture integrates physical mobility, embedded 
computation, and real-time visual perception.

RC Car (Client - Raspberry Pi)

- Computation: Raspberry Pi 5
- Actuators: Quicrun fusion mini 16 brushless motor
             Hitec D89MW servo
- Communication: TCP socket client connecting to the laptop/server
- Power Supply: 
- Software: Python script receiving and parsing commands
            and activates GPIO pins accordingly


Laptop (Server - Vision & Control Unit)

- Camera: Laptop-integrated webcam or USB webcam (overhead view)
- Visual Processing:
  - ArUco marker detection for car localization
  - Thresholding and contour detection for identifying road borders
- Control Logic:
  - Manual mode: Keyboard input (W/A/S/D) sends real-time commands
  - Optional: Automatic "TOO CLOSE" detection with steering decisions
- Communication: Runs TCP socket server and sends commands to client

Communication Protocol

- Type: TCP socket (IPv4)
- Flow:
  1. Raspberry Pi connects to the laptop server
  2. Laptop waits for key input or vision-based condition
  3. Sends command strings like "forward", "stop" via UTF-8
  4. Raspberry Pi decodes and controls motors

Data Flow

Webcam Input
    │
    ├──► ArUco Detection
    ├──► Edge (Contour) Detection
    └──► Marker-to-Edge Evaluation
          │
          ▼
    TCP Command: "left", "right", etc.
          │
          ▼
    Raspberry Pi GPIO Motor Control
          │            │
          ▼            ▼     
        PCA9685     ESC/Motor
          │
          ▼
    D89MW servo driver

----------------------------------------------------------------------
## Installation
----------------------------------------------------------------------

On Laptop (Controller / Server)
git clone 
https://github.com/Cyber-physical-Systems-Lab/AutonomousCarGuide.git
cd AutonomousCarGuide/Server
pip install -r requirements.txt

On Raspberry Pi (RC Car / Client)
git clone
https://github.com/Cyber-physical-Systems-Lab/AutonomousCarGuide.git
cd AutonomousCarGuide/Client
pip install -r requirements.txt

----------------------------------------------------------------------
## Usage
----------------------------------------------------------------------

1. Start the Server on the Laptop
python server_control.py

2. Start the Client on the Raspberry Pi
python client.py

3. Start ArUco Detection and Border Monitoring
python aruco_edge_detector.py

Keyboard Controls:
- W: Forward
- S: Backward
- A: Left
- D: Right
- Q: Quit
----------------------------------------------------------------------
## Simulations / Demos
----------------------------------------------------------------------

- Basic ArUco marker tracking
- Edge detection using white border tape
- Real-time manual control over Wi-Fi
- Automatic edge-avoidance behavior (coming soon)

Demo will be added

----------------------------------------------------------------------
## Configuration
----------------------------------------------------------------------

Parameters are currently defined as constants in the scripts:
- DIST_THRESHOLD = 100         # pixel distance from white border
- SERVER_IP = "192.168.x.x"    # replace with your laptop IP

Config support via YAML/JSON may be added in future updates.

----------------------------------------------------------------------
## Dependencies
----------------------------------------------------------------------

Requirements laptop:
- Python 3.8
- OpenCV 4.x
- NumPy
- keyboard (for manual control via server)

Requirements RC:
- Python 3.8

----------------------------------------------------------------------
## Data Logging & Evaluation
----------------------------------------------------------------------

Planned features:
- Navigational outputs from server depending on vehicle detection
- Making overtakes possible on multi-lane roads

----------------------------------------------------------------------
## Contributing
----------------------------------------------------------------------

To contribute:
1. Fork the repository
2. Create a branch: git checkout -b feature/my-feature
3. Make your changes and commit
4. Push and open a Pull Request

----------------------------------------------------------------------
## License
----------------------------------------------------------------------

For academic or institutional use, please cite accordingly.
