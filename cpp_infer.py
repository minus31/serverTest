from pyfootdet import pyFootDetector
from oneEuroFilter import *

min_cutoff = 0.1
beta = 0.11

footdetector = pyFootDetector(model_path="./pyfootdet/model", isFrozen=False, isEncrypted=False)

def infer_and_estimation(img, cameraInfo, prevInfo=None):

    L_KP, R_KP, L_render, R_render = footdetector.run(img, (cameraInfo))

    if prevInfo:
        L_KP = filter(L_KP, prevInfo[0], min_cutoff=min_cutoff, beta=beta)
        R_KP = filter(R_KP, prevInfo[1], min_cutoff=min_cutoff, beta=beta)

    return L_KP, R_KP, L_render, R_render