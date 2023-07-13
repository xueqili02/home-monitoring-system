

known_face_encodings, known_face_labels = None, None

def face_preload():
    global known_face_encodings, known_face_labels
    # Load the known face encodings and their corresponding labels
    known_face_encodings = []
    known_face_labels = []

    # Folder containing the known face images
    known_faces_folder = "model/face_recognition/facelow"

    # Retrieve the file paths of the images within the folder
    image_paths = glob.glob(known_faces_folder + "/*.jpg")  # Update the file extension if necessary

    for image_path in image_paths:
        # Load the image and encode the face
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        # print(image_path)
        # Extract the label from the file name (assuming the file name is in the format "label.jpg")
        label = image_path.split("/")[-1].split(".")[0]

        # Append the encoding and label to the known faces list
        known_face_encodings.append(face_encoding)
        known_face_labels.append(label)
