import json
import cv2

from django.core import serializers
from urllib.parse import quote_plus
from django.http import StreamingHttpResponse, HttpResponse
from model.object_detect.object_detection import object_detection, set_coordinate, get_first_image, \
    set_active_objects, get_record
from recognition.models import Detection
from user.models import User

camera_ranges = {}

def object_recognition(request):
    def frame_generator():
        for frame, cnt in object_detection('rtmp://47.92.211.14:1935/live'):
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')
    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')

def camera(request, uid):
    url = request.GET.get("camera_url")

    def frame_generator():
        for frame, cnt in object_detection(url):
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()

            if cnt is not None:
                user = User.objects.filter(id=uid)
                if user.exists():
                    detection_record = get_record()
                    Detection.objects.create(uid=user[0], time=detection_record.get('time'),
                                             number=detection_record.get('number'),
                                             camera_url=detection_record.get('camera_url'),
                                             path=detection_record.get('path'))

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')
    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')

# 视频范围选择框
def range_coordinate(request):
    coordinate = json.loads(request.body)
    camera_url = coordinate.get('url')
    ltx = coordinate.get('ltx')  # left top
    lty = coordinate.get('lty')
    rbx = coordinate.get('rbx')  # right bottom
    rby = coordinate.get('rby')

    camera_ranges[camera_url] = (ltx, lty, rbx, rby)

    set_coordinate(camera_ranges)
    return HttpResponse(json.dumps({"code": 0, "message": "success", "data": []}))

def first_image(request):
    url = request.GET.get("camera_url")
    frame_data = get_first_image(url)

    return HttpResponse(b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n',
                        content_type='multipart/x-mixed-replace; boundary=frame')

def active_objects(request):
    body = json.loads(request.body)
    set_active_objects(body.get('data'))
    response = {
        "code": 200,
        "message": "success",
        "data": None
    }
    return HttpResponse(json.dumps(response))

def record(request, uid):
    record_queryset = Detection.objects.filter(uid=uid)
    json_data = serializers.serialize('json', record_queryset)
    return HttpResponse(json_data, content_type='application/json')

def object_image(request):
    camera_url = request.GET.get('camera_url')
    time = request.GET.get('time')
    path = 'resource/detection_image/' + quote_plus(camera_url) + time + '.jpg'
    image = cv2.imread(path)
    ret, jpg = cv2.imencode('.jpg', image)
    frame_data = jpg.tobytes()
    return HttpResponse(frame_data, content_type='image/jpeg')
