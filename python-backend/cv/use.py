from nn import core
from ultralytics import YOLO
import tensorflow


# models initialization
normalizer_model   = YOLO(r'C:\Users\Sehap\Documents\code\gagrin\GagarinHack\python-backend\cv\models\normalizer.pt')
classifier_model   = tensorflow.keras.models.load_model(r'C:\Users\Sehap\Documents\code\gagrin\GagarinHack\python-backend\cv\models\classifier.keras')
batch_model        = YOLO(r'C:\Users\Sehap\Documents\code\gagrin\GagarinHack\python-backend\cv\models\text_batch.pt')

photo_path = r"C:\Users\Sehap\Documents\code\gagrin\GagarinHack\python-backend\cv\testing\sts1.jpg"


# main function
result = core.main(
    doc=photo_path,
    normalizer_model=normalizer_model,
    classifier_model=classifier_model,
    batch_model=batch_model,
    export_showcase=False,
    launch_type='windows',
    debugging=False
)

print(result)