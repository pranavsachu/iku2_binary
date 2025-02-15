import os
import json

TRAINING_DIR = "training_data"

def save_training_data(letter, path_points):
    if not os.path.exists(TRAINING_DIR):
        os.makedirs(TRAINING_DIR)

    data_path = os.path.join(TRAINING_DIR, f"{letter}.json")
    
    # Check if the file already exists
    if os.path.exists(data_path):
        # Load existing data
        with open(data_path, "r") as file:
            existing_data = json.load(file)
        
        # Append new data to existing data
        if isinstance(existing_data, list):
            existing_data.append(path_points)
        else:
            existing_data = [existing_data, path_points]
    else:
        # If the file doesn't exist, start a new list with the current data
        existing_data = [path_points]

    # Save the updated data back to the file
    with open(data_path, "w") as file:
        json.dump(existing_data, file)

def load_training_data():
    training_data = {}
    if os.path.exists(TRAINING_DIR):
        for file_name in os.listdir(TRAINING_DIR):
            if file_name.endswith(".json"):
                letter = file_name.split(".")[0]
                with open(os.path.join(TRAINING_DIR, file_name), "r") as file:
                    training_data[letter] = json.load(file)
    return training_data
