from django.shortcuts import render


def object_detection(request, video_name):
    return render(request, "index.html", {"video_name": video_name})
