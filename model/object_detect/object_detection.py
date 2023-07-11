import datetime
from urllib.parse import quote_plus

import numpy as np
import cv2

g_camera_ranges = {}
g_first_image = {}
g_active_objects = ['person', 'cat', 'dog']
IMAGE_FREQ = 200
g_record_list = []

def object_detection(url):
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

    # Local camera /  fps: 25
    cap = cv2.VideoCapture(url)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    # store the first image
    while True:
        ret = cap.grab()
        if ret is True:
            ret, frame = cap.read()
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()
            g_first_image[url] = frame_data
            break

    cnt = 0
    object_num = 0
    while True:
        cnt = cnt + 1
        ret = cap.grab()
        if ret is False:
            continue
        _, frame = cap.retrieve()

        camera_range = g_camera_ranges.get(url)
        if camera_range is None:
            ltx, lty, rbx, rby = 0., 0., 1., 1.
        else:
            (ltx, lty, rbx, rby) = camera_range

        # set coordinate
        range_frame = frame[int(height * lty): int(height * rby), int(width * ltx): int(width * rbx)]
        if abs(ltx - 0) > 1e-6 or abs(lty - 0) > 1e-6 or \
                abs(rbx - 1) > 1e-6 or abs(rby - 1) > 1e-6:
            cv2.rectangle(frame, (int(width * ltx), int(height * lty)), (int(width * rbx), int(height * rby)),
                          (0, 255, 0), thickness=2, lineType=cv2.LINE_AA)

        # Object Detection
        (class_ids, scores, bboxes) = model.detect(range_frame, confThreshold=0.3, nmsThreshold=.4)
        for class_id, score, bbox in zip(class_ids, scores, bboxes):
            (x, y, w, h) = bbox

            # set the new coordinate
            x = int(width * ltx) + x
            y = int(height * lty) + y

            class_name = classes[class_id]
            color = colors[class_id]
            if class_name in g_active_objects:
                cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 5)
                if cnt % IMAGE_FREQ == 0:
                    object_num = object_num + 1

        if cnt % IMAGE_FREQ == 0:
            image_time = str(datetime.datetime.now().replace(microsecond=0)).replace(' ', 'T').replace(':', '-')
            image_path = 'resource/detection_image/' + quote_plus(url) + image_time + '.jpg'
            ret, jpeg = cv2.imencode('.jpg', frame)
            if ret:
                with open(image_path, 'wb') as f:
                    f.write(jpeg.tobytes())
                record = {'number': object_num, 'time': image_time, 'camera_url': url, 'path': image_path}
                g_record_list.append(record)
            object_num = 0
            yield frame, cnt
        else:
            yield frame, None


def object_service(frame, model, classes, colors, active_objects):
    (class_ids, scores, bboxes) = model.detect(frame, confThreshold=0.3, nmsThreshold=.4)
    for class_id, score, bbox in zip(class_ids, scores, bboxes):
        (x, y, w, h) = bbox
        class_name = classes[class_id]
        color = colors[class_id]
        if class_name in active_objects:
            cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 5)
    return frame


def set_coordinate(camera_ranges):
    global g_camera_ranges
    g_camera_ranges = camera_ranges

def get_first_image(url):
    return g_first_image.get(url)

def set_active_objects(active_objects):
    global g_active_objects
    g_active_objects = active_objects

def get_record():
    global g_record_list
    return g_record_list[-1]
