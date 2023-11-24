import ast
import datetime
import json
import cv2

from django.core import serializers
from django.http import StreamingHttpResponse, HttpResponse
from model.object_detect.object_detection import object_detection, set_coordinate, get_first_image, \
    set_active_objects, get_record
from recognition.models import Detection
from user.models import User

camera_ranges = {}

def object_recognition(request):
    def frame_generator():
        for frame, cnt in object_detection('rtmp://47.92.211.14:1935/live/5'):
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')
    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')

def camera(request, uid, cid):
    try:
        user = User.objects.get(id=uid)
        camera_url_dict = ast.literal_eval(user.camera_urls)
        url = ''
        if int(cid) == 1:
            url = camera_url_dict.get('url1')
        elif int(cid) == 2:
            url = camera_url_dict.get('url2')
        elif int(cid) == 3:
            url = camera_url_dict.get('url3')
        elif int(cid) == 4:
            url = camera_url_dict.get('url4')
        else:
            return HttpResponse(json.dumps({'code': 403, 'message': 'camera url does not exist', 'data': None}))
    except User.DoesNotExist:
        return HttpResponse(json.dumps({'code': 403, 'message': 'user does not exist', 'data': None}))

    def frame_generator():
        for frame, cnt in object_detection(url):
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()

            if cnt is not None:
                user_fk = User.objects.filter(id=uid)
                if user_fk.exists():
                    detection_record = get_record()
                    Detection.objects.create(uid=user_fk[0], time=detection_record.get('time'),
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
    path = 'resource/detection_image/' + str(camera_url).replace('/', '%2F').replace(':', '%3A') + time + '.jpg'
    image = cv2.imread(path)
    ret, jpg = cv2.imencode('.jpg', image)
    frame_data = jpg.tobytes()
    return HttpResponse(frame_data, content_type='image/jpeg')

def camera_url(request):
    body = json.loads(request.body)
    uid = body.get('uid')
    url1 = body.get('url1')
    url2 = body.get('url2')
    url3 = body.get('url3')
    url4 = body.get('url4')
    camera_url_dict = {'url1': url1, 'url2': url2, 'url3': url3, 'url4': url4}
    try:
        user = User.objects.get(id=uid)
        user.camera_urls = camera_url_dict
        user.save()
        return HttpResponse(json.dumps({'code': 200, 'message': 'success', 'data': None}))
    except User.DoesNotExist:
        return HttpResponse(json.dumps({'code': 403, 'message': 'user does not exist', 'data': None}))

def week_record(request, uid):
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse(json.dumps({'code': 403, 'message': 'user does not exist', 'data': None}))
    date = datetime.date.today()
    record_queryset = Detection.objects.filter(uid=user)
    result = [0, 0, 0, 0, 0, 0, 0]
    for record in record_queryset:
        record_date = datetime.datetime.strptime(record.time.split('T')[0], '%Y-%m-%d').date()
        time_diff = (date - record_date).days
        if time_diff <= 6:
            result[6 - time_diff] += 1
    return HttpResponse(json.dumps({'code': 200, 'message': 'success', 'data': json.dumps(result)}))

def camera_record(request, uid):
    try:
        user = User.objects.get(id=uid)
        camera_urls = ast.literal_eval(user.camera_urls)
        url1 = camera_urls.get('url1')
        url2 = camera_urls.get('url2')
        url3 = camera_urls.get('url3')
        url4 = camera_urls.get('url4')
    except User.DoesNotExist:
        return HttpResponse(json.dumps({'code': 403, 'message': 'user does not exist', 'data': None}))

    record_queryset = Detection.objects.filter(uid=user)
    result = [0, 0, 0, 0]
    for record in record_queryset:
        if record.camera_url == url1:
            result[0] += 1
        if record.camera_url == url2:
            result[1] += 1
        if record.camera_url == url3:
            result[2] += 1
        if record.camera_url == url4:
            result[3] += 1
    return HttpResponse(json.dumps({'code': 200, 'message': 'success', 'data': json.dumps(result)}))
