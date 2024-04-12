import os
from .normalizer import normalize
from .classifier import classify
from .reader import read
import cv2
import os
import logging
import time

logging.basicConfig(filename='cv/work.log', 
                    filemode='a', 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO)

def get_logger(name):
    return logging.getLogger(name)

def main(doc, normalizer_model, classifier_model, batch_model, debugging, export_showcase=False, launch_type='windows'):
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

    result = None
    # read data
    # result = read(warped, doc_class, batch_model, launch_type, debugging)
    end_time = time.time()
    elapsed_time = (end_time - start_time) * 1000
    if debugging: logging.info(f'[core] done in {elapsed_time} ms')
    logging.info('[core] finished')
    return {'result': 'success', 'data': {'doc_class': doc_class, 'percentages': percentages, 'fields_values': result}}
