from django.http import StreamingHttpResponse
from model.microexpression_recognition.demo import demo
import cv2

def expression_recognition(requests):
    def frame_generator():
        for frame in demo('model/microexpression_recognition/model', True):
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')
    return StreamingHttpResponse(frame_generator(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
