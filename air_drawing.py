import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands and drawing utilities
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize the hand detector
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Create a blank canvas and a color palette
canvas = np.ones((480, 640, 3), dtype="uint8") * 255
color_palette = np.zeros((480, 100, 3), dtype="uint8")
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0), (0, 0, 0)]
for i, color in enumerate(colors):
    cv2.rectangle(color_palette, (0, i * 80), (100, (i + 1) * 80), color, -1)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Variables to store previous fingertip position and current color
prev_x, prev_y = None, None
current_color = (0, 0, 0)

def is_index_raised(landmarks):
    """Check if only the index finger is raised"""
    if landmarks[8].y < landmarks[6].y and landmarks[12].y > landmarks[10].y and landmarks[16].y > landmarks[14].y and landmarks[20].y > landmarks[18].y:
        return True
    return False

def is_thumb_open(landmarks):
    """Check if the thumb is open and all other fingers are closed"""
    if landmarks[4].x < landmarks[3].x and all(landmarks[i].y > landmarks[i-2].y for i in range(8, 21, 4)):
        return True
    return False

def is_fist(landmarks):
    """Check if the hand forms a fist"""
    if all(landmarks[i].y > landmarks[i-2].y for i in range(8, 21, 4)) and landmarks[4].x > landmarks[3].x:
        return True
    return False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to find hands
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Draw hand landmarks on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Get the coordinates of the index fingertip (landmark 8)
            height, width, _ = frame.shape
            landmarks = hand_landmarks.landmark
            index_finger_tip = landmarks[8]
            thumb_tip = landmarks[4]
            x = int(index_finger_tip.x * width)
            y = int(index_finger_tip.y * height)
            thumb_x = int(thumb_tip.x * width)
            thumb_y = int(thumb_tip.y * height)

            if is_fist(landmarks):
                canvas = np.ones((480, 640, 3), dtype="uint8") * 255
            elif is_index_raised(landmarks):
                if prev_x is not None and prev_y is not None:
                    cv2.line(canvas, (prev_x, prev_y), (x, y), current_color, thickness=3)
                prev_x, prev_y = x, y
            else:
                prev_x, prev_y = None, None

            if is_thumb_open(landmarks):
                if 0 <= thumb_x < 100:
                    color_index = thumb_y // 80
                    if 0 <= color_index < len(colors):
                        current_color = colors[color_index]

    # Combine the canvas and the frame
    combined_frame = cv2.addWeighted(frame, 0.5, canvas, 0.5, 0)

    # Add the color palette to the combined frame
    combined_frame[:, :100] = color_palette

    # Show the combined frame
    cv2.imshow('Air Drawing', combined_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close the window
cap.release()
cv2.destroyAllWindows()
