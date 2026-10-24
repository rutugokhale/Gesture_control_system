import cv2
import cvzone
import serial
import time
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# 1. Setup Serial
try:
    arduino = serial.Serial('COM5', 9600, timeout=1)
    time.sleep(2)
    print("Serial connected to COM5!")
except:
    print("Could not connect to COM5. Check your port!")

# 2. Setup Camera and Detector
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1, detectionCon=0.8)

target_pose = None

def get_hand_geometry(lmList):
    # Extracts the coordinates of the 5 fingertips 
    fingertips = [lmList[4], lmList[8], lmList[12], lmList[16], lmList[20]]
    return np.array(fingertips).flatten()

print("Show your hand, press 's' to save the target gesture, 'r' to reset, 'q' to quit.")

while True:
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1)
    hands, frame = detector.findHands(frame, draw=False)
    
    key = cv2.waitKey(1) & 0xFF
    
    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        
        # --- DRAWING VISUALS ---
        # 1. Draw Rectangular Frame
        x, y, w, h = hand["bbox"]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # 2. Draw Blue Joints (Size 3)
        for lm in lmList:
            cv2.circle(frame, (lm[0], lm[1]), 3, (255, 0, 0), cv2.FILLED)
        # -----------------------

        current_pose = get_hand_geometry(lmList)
        
        if key == ord('s'):
            target_pose = current_pose
            print("Gesture Saved!")
        elif key == ord('r'):
            target_pose = None
            if 'arduino' in locals() and arduino.is_open:
                arduino.write(b'R')
            print("Gesture Reset!")
            
        if target_pose is not None:
            dist = np.linalg.norm(current_pose - target_pose)
            current_state = 'G' if dist < 150 else 'R'
            
            if 'arduino' in locals() and arduino.is_open:
                arduino.write(current_state.encode())
    else:
        if 'arduino' in locals() and arduino.is_open:
            arduino.write(b'R')

    cv2.imshow("Machine Learning Pose Matcher", frame)
    
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

