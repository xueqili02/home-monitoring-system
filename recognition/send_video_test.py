# send_video.py
import asyncio
import websockets
import numpy as np
import json
import cv2
import base64
import time


# 向服务器端实时发送视频截图
async def send_video(websocket):
    capture = cv2.VideoCapture('rtmp://47.92.211.14:1935/live')
    if not capture.isOpened():
        print('quit')
        quit()
    ret, frame = capture.read()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 95]

    # global ret, frame
    # global cam
    while True:
        # time.sleep(0.1)
        ret, frame = capture.read()
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = np.array(imgencode)
        img = data.tobytes()
        # base64编码传输
        img = base64.b64encode(img).decode()

        await websocket.send("data:image/jpg;base64," + img)


async def main_logic():
    async with websockets.connect('ws://127.0.0.1:8000/ws/video/wms/') as websocket:
        await send_video(websocket)

asyncio.get_event_loop().run_until_complete(main_logic())

# asyncio.new_event_loop().run_until_complete(main_logic())