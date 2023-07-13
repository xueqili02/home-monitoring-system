import datetime
import time
import cv2
import face_recognition
import numpy as np

from queue import Queue

from service.preload import known_face_encodings, known_face_labels

INTRUSION_INTERVAL = 30.0
MAX_QUEUE_SIZE = 30
MAX_VIDEO_QUEUE_SIZE = 500

def fr(url, uid):
    # Initialize the video capture
    cap = cv2.VideoCapture(url)
    # 获取视频的帧率和尺寸
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    cnt = 0
    queue = Queue()
    queue.maxsize = MAX_QUEUE_SIZE
    unknown_cnt = 0
    last_intrusion_time = time.time()
    intrusion_flag = False
    video_queue = Queue()
    while True:
        cnt = cnt + 1
        # Capture frame-by-frame
        ret = cap.grab()
        if ret is False:
            continue
        if cnt % 5 != 0:
            _, frame = cap.retrieve()
            video_queue.put(frame)
            continue
        _, frame = cap.retrieve()

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

            threshold = 0.4  # 调整阈值
            # use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if face_distances[best_match_index] < threshold:
                label = known_face_labels[best_match_index]
                if queue.full():
                    item = queue.get()
                    if item == 'Unknown':
                        unknown_cnt = unknown_cnt - 1
                queue.put('Known')
            else:
                if queue.full():
                    item = queue.get()
                    if item == 'Unknown':
                        unknown_cnt = unknown_cnt - 1
                queue.put('Unknown')
                unknown_cnt = unknown_cnt + 1
            recognized_face_labels.append(label)

        # print(unknown_cnt, queue.full())
        if unknown_cnt >= 5 and queue.full():
            # print(cnt)
            if time.time() - last_intrusion_time > INTRUSION_INTERVAL:  # intrusion detected
                last_intrusion_time = time.time()
                intrusion_flag = True
                # print('stranger! ', queue.qsize())

        # Draw rectangles and labels on the frame for recognized faces
        for (top, right, bottom, left), label in zip(face_locations, recognized_face_labels):
            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw the label below the face
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, label, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        if video_queue.qsize() == MAX_VIDEO_QUEUE_SIZE:
            video_queue.get()
            video_queue.get()
        video_queue.put(frame)
        video_queue.put(frame)

        if intrusion_flag:
            intrusion_flag = False
            intrusion_time = str(datetime.datetime.now().replace(microsecond=0)).replace(' ', 'T').replace(':', '-')
            video_filename = 'uid' + uid + '_' + intrusion_time + '.mp4'
            yield frame, intrusion_time, video_filename, fps, width, height, video_queue
        else:
            yield frame, None, None, None, None, None, None


def face_service(frame, known_face_encodings, known_face_labels):
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

    return frame
