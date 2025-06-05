# Step-by-Step Guide for Replication

-----------------------------------------------------------------------
## Overview
-----------------------------------------------------------------------
This guide is a step-by-step walkthrough designed to make it easy to 
replicate and understand the project. It provides detailed instructions
for setting up both the hardware and software components involved in 
building the autonomous RC car system.

This guide covers:
- Required hardware and wiring
- Environment setup (on both the Pi and the laptop)
- Running the main scripts
- Common issues and troubleshooting tips
- Tips on hardware that could be exchangable for an easier build

By the end of this guide, you should have a working system capable of:
- Detecting ArUco markers from an overhead camera
- Monitoring distance to a taped border
- Controlling an RC car in real-time via manual or automated logic

-----------------------------------------------------------------------
## Table of Contents
-----------------------------------------------------------------------
- [Required Components](#required-components)
- [Tips for an Upgraded Approach](#tips-for-an-upgraded-approach)
- [Chassis build](#chassis-build)
- [Connecting Inputs to PCA9685](#connecting-inputs-to-pca9685)
- [Connecting Outputs from PCA9685](#connecting-outputs-from-pca9685)
- [Motor Connections](#motor-connections)
- [Software Setup Pi](#software-setup-pi)
- [Software Setup for External Computer](#software-setup-for-external-computer)

-----------------------------------------------------------------------
## Required Components
-----------------------------------------------------------------------
To complete this project, you’ll need the following:

### Core Components
- **Raspberry Pi 5**
- **64GB Micro SD card**
- **XRAY M18 PRO chassis**
- **Hobbywing QuicRun Fusion Mini 16** (2-in-1 ESC + motor combo)
- **LiPo battery** for motor (2S or 3S, 7.4–11.1V, EC2 connector)
- **Power supply** 7.4V Li-Po battery with step-down converters
- **PCA9685 16-channel PWM driver board**
- **Printed ArUco marker** (attached to the RC car)
- **USB webcamera**
- **HW-BQ2001** stabilized DC converter for the pi
- **XL4015E1** step down DC converter for the PCA
- **Pinion gear** (pinion gear with 2.3mm wide hole)

### Wiring & Connectors
- 4× **female-to-female jumper wires** (Pi to PCA9685 I2C)
- 2× **male-to-female jumper wires** (motor signal + ground to Pi)
- 2× **male-to-male jumper wires** (Power for PCA9685)
- **XT60H Parallel Battery Connector**
- **Stripped USB-C adapter**

### Peripherals for Pi Setup
- **Monitor** (with HDMI input)
- **HDMI to mini-HDMI cable** (for monitor connection)
- **USB keyboard and mouse** (or wireless combo)
- **Internet access** (Wi-Fi or Ethernet)

### Tools & Accessories
- **Multimeter** (to verify voltage and continuity)
- **Soldering iron** (for solid, permanent connections if needed)
- **Solder wire** 
- **Zip ties** or **double-sided tape** (to secure components)
- **SD card reader** (for flashing the Raspberry Pi OS)
- **Small screwdriver set**
- **Printer** (for printing ArUco markers at correct scale)
- **Battery charger**
- **Screwdriver**

-----------------------------------------------------------------------
## Tips for an Upgraded Approach
-----------------------------------------------------------------------
The servo does **not perfectly align** with the pre-drilled holes in 
the chassis base. Other servos could fit better to this chassis and 
therefore sit more secure. 

The motor is **too large** for the standard motor slot located on the
left side of the chassis. The motor's EC2 cable adapter doesn't match
the battery adapter used in this project. The gears included with the
chassis do not fit the motor’s pinion shaft.

Either swap out the motor for a one that fits the requirements on the
other components. Or swap out the battery to be able to skip the 
wire replacement and order another pinion gear.
-----------------------------------------------------------------------
## Chassis build
-----------------------------------------------------------------------
The **XRAY M18 PRO** is delivered as a disassembled chassis and must be
assembled before use. A simple step-by-step assembly guide is included 
in the box and should be followed for basic construction.

### Servo Mounting
To mount it securely:
- Use the **servo foot with one screw hole and a pin** on one side.
- Use the **perpendicular bracket** on the opposite side.

This combination allows a stable and functional mounting, even if not 
perfectly symmetrical.

### Motor Fitment
TODO

### Gear Compatibility
Use the gear specified under [Required Components](#required-components), 
as it is compatible with the motor.

-----------------------------------------------------------------------
## Input to PCA9685
-----------------------------------------------------------------------
Use 4 female-to-female jumper wires to connect the PCA9685 to the
Raspberry Pi 5.

### PCA9685 to Raspberry Pi 5 (I2C Wiring):

- **GND** → Ground (Pin 6 on Pi)  
- **SCL** → SCL (Pin 5 on Pi)  
- **SDA** → SDA (Pin 3 on Pi)  
- **VCC** → 3.3V (Pin 1 on Pi)

### 5V Power Distribution

The PCA9685 also needs a separate 5V power input connected through
its screw terminal block. Connect it as follows:

- **Red (V+)** → Left screw terminal (positive side)  
- **Black (GND)** → Right screw terminal (ground)

Reference image:

![PCA wiring](img/PCA_wiring.jpg)

-----------------------------------------------------------------------
## Output from PCA9685
-----------------------------------------------------------------------
Connect a 3-wire cable to the first PWM output channel on the PCA9685. 
Make sure to align the wires according to their color so that each 
signal is properly routed.

### Wire Color Matching:
- **Yellow → Yellow** (Signal)  
- **Red → Red** (Power)  
- **Black → Black** (Ground)

-----------------------------------------------------------------------
## Battery Management
-----------------------------------------------------------------------

To power the Raspberry Pi, motor and PCA9685 from a single Li-Po 
battery, modify a XT60H parallel connector and use two buck converters:  
**HW-BQ2001** (for the Pi) and **XL4015E1** (for the PCA9685).

#### Steps

1. **Cut and prepare the XT60H connector**  
- Cut off one end of the XT60H parallel wire to expose bare wires.  
- Strip a short length of insulation from both the red and black wires.

2. **Connect power to the XL4015E1 input**  
- Twist the red and black wires from the XT60 with the  
    matching wires from the HW-BQ2001 input side.  
- Solder the combined red wires to the `+` input terminal of XL4015E1.  
- Solder the black wires to the `–` input terminal.

3. **Connect the HW-BQ2001 output to the USB-C adapter**  
- Strip the **output wires** of the HW-BQ2001 buck converter.  
- Use a USB-C power cable with red and black wires already exposed.  
- Solder the **red HW-BQ2001 wire** to the **red USB-C wire** (+).  
- Solder the **black HW-BQ2001 wire** to the **black USB-C wire** (–).  
- Insulate the joints with heat shrink tubing or electrical tape.  
- Plug the USB-C end into the Raspberry Pi’s power port.

4. **Set up XL4015E1 output to the PCA9685**  
- Solder two male-to-male jumper wires to the XL4015E1 output.  
- Red jumper for 5V (V+), black jumper for GND.  
- Plug them into the screw terminals of the PCA9685.

5. **Adjust the XL4015E1 voltage**  
- Plug in the Li-Po battery using the XT60 plug.  
- Use a multimeter to measure the XL4015E1 output.  
- Turn the small screw on the blue potentiometer until it reads 5.00V.

6. **Final connections**  
- XL4015E1 output goes to PCA9685 V+ and GND.  
- HW-BQ2001 output (via USB-C) powers the Raspberry Pi.  
- The XT60 adapter goes to the motor
- Ensure all grounds are connected and shared between devices.

#### Summary

- XT60H cable splits the battery output to two buck converters.  
- XL4015E1 supplies 5V to the PCA9685 via screw terminals.  
- HW-BQ2001 powers the Pi through a custom USB-C cable.  
- All devices must share a common ground for stability.

-----------------------------------------------------------------------
## Motor connections
-----------------------------------------------------------------------
You will need 2 male-to-female jumper wires.

The **Hobbywing QuicRun Fusion Mini 16** requires a power source of
**7.4V (2S Li-Po)** to **11.1V (3S Li-Po)**. Connect your battery to
the motor via the **blue EC2 connector**.

Since the motor draws power directly from the external battery, it does
**not** require power from the red V+ (power) wire on the PCA9685. It
only needs:

- A PWM **signal**
- A shared **ground** with the rest of the system

Leave the **red wire unconnected** when wiring the signal output.

### Wiring Instructions:
- Connect the signal wire to **GPIO 26 (Pin 37)** on the Raspberry Pi  
- Connect the ground wire to **Ground (Pin 39)** on the Raspberry Pi

Reference image:
![Pi wiring](img/Pi_wiring.jpg)

-----------------------------------------------------------------------
## Software Setup Pi
-----------------------------------------------------------------------

1. Flash the SD card with Raspberry Pi OS using an external computer.
2. Insert the SD card and power the Raspberry Pi 5.
3. Connect a monitor, keyboard, and mouse to the Pi.
4. Boot the Pi and follow the initial setup wizard.
5. Connect to Wi-Fi or use an Ethernet cable.
6. Open a terminal and run the following:

git clone 
https://github.com/Cyber-physical-Systems-Lab/AutonomousCarGuide.git
cd Autonomous-car-guide/Client
sudo apt-get update
sudo apt-get install python3-pip python3-dev i2c-tools
pip3 install -r requirements_client.txt --break-system-packages

sudo raspi-config
Here we need to enable I2C by clicking:
- 3: Interface Options
- I5: I2C 
Would you like the ARM I2C interface to be enabled?
<Yes>

Go into the client.py file and change the server IP-address to
the address of the external computer that is being used as server.

-----------------------------------------------------------------------
## Software Setup for External Computer
-----------------------------------------------------------------------

git clone 
https://github.com/Cyber-physical-Systems-Lab/AutonomousCarGuide.git
cd Autonomous-car-guide/Server
sudo apt-get update
sudo apt-get install python3-pip
pip3 install -r requirements_server.txt

-----------------------------------------------------------------------
## Running the System
-----------------------------------------------------------------------

First, start the server script by writing:
python .\aruco_edge_detector.py

And start the client with.
python client.py

-----------------------------------------------------------------------
## Calibration
-----------------------------------------------------------------------
Calibrating the motor is an important step to ensure consistent and
reliable throttle control. Using the `calibration.py` script provided
in the repository, follow these steps:

1. **Make sure the ESC is off** using the switch.
2. **Power the motor** (ensure the power source is connected).
3. **Press and hold the button on the ESC**, then **turn it on** while
    continuing to hold the button.
4. When the motor begins to beep, **release the button**.
5. On the Raspberry Pi, **start the `calibration.py` script**.
6. When the program says: `Press enter to send neutral throttle`,  
    press **Enter**, then **press the button on the ESC**.
    The motor should beep once.
7. Repeat this process when prompted for **max** and **min** throttle:  
   - The motor will beep **twice** for max  
   - And **three times** for min
8. When the script finishes, **calibration is complete**.
9. You can now run your desired control program.

-----------------------------------------------------------------------
## Project Wrap-up
-----------------------------------------------------------------------

You're now ready to build and operate a functional, centralized  
autonomous vehicle platform.

For questions, suggestions, or contributions, feel free to submit a  
GitHub issue or open a pull request!

Happy building!