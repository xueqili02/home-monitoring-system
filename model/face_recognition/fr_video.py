import cv2
import face_recognition
import glob
import numpy as np

# Load the known face encodings and their corresponding labels
known_face_encodings = []
known_face_labels = []

# Folder containing the known face images
known_faces_folder = "face1"

# Retrieve the file paths of the images within the folder
image_paths = glob.glob(known_faces_folder + "/*.jpg")  # Update the file extension if necessary

for image_path in image_paths:
    # Load the image and encode the face
    image = face_recognition.load_image_file(image_path)
    face_encoding = face_recognition.face_encodings(image)[0]
    print(image_path)
    # Extract the label from the file name (assuming the file name is in the format "label.jpg")
    label = image_path.split("/")[-1].split(".")[0]

    # Append the encoding and label to the known faces list
    known_face_encodings.append(face_encoding)
    known_face_labels.append(label)

# Initialize the video capture
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    rgb_frame = np.ascontiguousarray(frame[:, :, ::-1])
    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Initialize an empty list to store the labels of recognized faces
    recognized_face_labels = []

    for face_encoding in face_encodings:
        # Compare the face encoding with the known face encodings
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        label = "Unknown"
        # print(matches)
        # Check if there is a match in the known faces
        if True in matches:
            matched_indices = [i for i, match in enumerate(matches) if match]

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)


            # best_match_index = matched_indices[np.argmin(face_distances)]
            best_match_index = np.argmin(face_distances)
            label = known_face_labels[best_match_index]

        recognized_face_labels.append(label)

    # Draw rectangles and labels on the frame for recognized faces
    for (top, right, bottom, left), label in zip(face_locations, recognized_face_labels):
        # Draw a rectangle around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw the label below the face
        cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, label, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

    # Display the resulting frame
    cv2.imshow('Face Recognition', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
video_capture.release()
cv2.destroyAllWindows()
