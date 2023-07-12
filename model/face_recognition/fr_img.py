import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
from time import sleep


def get_encoded_faces(face_image_path):
    """
    looks through the faces folder and encodes all
    the faces

    :return: dict of (name, image encoded)
    """
    encoded = {}

    for dirpath, dnames, fnames in os.walk(face_image_path):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file(face_image_path + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded


def unknown_image_encoded(img):
    """
    encode a face given the file name
    """
    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding


def classify_face(pil_image, face_image_path):

    faces = get_encoded_faces(face_image_path)
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR) # convert image from pillow format to cv2 format
    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:

        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        threshold = 0.5  # 调整阈值
        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if face_distances[best_match_index] < threshold:
            name = known_face_names[best_match_index]

        face_names.append(name)

    return face_names


# print(classify_face("Lkj.jpg"))
