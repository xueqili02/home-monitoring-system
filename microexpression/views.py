from django.http import StreamingHttpResponse
import cv2
import tensorflow as tf
from model.microexpression_recognition.demo import format_image
from model.microexpression_recognition.model import deepnn, image_to_tensor, EMOTIONS


def expression_recognition(requests):
    return StreamingHttpResponse(demo('model/microexpression_recognition/model', True),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def demo(modelPath, showBox=True):
    # 调用模型分析人脸微表情
    # tf.reset_default_graph()
    tf.compat.v1.disable_eager_execution()

    face_x = tf.compat.v1.placeholder(tf.float32, [None, 2304])
    y_conv = deepnn(face_x)
    probs = tf.nn.softmax(y_conv)

    # 加载模型
    tf.compat.v1.disable_eager_execution()
    saver = tf.compat.v1.train.Saver()
    ckpt = tf.train.get_checkpoint_state(modelPath)
    sess = tf.compat.v1.Session()
    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess, ckpt.model_checkpoint_path)

    # 获取笔记本的摄像头，
    video_captor = cv2.VideoCapture("rtmp://47.92.211.14:1935/live")

    emoji_face = []
    result = None
    while True:
        ret, frame = video_captor.read()
        detected_face, face_coor = format_image(frame)
        if showBox:
            if face_coor is not None:
                # 获取人脸的坐标,并用矩形框出
                [x, y, w, h] = face_coor
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                tensor = image_to_tensor(detected_face)
                result = sess.run(probs, feed_dict={face_x: tensor})

        if result is not None:
            for index, emotion in enumerate(EMOTIONS):
                # 将七种微表情的文字添加到图片中
                cv2.putText(frame, emotion, (10, index * 20 + 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)
                # 将微表情的概率用矩形表现出来
                cv2.rectangle(frame, (130, index * 20 + 10), (130 + int(result[0][index] * 100), (index + 1) * 20 + 4),
                              (255, 0, 0), -1)

        # cv2.imshow('face', frame)
        # Convert the frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame_data = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')
