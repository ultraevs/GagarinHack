<<<<<<< HEAD
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

def classify(cv2_img, model, launch_type):
    if launch_type == 'linux':
        from cv.nn import core as nn_core
    elif launch_type == 'windows':
        from nn import core as nn_core

    logger = nn_core.get_logger(__name__)
    logger.info('[classifier] processing image')

    img_array = np.expand_dims(cv2.resize(cv2_img, (224, 224)), axis=0).astype('float32') / 255.

    predictions = model.predict(img_array)[0]
    
    predictions_sum = np.sum(predictions)
    normalized_predictions = predictions / predictions_sum
    
    class_indices = {'pass_1': 0, 'pass_2': 1, 'pts': 2, 'sts_1': 3, 'sts_2': 4, 'vu_1': 5, 'vu_2': 6}
    classes = list(class_indices.keys())
    
    predicted_class = classes[np.argmax(predictions)]
    
    logger.info('[classifier] got image type predictions')
    percentages = {classes[i]: round(float(normalized_predictions[i]) * 100, 2) for i in range(len(predictions))}

    return predicted_class, percentages
=======
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

def classify(cv2_img, model, launch_type):
    if launch_type == 'linux':
        from cv.nn import core as nn_core
    elif launch_type == 'windows':
        from nn import core as nn_core

    logger = nn_core.get_logger(__name__)
    logger.info('[classifier] processing image')

    img_array = np.expand_dims(cv2.resize(cv2_img, (224, 224)), axis=0).astype('float32') / 255.

    predictions = model.predict(img_array)[0]
    
    predictions_sum = np.sum(predictions)
    normalized_predictions = predictions / predictions_sum
    
    class_indices = {'pass_1': 0, 'pass_2': 1, 'pts': 2, 'sts_1': 3, 'sts_2': 4, 'vu_1': 5, 'vu_2': 6}
    classes = list(class_indices.keys())
    
    predicted_class = classes[np.argmax(predictions)]
    
    logger.info('[classifier] got image type predictions')
    percentages = {classes[i]: round(float(normalized_predictions[i]) * 100, 2) for i in range(len(predictions))}

    return predicted_class, percentages
>>>>>>> 1b5987952fe44aa135383109ce9d9957d62f660c
