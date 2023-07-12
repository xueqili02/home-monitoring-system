import json

import cv2
from PIL import Image
from django.http import HttpResponse

from face.forms import UploadImageForm
from model.face_recognition.preProcess import preprocess_single


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

# def face_login(request):
