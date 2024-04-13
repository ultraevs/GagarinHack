from nn import core
from ultralytics import YOLO
import tensorflow
import os

# models initialization
normalizer_model   = YOLO(r'C:\Users\Sehap\Documents\code\gagrin\GagarinHack\python-backend\cv\models\normalizer.pt')
classifier_model   = tensorflow.keras.models.load_model(r'C:\Users\Sehap\Documents\code\gagrin\GagarinHack\python-backend\cv\models\best_model.keras')
batch_model        = YOLO(r'C:\Users\Sehap\Documents\code\gagrin\GagarinHack\python-backend\cv\models\text_batch.pt')

name = r"C:\Users\Sehap\Documents\code\gagrin\GagarinHack\python-backend\cv\training\text_finder\data\v_3535_914735-1.png"

print('initialized')

while True:
    name = os.path.join("C:/Users/Sehap/Documents/code/gagrin/GagarinHack/python-backend/cv/testing/new/", input('> '))
    # main function
    result = core.main(
        doc=name,
        normalizer_model=normalizer_model,
        classifier_model=classifier_model,
        batch_model=batch_model,
        export_showcase=False,
        launch_type='windows',
        debugging=False
    )

    print(result)