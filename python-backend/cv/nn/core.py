import os
from .normalizer import normalize
from .classifier import classify
from .reader import read
import cv2
import os
import logging
import time
import re

logging.basicConfig(filename='cv/work.log', 
                    filemode='a', 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)

def get_logger(name):
    return logging.getLogger(name)

def main(doc, normalizer_model, classifier_model, text_model, debugging, reader, launch_type='windows'):
    start_time = time.time()

    logger = get_logger('core')
    logger.info('started')
    
    if launch_type == 'linux':
        os.environ['TESSDATA_PREFIX'] = 'tesseract/tessdata'
    
    processing = cv2.imread(os.path.join(os.getcwd(), doc))

    # document outline prediction
    results = normalizer_model.predict(processing, verbose=False, save=debugging, conf=0.65)


    # fix/transform image
    try:
        warped = normalize(processing, results, launch_type=launch_type)
    except TypeError:
        logger.info('[core] failed to normalize, using default image')
        warped = processing
    

    # classify document type
    doc_class, percentages = classify(warped, model=classifier_model, launch_type=launch_type)
    try:
        type_, page_number_ = doc_class.split('_')
    except: type_, page_number_ = doc_class, 0
    type_ = {'pass':'personal_passport', 'pts':'vehicle_passport', 'sts':'vehicle_certificate', 'vu':'driver_license'}[type_]
    confidence_ = percentages[doc_class] / 100

    # rotate image
    rotation = {'personal_passport': 'horizontal', 'vehicle_passport': 'vertical', 'vehicle_certificate': 'vertical', 'driver_license': 'horizontal'}
    required_orientation = rotation[type_]
    
    height, width = warped.shape[:2]
    current_orientation = "vertical" if height > width else "horizontal"
    if current_orientation != required_orientation:
        if current_orientation == "horizontal" and required_orientation == "vertical":
            rotated_image = cv2.rotate(warped, cv2.ROTATE_90_CLOCKWISE)
        elif current_orientation == "vertical" and required_orientation == "horizontal":
            rotated_image = cv2.rotate(warped, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        rotated_image = warped

    def process_string(s):
        letters = re.findall(r'[А-Яа-яA-Za-z]', s)
        
        if len(letters) == 1:
            return re.sub(r'[А-Яа-яA-Za-z]', '', s)
        return s
    
    res__ = []
    for res in res__:
        res__.append(process_string(res))

    # read data
    res_ = read(rotated_image, text_model, reader)
    
    try:
        series_, number_ = res_[0].replace(' ', '')[:4], res_[0].replace(' ', '')[4:]
    except IndexError: return {'_': 'failed to find serial or number on document'}
#    series_ = re.sub("[^0-9]", "", series_)
#    number_ = re.sub("[^0-9]", "", number_)

    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    if debugging: logging.info(f'[core] done in {elapsed_time} ms')
    logging.info('[core] finished')


    return {
        'type': type_,
        'confidence': float("{:.2f}".format(confidence_)),
        'series': series_,
        'number': number_,
        'page_number': page_number_
    }
