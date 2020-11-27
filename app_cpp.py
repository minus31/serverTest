import socketio
import eventlet
import eventlet.wsgi
from flask import Flask
import numpy as np 
import base64
import cv2
from cpp_infer import infer_and_estimation
import time
import math
from dl_utils import parse_image

sio = socketio.Server()
app = Flask(__name__)

@sio.on('connect')
def on_connect(sid, env):
    print('connected')
    sio.emit('successConnect', {"data" : "test_packet"})

@sio.on('sendCameraInfo')
def on_sendCameraInfo(sid, data):
    if data : 
        print('camera info ', data)
        camera = {
            'ax' : data["width"],
            'ay' : data["width"],
            'px' : data["width"]/2,
            'py' : data["height"]/2
            }
        sio.emit('recvCameraMat', camera)
    else:
        print("No camera info")

def parse_KP(data):
    result = np.ones((3, 4))
    for i, m in enumerate(["m0", "m1", "m2"]):
        for j, x in enumerate(["x", "y", "z", "w"]):
            result[i][j] = data[m][x]

    return result

@sio.on('sendImage')
def getEvent(sid, data):
    print(" I ve sent result")
    L_KP = {"m0": {"x":0.01,"y":0.01,"z":0.01, "w":0.01}, "m1" : {"x":0.01,"y":0.01,"z":0.01, "w":0.01}, "m2" : {"x":0.01,"y":0.01,"z":0.01, "w":0.01}}
    R_KP = {"m0": {"x":0.01,"y":0.01,"z":0.01, "w":0.01}, "m1" : {"x":0.01,"y":0.01,"z":0.01, "w":0.01}, "m2" : {"x":0.01,"y":0.01,"z":0.01, "w":0.01}}
    L_render = 0.
    R_render = 0.

    if data:
        imgbyte = base64.b64decode(data["image"])
        nparr = np.fromstring(imgbyte, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)[:,:,::-1]
        img_parsed = parse_image(img, shape=(224,224))
        # cv2.imwrite("./test.png", img)
        w   = data["width"]
        h   = data["height"]

        prevLeft  = "None"
        prevRight = "None"

        if data["left"]["render"] == True:
            prevLeft  = parse_KP(data["left"])

        if data["right"]["render"] == True:
            prevRight = parse_KP(data["right"])


        prev_info = [prevLeft, prevRight]

        L_KP, R_KP, L_render, R_render = infer_and_estimation(img_parsed, (h, w), prev_info)

        result = {
            "left" : {
                "kp" : {k : {k2:v2 for k2, v2 in zip(["x", "y", "z", "w"], v)} for k, v  in zip(["m0", "m1", "m2"], L_KP)},
                "render" : bool(L_render > 0.22)
                },
            "right" : {
                "kp" : {k : {k2:v2 for k2, v2 in zip(["x", "y", "z", "w"], v)} for k, v  in zip(["m0", "m1", "m2"], R_KP)},
                "render" : bool(R_render > 0.22)
                },
            }

    else: 
        result = {
                "left" : {
                    "kp" : L_KP,
                    "render" : False
                    },
                "right" : {
                    "kp" : R_KP,
                    "render" : False
                    },
            }

    sio.emit("recvTransform", result)
    print(" I ve sent result")

if __name__ == '__main__':
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

