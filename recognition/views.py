import cv2

from django.http import StreamingHttpResponse
from model.object_detect.object_detection import object_detection


def object_recognition(request):
    def frame_generator():
        for frame in object_detection('rtmp://47.92.211.14:1935/live'):
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