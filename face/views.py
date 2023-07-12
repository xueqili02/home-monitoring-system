import json

from PIL import Image
from django.http import HttpResponse

from face.forms import UploadImageForm


def upload_image(request, uid):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            title = form.cleaned_data['title']
            img = Image.open(image)
            img.save('resource/face_image/uid' + uid + '_' + title + '.jpg', 'JPEG')

    return HttpResponse(json.dumps({'code': 200, 'message': 'success', 'data': None}))

# def face_login(request):
