import numpy as np 
import cv2
import base64
import tensorflow as tf
from dl_utils import *

model = tf.keras.models.load_model("./0191_0.97_withGraph.h5")
def infer_and_estimation(img, cameraInfo):
    img = parse_image(img, shape=(224,224))[np.newaxis, :]
    result = model.predict(img)
    landmarks = result[0][0]
    renderOnOff = result[2][0]
    L_KP, R_KP = get_T_vector(parse_result(landmarks, cameraInfo), cameraInfo)
    return L_KP, R_KP, renderOnOff[0], renderOnOff[1]
