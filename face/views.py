import json
import cv2
import re

from PIL import Image
from django.core import serializers
from django.http import HttpResponse, StreamingHttpResponse, FileResponse
from face.forms import UploadImageForm, FaceLoginForm
from face.models import Intrusion
from model.face_recognition.fr_img import classify_face
from model.face_recognition.fr_video import fr
from model.face_recognition.preProcess import preprocess_single
from user.models import User


def upload_image(request, uid):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            title = form.cleaned_data['title']
            img = preprocess_single(Image.open(image))
            if img is not None:
                cv2.imwrite('resource/face_image/uid' + uid + '_' + title + '.jpg', img)
                return HttpResponse(json.dumps({'code': 200, 'message': 'success', 'data': None}))
    return HttpResponse(json.dumps({'code': 403, 'message': 'failure', 'data': None}))

def face_login(request):
    if request.method == "POST":
        form = FaceLoginForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            face_names = classify_face(Image.open(image), 'resource/face_image/')
            if face_names[0] != 'Unknown':
                pattern = r'uid(\d+)'
                match = re.search(pattern, face_names[0])
                try:
                    user = User.objects.get(id=int(match.group(1)))
                    return HttpResponse(json.dumps({'code': 200, 'message': 'success',
                                                    'data': {'username': user.username,
                                                             'email': user.email,
                                                             'id': user.id}}))
                except User.DoesNotExist:
                    return HttpResponse(json.dumps({'code': 200, 'message': 'user des not exist', 'data': user}))
    return HttpResponse(json.dumps({'code': 200, 'message': 'failure', 'data': None}))

def intrusion_recognition(request, uid):
    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        return HttpResponse(json.dumps({'code': 403, 'message': 'user does not exist', 'data': None}))

    def frame_generator():
        for frame, intrusion_time, video_filename, fps, width, height, video_queue in fr('rtmp://47.92.211.14:1935/live/1', uid):
            if intrusion_time is not None:
                Intrusion.objects.create(uid=user, intrusion_time=intrusion_time, video_path=video_filename)
                # 创建一个VideoWriter对象，用于保存视频
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 指定编码器为MP4
                out = cv2.VideoWriter('resource/intrusion_video/' + video_filename, fourcc, fps, (width, height))
                while not video_queue.empty():
                    item = video_queue.get()
                    out.write(item)
                out.release()
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')
    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')

def intrusion_record(request, uid):
    record_queryset = Intrusion.objects.filter(uid=uid)
    json_data = serializers.serialize('json', record_queryset)
    return HttpResponse(json_data, content_type='application/json')

def intrusion_video(request):
    video_path = 'resource/intrusion_video/' + request.GET.get('path')
    response = FileResponse(open(video_path, 'rb'), content_type='video/mp4')
    return response
