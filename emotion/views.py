import cv2
from django.http import StreamingHttpResponse
from model.emotional_recognition.emo_reco import emo_reco


# Create your views here.

def emotion_recognition(requests):
    def frame_generator():
        for frame in emo_reco():
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')
    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')