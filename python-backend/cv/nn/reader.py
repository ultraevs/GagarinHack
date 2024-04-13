import cv2
import numpy as np

def read(image, text_model, reader):
    height, width, _ = image.shape
    results = text_model(image, verbose=False, save=False)
    boxes = results[0].boxes.xyxyn.tolist()
    res_ = []
    for box in boxes:
        line_ = ''
        x1, y1, x2, y2 = box
        x1*=width
        y1*=height
        x2*=width
        y2*=height

        cropped_image = image[int(y1):int(y2), int(x1):int(x2)]
        results = reader.readtext(cropped_image)
        
        for result in results:
            line_ += f'{result[1]} '
        res_.append(line_)
    return res_