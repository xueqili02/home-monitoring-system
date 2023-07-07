import cv2
import numpy as np
import torch
import torchvision.transforms as transforms

from django.http import StreamingHttpResponse
from model.emotional_recognition.EMR import to_device, MERCnnModel, get_default_device
from model.emotional_recognition.emo_reco import emotion_service
from model.object_detect.object_detection import object_service


# Create your views here.

def call_service(requests, obj, emotion, microexpression, face, caption):
    obj = int(obj)
    emotion = int(emotion)
    microexpression = int(microexpression)
    face = int(face)
    caption = int(caption)
    if obj == 1:
        print('obj')
    if emotion == 1:
        print('emotion')
    if microexpression == 1:
        print('microexpression')
    if face == 1:
        print('face')
    if caption == 1:
        print('caption')

    def call():
        cap = cv2.VideoCapture('rtmp://47.92.211.14:1935/live')

        '''
            object recognition config
        '''
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
        while True:
            ret, frame = cap.read()
            # import time
            # start_time = time.time()
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
                    prediction, x, y = emotion_service(frame, emotion_model, device, transform)
                    if prediction is not None and x is not None and y is not None:
                        cv2.putText(frame, prediction, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))

            # end_time = time.time()
            # execution_time = end_time - start_time
            # print(f"代码运行时间为：{execution_time} 秒")

            if microexpression == 1:
                print('call microexpression')

            if face == 1:
                print('call face')

            if caption == 1:
                print('call caption')

            yield frame

    def frame_generator():
        for frame in call():
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')
    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')
