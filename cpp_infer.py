from pyfootdet import pyFootDetector
from oneEuroFilter import *

min_cutoff = 1
beta = 0

footdetector = pyFootDetector(model_path="./pyfootdet/model/foot_model_encrypted.pb")

def infer_and_estimation(img, cameraInfo, prevInfo):

    L_KP, R_KP, L_render, R_render = footdetector.run(img, (cameraInfo))

    if prevInfo[0] != "None":
        L_KP = filter(L_KP, prevInfo[0], min_cutoff=min_cutoff, beta=beta)

    if prevInfo[1] != "None":
        R_KP = filter(R_KP, prevInfo[1], min_cutoff=min_cutoff, beta=beta)

    return L_KP, R_KP, L_render, R_render