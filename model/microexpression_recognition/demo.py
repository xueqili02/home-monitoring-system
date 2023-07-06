import cv2
import tensorflow as tf

from model.microexpression_recognition.model import image_to_tensor, deepnn

# opencv自带的人脸识别器
CASC_PATH = 'model/microexpression_recognition/haarcascade_frontalface_alt2.xml'
cascade_classifier = cv2.CascadeClassifier(CASC_PATH)
EMOTIONS = ['angry', 'disgusted', 'fearful', 'happy', 'sad', 'surprised', 'neutral']


def format_image(image):
    # image如果为彩色图：image.shape[0][1][2](水平、垂直像素、通道数)
    if len(image.shape) > 2 and image.shape[2] == 3:
        # 将图片变为灰度图
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 它可以检测出图片中所有的人脸，并将人脸用vector保存各个人脸的坐标、大小（用矩形表示）
        # 调整scaleFactor参数的大小，可以增加识别的灵敏度，推荐1.1
        faces = cascade_classifier.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)
    # 如果图片中没有检测到人脸，则返回None
    if not len(faces) > 0:
        return None, None
    # max_are_face包含了人脸的坐标，大小
    max_are_face = faces[0]
    # 在所有人脸中选一张最大的脸
    for face in faces:
        if face[2] * face[3] > max_are_face[2] * max_are_face[3]:
            max_are_face = face
    face_coor = max_are_face
    image = image[face_coor[1]:(face_coor[1] + face_coor[2]), face_coor[0]:(face_coor[0] + face_coor[3])]

    # 调整图片大小，变为48*48
    try:
        image = cv2.resize(image, (48, 48), interpolation=cv2.INTER_CUBIC)
    except Exception:
        print("problem during resize")
        return None, None

    return image, face_coor


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
    video_captor = cv2.VideoCapture(0)

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

        yield frame
        # cv2.imshow('face', frame)
        # if cv2.waitKey(10) & 0xFF == ord('q'):
        #     break

    # video_captor.release()
    # cv2.destroyAllWindows()
