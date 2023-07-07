import cv2
import torchvision.transforms as transforms
import torch
from model.emotional_recognition.EMR import get_default_device, to_device, MERCnnModel, faceBox, predict_image


def emo_reco():
    cam = cv2.VideoCapture('rtmp://47.92.211.14:1935/live')
    # cam = cv2.VideoCapture("http://192.168.43.164:4747/video")# connecting to ip cam
    # cam = cv2.VideoCapture('./Videos/all.mp4')# video
    # cam.set(cv2.CAP_PROP_FPS, 30)

    # GPU if available, else CPU
    device = get_default_device()
    print("Selected device:", device)

    # Loading pretrained weights
    w = 'model/emotional_recognition/model_U.pth'
    model = to_device(MERCnnModel(), device)
    if str(device) == 'cpu':
        model.load_state_dict(torch.load(w, map_location=torch.device('cpu')))  # use for cpu
    if str(device) == 'gpu':
        model.load_state_dict(torch.load(w, map_location=torch.device('cuda')))  # for GPU

    transform = transforms.ToTensor()

    while True:
        ret, frame = cam.read()
        if ret:
            bBox = faceBox(frame)
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
                    prediction = predict_image(faceExpResizedTensor, model, device)
                    cv2.putText(frame, prediction, (x, y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255))

        yield frame
        #     cv2.imshow('MER', frame)
        # if cv2.waitKey(1) & 0xff == ord('q'):  # to quit the camera press 'q'
        #     print('end')
        #     break
    # cam.release()
    # cv2.destroyAllWindows()


# emo_reco()
def emotion_service(frame, model, device, transform):
    bBox = faceBox(frame)
    if len(bBox) > 0:
        for box in bBox:
            x, y, w, h = box
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            faceExp = frame[y:y + h, x:x + w]
            try:  # sometime crashes due to corrupted/empty frame
                faceExpResized = cv2.resize(faceExp, (80, 80))
            except:
                return None, None, None, None, None
            faceExpResizedTensor = transform(faceExpResized)
            prediction = predict_image(faceExpResizedTensor, model, device)
            return prediction, x, y, w, h
    return None, None, None, None, None
