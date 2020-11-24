import numpy as np 
import cv2
import base64

def resize(img, shape):
	return cv2.resize(img, shape)

def scale(img):
	return (img / 127.5)  - 1.

def make_square_with_padding(img):
    if len(img.shape) == 3:
        h, w, c = img.shape
    else:
        raise ("Please Input a Color Image")
    diff = h - w
    if diff > 0:
        pad = np.zeros(shape=(h, diff, c), dtype=np.uint8)
        img = np.concatenate((img, pad), axis=1)
    else :
        pad = np.zeros(shape=(np.abs(diff), w, c), dtype=np.uint8)
        img = np.concatenate((img, pad), axis=0)
    return img

def image_preprocessing(img, input_shape=None):
	img = make_square_with_padding(img)
	if input_shape:
		h, w = input_shape
		img = resize(img, (w, h))
	img = scale(img)
	return img
    
def parse_image(img, shape): 
    img = image_preprocessing(img, shape)
    return img

def parse_result(kpts, shape):
    h, w = shape
    if h < w:
        div = w
    else :
        div = h
    kpts = (kpts / 224) * div
    return kpts.reshape(26,2)

def parse_vertex(vertex):
    xyz = vertex.split(" ")[1:]
    # scale = 1
    # res = [np.float(xyz[0]) * scale, np.float(xyz[1]) * scale, np.float(xyz[2]) * scale]
    res = [np.float(xyz[0]), np.float(xyz[1]), np.float(xyz[2])]
    return res

def get_T_vector(keypoints, cameraInfo):
    # print("Model output keypoints : ", keypoints)
    using_idxes = np.array([1, 6, 7, 10, 11, 12, 13]) - 1
    h, w = cameraInfo

    LmeshPath = "./Foot_L.obj"
    with open(LmeshPath, 'r') as f:
        src_l = f.read()
    L_vertexes = np.array([x for x in src_l.split("\n") if x[:2] == "v "])

    RmeshPath = "./Foot_R.obj"
    with open(RmeshPath, 'r') as f:
        src_r = f.read()
    R_vertexes = np.array([x for x in src_r.split("\n") if x[:2] == "v "])
    
    vertex_number  = np.array([225, 228, 231, 234, 237, 256, 241, 253, 278, 260, 151, 141, 156])
    vertex_number_ = vertex_number[using_idxes]
    
    L_keypoint_vertex = np.array(list(map(parse_vertex, L_vertexes[vertex_number_])))
    R_keypoint_vertex = np.array(list(map(parse_vertex, R_vertexes[vertex_number_])))

    focal_length = w
    center = (w/2, h/2)

    camera_matrix = np.array([[focal_length, 0,            center[0]],
                              [0,            focal_length, center[1]],
                              [0,            0,            1]], 
                              dtype=np.float32)
    dist_coeffs = np.zeros((1,4))

    _, L_rvec, L_tvec = cv2.solvePnP(L_keypoint_vertex, keypoints[:13][using_idxes], camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
    _, R_rvec, R_tvec = cv2.solvePnP(R_keypoint_vertex, keypoints[13:][using_idxes], camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)

    # return L_rvec, L_tvec, R_rvec, R_tvec
    L_rotM, _ = cv2.Rodrigues(L_rvec)
    R_rotM, _ = cv2.Rodrigues(R_rvec)
    # return L_rotM, L_tvec, R_rotM, R_tvec

    L_P = np.hstack([L_rotM, L_tvec])
    R_P = np.hstack([R_rotM, R_tvec])

    # print("L_P : ", L_P)
    # print("R_P : ", R_P)

    #L_KP = camera_matrix @ L_P
    #R_KP = camera_matrix @ R_P
    
    return L_P, R_P
