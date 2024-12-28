import os
import json

TRAINING_DIR = "training_data"

def save_training_data(letter, path_points):
    if not os.path.exists(TRAINING_DIR):
        os.makedirs(TRAINING_DIR)

    data_path = os.path.join(TRAINING_DIR, f"{letter}.json")
    with open(data_path, "w") as file:
        json.dump(path_points, file)

def load_training_data():
    training_data = {}
    if os.path.exists(TRAINING_DIR):
        for file_name in os.listdir(TRAINING_DIR):
            if file_name.endswith(".json"):
                letter = file_name.split(".")[0]
                with open(os.path.join(TRAINING_DIR, file_name), "r") as file:
                    training_data[letter] = json.load(file)
    return training_data
