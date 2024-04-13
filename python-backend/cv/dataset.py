import os
import cv2
import os
import numpy as np
from ultralytics import YOLO

directory_path = r'C:\Users\Sehap\Documents\code\gagrin\GagarinHack\python-backend\cv\training\text_finder\data'
normalizer_model = YOLO('python-backend/cv/models/normalizer.pt')

def normalize(results, image_pth):
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
    image = cv2.imread(image_pth)

    warped_image = cv2.warpPerspective(image, M, (max_width, max_height))

    cv2.imwrite(image_pth, warped_image)


for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    if os.path.isfile(file_path):
        # normalize every image
        try:
            results = normalizer_model.predict(fr'{file_path}', verbose=False, save=False)
            normalize(results, file_path)
            print(f'Normalized {file_path}')
        except: print('skipped')