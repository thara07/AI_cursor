import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Screen size
screen_w, screen_h = pyautogui.size()

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8
)
mp_draw = mp.solutions.drawing_utils

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Parameters
prev_x, prev_y = 0, 0
smoothening = 3.5
scale_factor = 1.2
center_x, center_y = screen_w // 2, screen_h // 2
click_delay = 0
click_cooldown = 10

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    h, w, _ = frame.shape

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        lm = hand.landmark
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        # Index fingertip
        ix, iy = int(lm[8].x * w), int(lm[8].y * h)

        # Convert to screen coordinates with scaling
        screen_x = int(center_x + (ix - w // 2) * (screen_w / w) * scale_factor)
        screen_y = int(center_y + (iy - h // 2) * (screen_h / h) * scale_factor)

        # Smooth movement
        curr_x = prev_x + (screen_x - prev_x) / smoothening
        curr_y = prev_y + (screen_y - prev_y) / smoothening
        pyautogui.moveTo(curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y

        # Draw index finger tip
        cv2.circle(frame, (ix, iy), 10, (0, 255, 255), -1)

        # Thumb tip
        tx, ty = int(lm[4].x * w), int(lm[4].y * h)
        thumb_index_dist = np.hypot(ix - tx, iy - ty)

        # Finger state detection
        finger_states = []
        for tip_id in [8, 12, 16, 20]:  # index, middle, ring, pinky
            if lm[tip_id].y < lm[tip_id - 2].y:
                finger_states.append(1)
            else:
                finger_states.append(0)

        # Scroll logic
        if sum(finger_states) == 0:  # All fingers down
            pyautogui.scroll(-50)  # scroll down
        elif sum(finger_states) == 4:  # All fingers up
            pyautogui.scroll(50)  # scroll up
        elif thumb_index_dist < 30 and click_delay == 0:
            pyautogui.click()
            click_delay = click_cooldown

    if click_delay > 0:
        click_delay -= 1

    cv2.imshow("Hand Gesture Mouse", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
