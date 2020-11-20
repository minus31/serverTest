# from pyfootdet import pyFootDetector
def prediction(img):
    footdetector = pyFootDetector("./model")
    # conf, kpts, vis = footdetector.detect(img)
    return footdetector.detect(img)

