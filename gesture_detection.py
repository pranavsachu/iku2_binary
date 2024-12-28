import mediapipe as mp
import cv2
import numpy as np
from training import load_training_data

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

def detect_fingertip_path(frame, path_points):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_fingertip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            h, w, _ = frame.shape
            x, y = int(index_fingertip.x * w), int(index_fingertip.y * h)

            path_points.append((x, y))
            for i in range(1, len(path_points)):
                cv2.line(frame, path_points[i - 1], path_points[i], (0, 255, 0), 2)

    return frame, path_points

def recognize_letter(path_points):
    training_data = load_training_data()
    best_match = None
    min_distance = float("inf")

    for letter, data_points in training_data.items():
        distance = compare_paths(path_points, data_points)
        if distance < min_distance:
            min_distance = distance
            best_match = letter

    if min_distance < 50:
        return best_match
    return None
def resample_path(path, num_points):
    """
    Resample the path to a fixed number of points for comparison.

    :param path: List of (x, y) points.
    :param num_points: Number of points to resample to.
    :return: Resampled path as a numpy array.
    """
    path = np.array(path)
    t = np.linspace(0, 1, len(path))
    t_resampled = np.linspace(0, 1, num_points)

    # Separate x and y coordinates
    x_resampled = np.interp(t_resampled, t, path[:, 0])
    y_resampled = np.interp(t_resampled, t, path[:, 1])

    # Combine x and y into a single array
    resampled_path = np.vstack((x_resampled, y_resampled)).T
    return resampled_path

def compare_paths(path1, path2):
    """
    Compares two paths after resampling them to have the same number of points.
    """
    num_points = min(len(path1), len(path2))
    path1_resampled = resample_path(path1, num_points)
    path2_resampled = resample_path(path2, num_points)
    return np.linalg.norm(path1_resampled - path2_resampled)
