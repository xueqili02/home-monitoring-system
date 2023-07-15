import cv2
import face_recognition
import numpy as np
import torch
import torchvision.transforms as transforms
import tensorflow as tf
import glob

from transformers import BertTokenizer

from model.emotional_recognition.EMR import to_device, MERCnnModel, get_default_device
from model.fall_detect_track.ActionsEstLoader import TSSTG
from model.fall_detect_track.Detection.Utils import ResizePadding
from model.fall_detect_track.DetectorLoader import TinyYOLOv3_onecls
from model.fall_detect_track.PoseEstimateLoader import SPPE_FastPose
from model.fall_detect_track.Track.Tracker import Tracker
from model.image_caption.configuration import Config
from model.image_caption.models.caption import build_model
from model.isLive.gaze_tracking.gaze_tracking import GazeTracking
from model.microexpression_recognition.model import deepnn

object_model, classes, colors, active_objects = None, None, None, None
emotion_model, device, transform = None, None, None
sess, probs, face_x = None, None, None
known_face_encodings, known_face_labels = None, None
gaze = None
config, model_caption, tokenizer, start_token, end_token, caption, cap_mask = None, None, None, None, None, None, None
detect_model, pose_model, tracker, action_model, resize_fn = None, None, None, None, None

def object_preload():
    global object_model, classes, colors, active_objects
    # Set colors
    colors = []
    for i in range(91):
        random_c = np.random.randint(256, size=3)
        colors.append((int(random_c[0]), int(random_c[1]), int(random_c[2])))
    # Load class lists
    classes = []
    with open("model/object_detect/classes.txt", "r") as file_object:
        for class_name in file_object.readlines():
            class_name = class_name.strip()
            classes.append(class_name)
    # Add the recognition you want to detect
    active_objects = ['person', 'cat', 'dog']
    # Opencv DNN
    net = cv2.dnn.readNet("model/object_detect/yolov4-tiny.weights", "model/object_detect/yolov4-tiny.cfg")
    object_model = cv2.dnn_DetectionModel(net)
    object_model.setInputParams(size=(320, 320), scale=1 / 255)


def emotion_preload():
    global emotion_model, device, transform
    device = get_default_device()
    # Loading pretrained weights
    w = 'model/emotional_recognition/model_U.pth'
    emotion_model = to_device(MERCnnModel(), device)
    if str(device) == 'cpu':
        emotion_model.load_state_dict(torch.load(w, map_location=torch.device('cpu')))  # use for cpu
    if str(device) == 'gpu':
        emotion_model.load_state_dict(torch.load(w, map_location=torch.device('cuda')))  # for GPU
    transform = transforms.ToTensor()

def microexpression_preload():
    global sess, probs, face_x
    tf.compat.v1.disable_eager_execution()

    face_x = tf.compat.v1.placeholder(tf.float32, [None, 2304])
    y_conv = deepnn(face_x)
    probs = tf.nn.softmax(y_conv)

    # 加载模型
    tf.compat.v1.disable_eager_execution()
    saver = tf.compat.v1.train.Saver()
    ckpt = tf.train.get_checkpoint_state('model/microexpression_recognition/model')
    sess = tf.compat.v1.Session()
    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess, ckpt.model_checkpoint_path)

def face_preload():
    global known_face_encodings, known_face_labels
    # Load the known face encodings and their corresponding labels
    known_face_encodings = []
    known_face_labels = []

    # Folder containing the known face images
    known_faces_folder = "resource/face_image"

    # Retrieve the file paths of the images within the folder
    image_paths = glob.glob(known_faces_folder + "/*.jpg")  # Update the file extension if necessary

    for image_path in image_paths:
        # Load the image and encode the face
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        # print(image_path)
        # Extract the label from the file name (assuming the file name is in the format "label.jpg")
        label = image_path.replace('\\', '/').split("/")[-1].split(".")[0].split('_')[-1]

        # Append the encoding and label to the known faces list
        known_face_encodings.append(face_encoding)
        known_face_labels.append(label)

def gaze_preload():
    global gaze
    gaze = GazeTracking()

def image_caption_preload():
    global config, model_caption, tokenizer, start_token, end_token, caption, cap_mask
    config = Config()
    model_caption, _ = build_model(config)
    checkpoint = torch.load('model/image_caption/models/weight493084032.pth')
    # model = torch.hub.load('saahiluppal/catr', 'v3', pretrained=True)
    model_caption.load_state_dict(checkpoint['model'])

    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    start_token = tokenizer.convert_tokens_to_ids(tokenizer._cls_token)
    end_token = tokenizer.convert_tokens_to_ids(tokenizer._sep_token)

    def create_caption_and_mask(start_token, max_length):
        caption_template = torch.zeros((1, max_length), dtype=torch.long)
        mask_template = torch.ones((1, max_length), dtype=torch.bool)

        caption_template[:, 0] = start_token
        mask_template[:, 0] = False

        return caption_template, mask_template

    caption, cap_mask = create_caption_and_mask(
        start_token, config.max_position_embeddings)

def fall_preload():
    global detect_model, pose_model, tracker, action_model, resize_fn
    detection_input_size = 320
    pose_input_size = '224x160'
    pose_backbone = 'resnet50'
    device = 'cuda'
    # DETECTION MODEL.
    inp_dets = detection_input_size
    detect_model = TinyYOLOv3_onecls(inp_dets, device=device)

    # POSE MODEL.
    inp_pose = pose_input_size.split('x')
    inp_pose = (int(inp_pose[0]), int(inp_pose[1]))
    pose_model = SPPE_FastPose(pose_backbone, inp_pose[0], inp_pose[1], device=device)

    # Tracker.
    max_age = 30
    tracker = Tracker(max_age=max_age, n_init=3)

    # Actions Estimate.
    action_model = TSSTG()

    resize_fn = ResizePadding(inp_dets, inp_dets)
