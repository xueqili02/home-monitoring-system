import cv2
import torchvision.transforms as transforms
import torch

from django.http import StreamingHttpResponse
from model.emotional_recognition import EMR


# Create your views here.

def emotion_recognition(requests):
    return StreamingHttpResponse(emo_reco(), content_type='multipart/x-mixed-replace; boundary=frame')


def emo_reco():
    cam = cv2.VideoCapture("rtmp://47.92.211.14:1935/live")
    # cam = cv2.VideoCapture("http://192.168.43.164:4747/video")# connecting to ip cam
    # cam = cv2.VideoCapture('./Videos/all.mp4')# video
    cam.set(cv2.CAP_PROP_FPS, 30)

    # GPU if available, else CPU
    device = EMR.get_default_device()
    print("Selected device:", device)

    # Loading pretrained weights
    w = 'model/emotional_recognition/model_U.pth'
    model = EMR.to_device(EMR.MERCnnModel(), device)
    if str(device) == 'cpu':
        model.load_state_dict(torch.load(w, map_location=torch.device('cpu')))  # use for cpu
    if str(device) == 'gpu':
        model.load_state_dict(torch.load(w, map_location=torch.device('cuda')))  # for GPU

    transform = transforms.ToTensor()

    while True:
        _, frame = cam.read()
        if _:
            bBox = EMR.faceBox(frame)
            if len(bBox) > 0:
                for box in bBox:
                    x, y, w, h = box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    faceExp = frame[y:y + h, x:x + w]
                    try:  # sometime crashes due to corrupted/empty frame
                        faceExpResized = cv2.resize(faceExp, (80, 80))
                    except:
                        continue
                    faceExpResizedTensor = transform(faceExpResized)
                    prediction = EMR.predict_image(faceExpResizedTensor, model, device)
                    cv2.putText(frame, prediction, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))
            # cv2.imshow('MER', frame)

            # Convert the frame to JPEG format
            ret, jpeg = cv2.imencode('.jpg', frame)
            frame_data = jpeg.tobytes()

            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')
