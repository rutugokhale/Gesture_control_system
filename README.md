# AI-Powered Gesture Control System

Real-time hand gesture recognition using MediaPipe and OpenCV that controls LEDs on an Arduino. You "train" the system on a hand pose, and the LEDs show whether your current pose matches it.

## How it works
1. The webcam feed goes through MediaPipe Hands (via the cvzone library), which finds 21 landmarks on the hand.
2. The fingertip coordinates of all 5 fingers are turned into a feature vector.
3. Press **S** to save your current pose as the target gesture.
4. For every frame, the Euclidean distance between the live pose and the saved pose is calculated.
5. If the distance is below the threshold (τ = 150), Python sends `G` (match) to the Arduino. Otherwise it sends `R`.
6. The Arduino turns the green LED on for `G` and the red LED on for `R`.

## Tech stack
Python, MediaPipe (cvzone), OpenCV, NumPy, PySerial, Arduino Uno

## Controls
| Key | Action |
|-----|--------|
| S | Save current pose as target gesture |
| R | Reset saved gesture |
| Q | Quit |

## Hardware
- Arduino Uno
- 1 red LED and 1 green LED, each with a resistor
- Breadboard and jumper wires
- Laptop webcam

## How to run
1. Install the libraries: `pip install -r requirements.txt`
2. Upload `arduino_led.ino` to the Arduino using the Arduino IDE.
3. In `gesture_controller.py`, change `COM5` to your Arduino's port.
4. Run `python gesture_controller.py`
5. Show your hand, press **S** to save a pose, then try matching it.

## Files
- `gesture_controller.py`: main Python script
- `arduino_led.ino`: Arduino sketch that controls the LEDs
- `requirements.txt`: Python libraries needed
- `project_report-hand_gestures_ml.pdf`: full project report
- `hardware_assembly.pdf`: photos of the circuit setup

## Author
Rutu Gokhale, B.Tech ECE (AI/ML), MIT-WPU Pune
