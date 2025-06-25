 Hand Gesture Controlled Mouse

This Python project allows you to control your computer's mouse cursor using hand gestures detected via a webcam. It leverages computer vision libraries like OpenCV, MediaPipe, and automation via PyAutoGUI.

Features

- Move the mouse cursor using your index finger
- Perform left clicks by joining your thumb and index finger
- Scroll up by raising all fingers
- Scroll down by making a fist
- Smooth cursor movement with customizable parameters

Requirements

Make sure you have the following installed:
- Python 3.7 or higher
- OpenCV (`opencv-python`)
- MediaPipe (`mediapipe`)
- PyAutoGUI
- NumPy

You can install dependencies using:

bash
pip install opencv-python mediapipe pyautogui numpy
How to Run
Save the Python code in a file named hand_mouse.py.

Run the script:

bash
python hand_mouse.py
Your webcam will open, and you'll see a window titled “Hand Gesture Mouse.”

Use your index finger to move the cursor.

Pinch your thumb and index finger to click.

Make a fist to scroll down or raise all fingers to scroll up.

Press q to quit.

Notes
Works best in well-lit environments.

Adjust the smoothening, scale_factor, or click_cooldown values for your setup.

This project is a great foundation for building gesture-based interfaces.

License
This project is open-source and free to use for educational purposes.
