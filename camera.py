import cv2
import time
import threading
from gesture_detection import detect_fingertip_path, recognize_letter
from training import save_training_data
from credits import add_credits
from utils.input_popup import prompt_for_letter
from typing_simulation import simulate_typing
import tkinter as tk
from tkinter import messagebox


def start_camera():
    """
    Starts the camera for gesture detection mode. Recognizes gestures, simulates typing for recognized gestures, 
    and stops after 20 seconds automatically if no valid gestures are recognized.
    """
    cap = cv2.VideoCapture(0)
    path_points = []
    start_time = time.time()
    print("Camera started for detection.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera frame not available. Exiting detection mode.")
            break

        frame, path_points = detect_fingertip_path(frame, path_points)

        if len(path_points) > 10:
            letter = recognize_letter(path_points)
            if letter:
                print(f"Recognized Gesture: {letter}")
                simulate_typing(letter)
                path_points = []  # Reset path after recognition
                break  # Exit detection after recognizing a gesture

        cv2.imshow("Fingertip Tracker", frame)

        # Stop after 20 seconds automatically
        elapsed_time = time.time() - start_time
        if elapsed_time >= 20:
            print("20 seconds elapsed. Stopping detection.")
            popup_not_recognized()
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Detection interrupted by user.")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Detection session ended.")


def popup_not_recognized():
    """
    Display a popup message if no gesture is recognized within the allowed time.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Gesture Recognition", "No gesture recognized!")
    root.destroy()


def start_training(user_id):
    """
    Starts training mode for a specific user. Records gestures for 10 seconds,
    allows the user to label them, and adds credits to their account.

    Args:
        user_id (int): The ID of the user currently logged in.
    """
    cap = cv2.VideoCapture(0)
    path_points = []
    start_time = time.time()

    print(f"Training started for user {user_id}. Gesture recording will stop automatically after 10 seconds.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Camera frame not available. Exiting training mode.")
            break

        frame, path_points = detect_fingertip_path(frame, path_points)

        cv2.imshow("Training Mode", frame)

        # Stop training after 10 seconds
        elapsed_time = time.time() - start_time
        if elapsed_time >= 10:
            print("10 seconds elapsed. Stopping recording.")
            letter = prompt_for_letter()
            if letter:
                save_training_data(letter, path_points)
                add_credits(user_id, 0.5)  # Add credits for the user
                print(f"Training data for '{letter}' saved! +0.5 credits added to user {user_id}")
            else:
                print("No letter provided. Data not saved.")
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Training interrupted by user.")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Training session ended.")
