import cv2
import os

import numpy as np


def preprocess():
    # 创建人脸检测器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

    # 输入和输出目录
    input_dir = 'C://Users//HP//Desktop//PracticalTraining//family_monitor_server//model//face_recognition//face1'
    output_dir = 'C://Users//HP//Desktop//PracticalTraining//family_monitor_server//model//face_recognition//facelow'
    output_size = (160, 160)  # 目标像素大小

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 处理每张图像
    for root, dirs, files in os.walk(input_dir):
        for filename in files:
            # 读取图像
            image_path = os.path.join(root, filename)
            image = cv2.imread(image_path)

            # 灰度化图像
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # 检测人脸
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # 遍历检测到的人脸
            for (x, y, w, h) in faces:
                # 裁剪人脸区域
                face = image[y:y + h, x:x + w]

                # 调整人脸大小为目标像素大小
                resized_face = cv2.resize(face, output_size)

                # 确定输出路径
                relative_path = os.path.relpath(image_path, input_dir)
                output_path = os.path.join(output_dir, relative_path)

                # 确保输出目录存在
                output_dir_path = os.path.dirname(output_path)
                if not os.path.exists(output_dir_path):
                    os.makedirs(output_dir_path)

                # 保存提取的人脸图像
                cv2.imwrite(output_path, resized_face)


def preprocess_single(pil_image):
    # 创建人脸检测器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')

    output_size = (160, 160)  # 目标像素大小

    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # 灰度化图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 检测人脸
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 遍历检测到的人脸
    for (x, y, w, h) in faces:
        # 裁剪人脸区域
        face = image[y:y + h, x:x + w]

        # 调整人脸大小为目标像素大小
        resized_face = cv2.resize(face, output_size)

        return resized_face
    return None
