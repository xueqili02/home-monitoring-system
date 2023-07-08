import cv2

from django.http import StreamingHttpResponse
from model.emotional_recognition.emo_reco import emotion_service
from model.face_recognition.fr_video import face_service
from model.microexpression_recognition.demo import microexpression_service
from model.object_detect.object_detection import object_service
from .preload import object_model, classes, colors, active_objects, \
                        emotion_model, device, transform, \
                        sess, probs, face_x, \
                        known_face_encodings, known_face_labels


def call_service(requests, obj, emotion, microexpression, face):
    obj = int(obj)
    emotion = int(emotion)
    microexpression = int(microexpression)
    face = int(face)

    def frame_generator():
        for frame in call(obj, emotion, microexpression, face):
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')

    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')


def call(obj, emotion, microexpression, face):
    cap = cv2.VideoCapture('rtmp://47.92.211.14:1935/live')
    cnt = 0
    while True:
        ret, frame = cap.read()
        cnt = cnt + 1
        if cnt % 4 != 0 or ret is False:
            continue

        if obj == 1:
            frame = object_service(frame, object_model, classes, colors, active_objects)

        if emotion == 1:
            frame = emotion_service(frame, emotion_model, device, transform)

        if microexpression == 1:
            frame = microexpression_service(frame, sess, probs, face_x)

        if face == 1:
            frame = face_service(frame, known_face_encodings, known_face_labels)

        yield frame
