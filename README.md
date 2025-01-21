# Gesture-Based-Virtual-Mouse

This project is a **Hand Tracking Mouse Control System** using a webcam, which leverages **MediaPipe Hands**, **OpenCV**, and **pynput** libraries to control the mouse cursor and perform click gestures based on hand movements and gestures.

---

## Features
- Move the mouse pointer by moving your index finger.
- Perform a **left-click** by touching your thumb and index finger together.
- Margins within the camera feed are defined to avoid edge cases and ensure accurate tracking.
- Optional functionality to include **right-click** by touching the thumb and pinky finger.

---

## Prerequisites
- Python 3.8 or higher installed on your system.
- A functional webcam.

---

## Installation
Follow the steps below to install the required dependencies:

1. Clone the repository or copy the script file to your local system.
2. Install the required Python libraries:
   ```bash
   pip install opencv-python mediapipe pynput pyautogui
   ```

---

## Usage
1. Save the script to a file, for example, `hand_tracking_mouse_control.py`.
2. Run the script using:
   ```bash
   python hand_tracking_mouse_control.py
   ```
3. **Interaction Guide:**
   - **Move Cursor**: Move your hand within the camera's view. Use the index finger to guide the cursor.
   - **Left-Click**: Touch your **thumb** and **index finger** together to press and release the left mouse button.
   - (Optional) **Right-Click**: Uncomment the second script section to enable right-click functionality by touching your **thumb** and **pinky finger** together.

---

## Code Overview
The script performs the following tasks:
1. Captures live video from the webcam using **OpenCV**.
2. Detects hand landmarks using **MediaPipe Hands**.
3. Maps hand movements to screen coordinates using the dimensions of your screen (retrieved via **pyautogui**).
4. Simulates mouse clicks using **pynput** when gestures (e.g., thumb and index finger touch) are detected.
5. Displays the webcam feed with overlays of detected landmarks and margins.

---

## Key Parameters
- **`min_detection_confidence`** and **`min_tracking_confidence`**:
  Adjust these parameters in `mp.solutions.hands.Hands()` to improve detection reliability.

- **Border Margin**:
  - The default margin is set to **2 cm** inside the camera frame.
  - You can adjust it by modifying the `border_cm` variable.

- **Click Sensitivity**:
  - The default distance threshold for detecting a "touch" is `0.05`. You can modify this in the `is_fingers_touching` function.

---

## How to Stop
- Press the `q` key to exit the application.

---

## Known Limitations
- Requires a well-lit environment for accurate hand detection.
- Gestures may fail if hands are partially out of the camera frame.
- The click detection sensitivity may vary based on the size and position of hands.

---

## Example Output
When running the program, the webcam feed will show:
- Hand landmarks detected with colored connections.
- A green rectangle representing the effective area within which hand movements are mapped to the screen.

---

Enjoy controlling your mouse with hand gestures! 🚀
