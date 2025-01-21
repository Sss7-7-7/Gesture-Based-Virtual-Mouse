# pip install opencv-python mediapipe pynput

import cv2
import mediapipe as mp
import numpy as np
from pynput.mouse import Controller, Button
import pyautogui

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize mouse controller
mouse = Controller()

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Define a 2 cm margin inside the camera frame
border_cm = 2
dpi = 96  # Standard DPI; adjust if needed
border_px = int((border_cm / 2.54) * dpi)  # Convert cm to pixels

# Click state
click_held = False

# Capture video
cap = cv2.VideoCapture(0)

def is_fingers_touching(landmarks, thumb_tip, index_tip):
    """Check if the thumb tip and index finger tip are close enough to be considered a touch."""
    thumb = landmarks[thumb_tip]
    index = landmarks[index_tip]
    distance = np.linalg.norm([thumb.x - index.x, thumb.y - index.y])
    return distance < 0.05  # Adjust threshold based on sensitivity

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the frame for natural interaction
        frame = cv2.flip(frame, 1)
        h, w, c = frame.shape

        # Define the effective camera area (excluding borders)
        x_min, x_max = border_px, w - border_px
        y_min, y_max = border_px, h - border_px

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and detect hands
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                # Extract index finger and thumb landmarks
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # Map hand coordinates (excluding borders) to full screen
                cursor_x = np.interp(index_tip.x, [x_min / w, x_max / w], [0, screen_width])
                cursor_y = np.interp(index_tip.y, [y_min / h, y_max / h], [0, screen_height])

                # Move the mouse cursor
                mouse.position = (int(cursor_x), int(cursor_y))

                # Detect and handle click gesture
                if is_fingers_touching(hand_landmarks.landmark, mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP):
                    if not click_held:
                        mouse.press(Button.left)  # Hold left-click
                        click_held = True
                else:
                    if click_held:
                        mouse.release(Button.left)  # Release left-click
                        click_held = False

                # Draw landmarks
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Draw the margins on the frame for visualization
        cv2.rectangle(frame, (border_px, border_px), (w - border_px, h - border_px), (0, 255, 0), 2)

        # Display the video frame
        cv2.imshow("Hand Tracking Mouse Control", frame)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()


# import cv2
# import mediapipe as mp
# import numpy as np
# from pynput.mouse import Controller, Button
# import pyautogui

# # Initialize Mediapipe Hands
# mp_hands = mp.solutions.hands
# hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
# mp_draw = mp.solutions.drawing_utils

# # Initialize mouse controller
# mouse = Controller()

# # Get screen dimensions
# screen_width, screen_height = pyautogui.size()

# # Define a 2 cm margin inside the camera frame
# border_cm = 2
# dpi = 96  # Standard DPI; adjust if needed
# border_px = int((border_cm / 2.54) * dpi)  # Convert cm to pixels

# # Click states
# left_click_held = False
# right_click_held = False

# # Capture video
# cap = cv2.VideoCapture(0)

# def is_fingers_touching(landmarks, finger1_tip, finger2_tip):
#     """Check if two fingers' tips are close enough to be considered a touch."""
#     finger1 = landmarks[finger1_tip]
#     finger2 = landmarks[finger2_tip]
#     distance = np.linalg.norm([finger1.x - finger2.x, finger1.y - finger2.y])
#     return distance < 0.05  # Adjust threshold based on sensitivity

# try:
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Flip the frame for natural interaction
#         frame = cv2.flip(frame, 1)
#         h, w, c = frame.shape

#         # Define the effective camera area (excluding borders)
#         x_min, x_max = border_px, w - border_px
#         y_min, y_max = border_px, h - border_px

#         # Convert the frame to RGB
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         # Process the frame and detect hands
#         result = hands.process(rgb_frame)

#         if result.multi_hand_landmarks:
#             for hand_landmarks in result.multi_hand_landmarks:
#                 # Extract finger landmarks
#                 thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
#                 index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
#                 little_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

#                 # Map hand coordinates (excluding borders) to full screen
#                 cursor_x = np.interp(index_tip.x, [x_min / w, x_max / w], [0, screen_width])
#                 cursor_y = np.interp(index_tip.y, [y_min / h, y_max / h], [0, screen_height])

#                 # Move the mouse cursor
#                 mouse.position = (int(cursor_x), int(cursor_y))

#                 # Detect and handle left-click gesture (thumb + index finger)
#                 if is_fingers_touching(hand_landmarks.landmark, mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP):
#                     if not left_click_held:
#                         mouse.press(Button.left)  # Hold left-click
#                         left_click_held = True
#                 else:
#                     if left_click_held:
#                         mouse.release(Button.left)  # Release left-click
#                         left_click_held = False

#                 # Detect and handle right-click gesture (thumb + little finger)
#                 if is_fingers_touching(hand_landmarks.landmark, mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.PINKY_TIP):
#                     if not right_click_held:
#                         mouse.press(Button.right)  # Hold right-click
#                         right_click_held = True
#                 else:
#                     if right_click_held:
#                         mouse.release(Button.right)  # Release right-click
#                         right_click_held = False

#                 # Draw landmarks
#                 mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

#         # Draw the margins on the frame for visualization
#         cv2.rectangle(frame, (border_px, border_px), (w - border_px, h - border_px), (0, 255, 0), 2)

#         # Display the video frame
#         cv2.imshow("Hand Tracking Mouse Control", frame)

#         # Break loop on 'q' key press
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

# finally:
#     cap.release()
#     cv2.destroyAllWindows()
