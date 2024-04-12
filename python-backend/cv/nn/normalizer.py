import cv2
import os
import numpy as np

def normalize(image, results, launch_type):
    if launch_type == 'linux':
        from cv.nn import core as nn_core
    elif launch_type == 'windows':
        from nn import core as nn_core

    logger = nn_core.get_logger(__name__)
    logger.info('[normalizer] got corners coords')
    path_ = os.getcwd()
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    names = results[0].names
    confidences = results[0].boxes.conf.tolist()
    masks = results[0].masks

    for box, cls, conf, mask in zip(boxes, classes, confidences, masks):
        points = np.array(mask.xy[0].tolist(), dtype=np.int32)

    # ! find corners

    points = np.unique(np.array(points), axis=0)
    
    hull = cv2.convexHull(points)
    
    epsilon = 0.1 * cv2.arcLength(hull, True)
    approx = cv2.approxPolyDP(hull, epsilon, True)
    
    while len(approx) > 4:
        epsilon *= 1.1
        approx = cv2.approxPolyDP(hull, epsilon, True)
        
    while len(approx) < 4:
        epsilon *= 0.9
        approx = cv2.approxPolyDP(hull, epsilon, True)
    
    approx = approx.reshape(-1, 2).tolist()

    approx.sort(key=lambda x: x[1])
    top_corners = approx[:2]
    bottom_corners = approx[2:]

    lu, ru = sorted(top_corners, key=lambda x: x[0])

    ld, rd = sorted(bottom_corners, key=lambda x: x[0])
    

    logger.info('[normalizer] transforming image')
    # ! transform image
    lu = np.array(lu)
    ru = np.array(ru)
    ld = np.array(ld)
    rd = np.array(rd)

    width_a = np.linalg.norm(rd - ld)
    width_b = np.linalg.norm(ru - lu)
    max_width = max(int(width_a), int(width_b))

    height_a = np.linalg.norm(ld - lu)
    height_b = np.linalg.norm(rd - ru)
    max_height = max(int(height_a), int(height_b))

    pts_dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype='float32')

    pts_src = np.array([lu, ru, rd, ld], dtype='float32')

    M = cv2.getPerspectiveTransform(pts_src, pts_dst)
    warped_image = cv2.warpPerspective(image, M, (max_width, max_height))

    logger.info('[normalizer] warped image')
    return warped_image