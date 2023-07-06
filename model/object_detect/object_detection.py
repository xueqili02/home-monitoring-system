import numpy as np
import cv2

def object_detection():
    # Set colors
    colors = []
    for i in range(91):
        random_c = np.random.randint(256, size=3)
        colors.append((int(random_c[0]), int(random_c[1]), int(random_c[2])))

    # Opencv DNN
    net = cv2.dnn.readNet("model/object_detect/yolov4-tiny.weights", "model/object_detect/yolov4-tiny.cfg")
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(320, 320), scale=1 / 255)

    # Load class lists
    classes = []
    with open("model/object_detect/classes.txt", "r") as file_object:
        for class_name in file_object.readlines():
            class_name = class_name.strip()
            classes.append(class_name)

    # Add the recognition you want to detect
    active_objects = ['person', 'cat', 'dog']

    # Local camera /  fps: 25
    cap = cv2.VideoCapture('rtmp://47.92.211.14:1935/live')

    while True:
        ret, frame = cap.read()

        # Object Detection
        (class_ids, scores, bboxes) = model.detect(frame, confThreshold=0.3, nmsThreshold=.4)
        for class_id, score, bbox in zip(class_ids, scores, bboxes):
            (x, y, w, h) = bbox
            class_name = classes[class_id]
            color = colors[class_id]
            if class_name in active_objects:
                cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 5)

        yield frame
        # # Convert the frame to JPEG format
        # ret, jpeg = cv2.imencode('.jpg', img_rd)
        # frame_data = jpeg.tobytes()
        #
        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')
