import socketio
import eventlet
import eventlet.wsgi
from flask import Flask
import numpy as np 
import base64
import cv2
from dl_infer import infer_and_estimation

import time

sio = socketio.Server()
app = Flask(__name__)

cnt = 0

@sio.on('connect')
def on_connect(sid, env):
    print('connected')
    # print(f"#######Connetion : {sid} ############")
    sio.emit('successConnect', {'msg':"Start Camera!"}, skip_sid=True)

@sio.on('sendImage')
def getEvent(sid, data):
    print(" I ve sent result")
    # tVec_L = []
    # tVec_R = []
    L_KP = {"m0": {"x":0.01,"y":0.01,"z":0.01, "w":0.01}, "m1" : {"x":0.01,"y":0.01,"z":0.01, "w":0.01}, "m2" : {"x":0.01,"y":0.01,"z":0.01, "w":0.01}}
    R_KP = {"m0": {"x":0.01,"y":0.01,"z":0.01, "w":0.01}, "m1" : {"x":0.01,"y":0.01,"z":0.01, "w":0.01}, "m2" : {"x":0.01,"y":0.01,"z":0.01, "w":0.01}}

    L_render = 0.
    R_render = 0.

    if data:
        imgbyte = base64.b64decode(data["image"])
        nparr = np.fromstring(imgbyte, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)#[:,:,::-1]
        # cv2.imwrite("./test.png", img)
        w   = data["width"]
        h   = data["height"]
        # tVec_L, tVec_R, L_render, R_render = infer_and_estimation(img, (h, w))
        L_KP, R_KP, L_render, R_render = infer_and_estimation(img, (h, w))
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
        # result = {
        #     "left" : {
        #         "position" : {k : v[0] for k, v  in zip(["x", "y", "z"], L_tvec)},
        #         "rotation" : {k : {k2:v2 for k2, v2 in zip(["x", "y", "z"], v)} for k, v  in zip(["m0", "m1", "m2"], L_rM)},
        #         "render" : bool(L_render > 0.22)
        #         },
        #     "right" : {
        #         "position" : {k : v[0] for k, v  in zip(["x", "y", "z"], R_tvec)}, 
        #         "rotation" : {k : {k2:v2 for k2, v2 in zip(["x", "y", "z"], v)} for k, v  in zip(["m0", "m1", "m2"], R_rM)},
        #         "render" : bool(R_render > 0.22)
        #         },
        #     }

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


    # result = {
    #         "Lvec" : tVec_L.tolist(), 
    #         "Rvec" : tVec_R.tolist(),
    #         "Lren" : int(L_render > 0.22),
    #         "Rren" : int(R_render > 0.22)
    #         }

    # print(result)

    sio.emit("recvTransform", result)
    print(" I ve sent result")

if __name__ == '__main__':
    app = socketio.Middleware(sio, app)
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)

