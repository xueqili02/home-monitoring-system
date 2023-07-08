import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
import tensorflow as tf

from django.http import StreamingHttpResponse
from model.emotional_recognition.EMR import to_device, MERCnnModel, get_default_device
from model.emotional_recognition.emo_reco import emotion_service
from model.microexpression_recognition.demo import microexpression_service
from model.microexpression_recognition.model import deepnn
from model.object_detect.object_detection import object_service


# Create your views here.

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

    '''
        object recognition config
    '''
    if obj == 1:
        # Set colors
        colors = []
        for i in range(91):
            random_c = np.random.randint(256, size=3)
            colors.append((int(random_c[0]), int(random_c[1]), int(random_c[2])))
        # Load class lists
        classes = []
        with open("model/object_detect/classes.txt", "r") as file_object:
            for class_name in file_object.readlines():
                class_name = class_name.strip()
                classes.append(class_name)
        # Add the recognition you want to detect
        active_objects = ['person', 'cat', 'dog']
        # Opencv DNN
        net = cv2.dnn.readNet("model/object_detect/yolov4-tiny.weights", "model/object_detect/yolov4-tiny.cfg")
        object_model = cv2.dnn_DetectionModel(net)
        object_model.setInputParams(size=(320, 320), scale=1 / 255)

    '''
        emotion recognition config
    '''
    if emotion == 1:
        device = get_default_device()
        # Loading pretrained weights
        w = 'model/emotional_recognition/model_U.pth'
        emotion_model = to_device(MERCnnModel(), device)
        if str(device) == 'cpu':
            emotion_model.load_state_dict(torch.load(w, map_location=torch.device('cpu')))  # use for cpu
        if str(device) == 'gpu':
            emotion_model.load_state_dict(torch.load(w, map_location=torch.device('cuda')))  # for GPU
        transform = transforms.ToTensor()

    '''
        microexpression recognition config
    '''
    if microexpression == 1:
        tf.compat.v1.disable_eager_execution()

        face_x = tf.compat.v1.placeholder(tf.float32, [None, 2304])
        y_conv = deepnn(face_x)
        probs = tf.nn.softmax(y_conv)

        # 加载模型
        tf.compat.v1.disable_eager_execution()
        saver = tf.compat.v1.train.Saver()
        ckpt = tf.train.get_checkpoint_state('model/microexpression_recognition/model')
        sess = tf.compat.v1.Session()
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)

    cnt = 0
    while True:
        ret, frame = cap.read()
        cnt = cnt + 1
        if cnt % 2 == 0 or ret is False:
            continue

        if obj == 1:
            class_ids, scores, bboxes = object_service(frame, object_model)
            for class_id, score, bbox in zip(class_ids, scores, bboxes):
                (x, y, w, h) = bbox
                class_name = classes[class_id]
                color = colors[class_id]
                if class_name in active_objects:
                    cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 5)

        if emotion == 1:
            if ret:
                prediction, x, y, w, h = emotion_service(frame, emotion_model, device, transform)
                if prediction is not None and x is not None and y is not None:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, prediction, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))

        if microexpression == 1:
            result, EMOTIONS = microexpression_service(frame, sess, probs, face_x)
            if result is not None:
                for index, m_emotion in enumerate(EMOTIONS):
                    # 将七种微表情的文字添加到图片中
                    cv2.putText(frame, m_emotion, (10, index * 20 + 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
                    # 将微表情的概率用矩形表现出来
                    cv2.rectangle(frame, (130, index * 20 + 10),
                                  (130 + int(result[0][index] * 100), (index + 1) * 20 + 4),
                                  (255, 0, 0), -1)

        if face == 1:
            print('call face')

        yield frame
