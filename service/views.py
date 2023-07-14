import base64
import io
import json
import cv2

from PIL import Image
from django.http import StreamingHttpResponse, HttpResponse, FileResponse
from model.emotional_recognition.emo_reco import emotion_service
from model.face_recognition.fr_video import face_service
from model.fall_detect_track.fall_main import fall_detection
from model.image_caption.predict import describe_image
from model.microexpression_recognition.demo import microexpression_service
from model.object_detect.object_detection import object_service
from model.three2two.three2two import three_d_to_two_d
from .forms import PLYForm
from .preload import object_model, classes, colors, active_objects, \
                        emotion_model, device, transform, \
                        sess, probs, face_x, \
                        known_face_encodings, known_face_labels


def call_service(requests, obj, emotion, microexpression, face):
    obj = int(obj)
    emotion = int(emotion)
    microexpression = int(microexpression)
    face = int(face)

    def frame_generator():
        for frame in call(obj, emotion, microexpression, face):
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')

    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')


def call(obj, emotion, microexpression, face):
    cap = cv2.VideoCapture('rtmp://47.92.211.14:1935/live/1')
    cnt = 0
    while True:
        cnt = cnt + 1
        ret = cap.grab()
        if ret is False:
            continue
        if cnt % 4 != 0:
            continue
        _, frame = cap.retrieve()

        if obj == 1:
            frame = object_service(frame, object_model, classes, colors, active_objects)

        if emotion == 1:
            frame = emotion_service(frame, emotion_model, device, transform)

        if microexpression == 1:
            frame = microexpression_service(frame, sess, probs, face_x)

        if face == 1:
            frame = face_service(frame, known_face_encodings, known_face_labels)

        yield frame


def image_caption(request):
    image_base64 = json.loads(request.body).get('image')
    image_base64 = image_base64.split(';base64,')[-1]
    image = io.BytesIO(base64.b64decode(image_base64))
    caption = describe_image(Image.open(image))
    return HttpResponse(json.dumps({'code': 200, 'message': 'success', 'data': caption}))

def three_to_two(request):
    if request.method == "POST":
        form = PLYForm(request.POST, request.FILES)
        if form.is_valid():
            ply_file = form.cleaned_data['file']
            extension = str(ply_file.name).split('.')[1]
            if extension != 'ply':
                return HttpResponse(json.dumps({'code': 403, 'message': 'file extension is incorrect', 'data': None}))
            ply_save_path = 'resource/three2two/ply/' + ply_file.name
            image_save_path = 'resource/three2two/image/' + str(ply_file.name).split('.')[0] + '.png'
            with open(ply_save_path, 'wb') as f:
                for chunk in ply_file.chunks():
                    f.write(chunk)
            three_d_to_two_d(ply_save_path, image_save_path)
            return HttpResponse(json.dumps({'code': 200, 'message': 'success', 'data': image_save_path}))
    return HttpResponse(json.dumps({'code': 403, 'message': 'failure', 'data': None}))

def image_download(request):
    image_path = request.GET.get('image_path')
    response = FileResponse(open(image_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename={}'.format(image_path.split('/')[-1])
    return response

def fall_recognition(request):
    def frame_generator():
        for frame in fall_detection('rtmp://47.92.211.14:1935/live/1'):
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')

    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')
