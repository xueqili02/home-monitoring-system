import os
import shutil
import random
from math import floor

train_dir = 'dataset/train_faces'
test_dir = 'dataset/test_faces'
percentage = 0.15

# Get a list of all subdirectories in the train directory
train_folders = [folder for folder in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, folder))]

for folder in train_folders:
    train_folder_path = os.path.join(train_dir, folder)
    test_folder_path = os.path.join(test_dir, folder)

    # Create the test folder if it doesn't exist
    if not os.path.exists(test_folder_path):
        os.makedirs(test_folder_path)

    # Get a list of all files in the train folder
    files = os.listdir(train_folder_path)

    # Calculate the number of files to move to the test folder
    num_files_to_move = floor(len(files) * percentage)

    # Randomly select files to move
    files_to_move = random.sample(files, num_files_to_move)

    # Move the selected files to the test folder
    for file_name in files_to_move:
        src = os.path.join(train_folder_path, file_name)
        dst = os.path.join(test_folder_path, file_name)
        shutil.move(src, dst)