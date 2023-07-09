import json
import cv2

from django.http import StreamingHttpResponse, HttpResponse
from model.object_detect.object_detection import object_detection, set_coordinate


def object_recognition(request):
    def frame_generator():
        for frame in object_detection(0):
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')
    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')

def camera(request):
    url = request.GET.get("camera_url")

    def frame_generator():
        for frame in object_detection(url):
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')
    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')

# 视频范围选择框
def range_coordinate(request):
    coordinate = json.loads(request.body)
    ltx = coordinate.get('ltx')  # left top
    lty = coordinate.get('lty')
    rbx = coordinate.get('rbx')  # right bottom
    rby = coordinate.get('rby')
    set_coordinate(ltx, lty, rbx, rby)
    return HttpResponse("success")
