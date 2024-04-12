from fastapi import FastAPI, UploadFile, File, APIRouter
from fastapi.responses import JSONResponse
import sys
import os
sys.path.append("..")
from ultralytics import YOLO
import tensorflow
import time
from cv.nn import core
router = APIRouter(tags=["AUTH"])
print(os.getcwd())
normalizer_model = YOLO('cv/models/normalizer.pt')
classifier_model = tensorflow.keras.models.load_model('cv/models/classifier.keras')
batch_model = YOLO(r'cv/models/text_batch.pt')


@router.post('/cv')
async def upload_file(file: UploadFile = File(...)):
    with open(fr'{os.getcwd()}/uploaded_images/{file.filename}', 'wb') as buffer:
        buffer.write(file.file.read())
    result = core.main(
        doc=fr'/uploaded_images/{file.filename}',
        normalizer_model=normalizer_model,
        classifier_model=classifier_model,
        batch_model=batch_model,
        export_showcase=True,
	launch_type="linux"
    )

    print(result)
    return JSONResponse(status_code=200, content=result)
