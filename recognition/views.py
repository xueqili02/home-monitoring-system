import cv2

from django.http import StreamingHttpResponse
from model.object_detect.object_detection import object_detection


def object_recognition(request):
    def frame_generator():
        for frame in object_detection():
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')
    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')

