import json
import cv2
import re

from PIL import Image
from django.http import HttpResponse
from face.forms import UploadImageForm, FaceLoginForm
from model.face_recognition.fr_img import classify_face
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
