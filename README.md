# AutonomousCarGuide

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
## Overview
----------------------------------------------------------------------
This project implements a cyber-physical system (CPS) for smart 
mobility using an autonomous RC car. The system uses ArUco marker 
detection to identify and localize the vehicle, and edge detection via 
thresholding and contour analysis to prevent collisions with 
physical boundaries (yellow lane boundaries). It demonstrates 
real-time control, sensing, and feedback with a cost effective sensor
setup and a well constructed hardware platform with high quality
components.

The goal is to provide an accessible and reproducible platform without
relying on onboard cameras, AI, or machine learning, ideal for
learning basic autonomy.

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
- Power Supply: 7.4V Li-Po battery with step-down converters for 5V
                components
- Software: Python script that listens and executes incoming commands
            via GPIO/PWM using the Adafruit ServoKit and gpiozero
            libraries


Laptop (Server - Vision & Control Unit)

- Camera: USB connected webcamera (overhead view)
- Visual Processing:
  - ArUco marker detection for car localization (OpenCV)
  - Yellow lane boundary detection via HSV thresholding and contour
    detection
- Control Logic:
  - Manual control via keyboardnds
  - Automatic lane boundary detection and reactive steering


Communication Protocol

- Type: TCP socket (IPv4)
- Flow:
  1. Client (Raspberry Pi) connects to server
  2. Server processes camera feed, detects marker and boundaries
  3. Server sends commands (e.g., "left", "90") via TCP
  4. Client parses and executes the command using GPIO/PWM

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
    Raspberry Pi GPIO Control
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
cd Autonomous-car-guide/Server
pip install -r requirements.txt

On Raspberry Pi (RC Car / Client)
git clone
https://github.com/Cyber-physical-Systems-Lab/AutonomousCarGuide.git
cd AutonomousCarGuide/Client
pip install -r requirements.txt

----------------------------------------------------------------------
## Usage
----------------------------------------------------------------------
For automacy:
1. Start the Server on the Laptop
python aruco_edge_detector.py

2. Start the Client on the Raspberry Pi
python client.py

For manual steering:
1. Start the Server on the Laptop
python steering.py

2. Start the Client on the Raspberry Pi
python steering_client.py


----------------------------------------------------------------------
## Simulations / Demos
----------------------------------------------------------------------

- Basic ArUco marker tracking
- Edge detection using yellow border tape
- Automatic edge avoidance behavior

- Real-time manual control over Wi-Fi

Demo will be added

----------------------------------------------------------------------
## Configuration
----------------------------------------------------------------------

Parameters are currently defined as constants in the scripts:
Client: 
  - USER = 1 
  - SERVER_IP = "192.168.x.x"    # replace with your laptop IP
  - STEERING_CHANNEL = 0         # PWM channel on PCA9685 to use

Server:
  - ANGLE_THRESHOLD = 1          # Minimum angle difference required
                                      before sending a new command
  - LOW_THRESHOLD = 40           # Lower bound for  
  - HIGH_THRESHOLD = 80
  - SCALE = 0.2
  - SEND_INTERVAL = 0.2

  - lower_yellow = np.array([18, 80, 60])
  - upper_yellow = np.array([40, 255, 255])

  
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
