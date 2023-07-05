# from django.shortcuts import render
#
#
# def object_detection(request, video_name):
#     return render(request, "index.html", {"video_name": video_name})

from django.shortcuts import render

# Create your views here.

import cv2
import numpy as np
from django.http import StreamingHttpResponse

from model.object_detect.object_detection import object_detection


def object_recognition(request):
    return StreamingHttpResponse(object_detection(), content_type='multipart/x-mixed-replace; boundary=frame')