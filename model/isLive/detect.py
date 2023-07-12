import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while (True):
    ret, frame = cap.read()
    if ret is False:
        break
    roi = frame[100: 500, 157: 800]  # 利用切片工具，选出感兴趣roi区域
    #  cv2.imshow("show",roi)

    rows, cols, _ = roi.shape  # 保存视频尺寸以备用
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)  # 转灰度
    gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)  # 高斯滤波一次

    _, threshold = cv2.threshold(gray_roi, 8, 255, cv2.THRESH_BINARY_INV)  # 二值化，依据需要改变阈值
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # 画连通域
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)

        # cv2.drawContours(roi, [cnt], -1, (0, 0, 255), 3)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.line(roi, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
        cv2.line(roi, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)
        break

    cv2.imshow("Roi", roi)
    cv2.imshow("Threshold", threshold)
    key = cv2.waitKey(30)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
