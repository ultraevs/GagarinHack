from fastapi import FastAPI, UploadFile, File, APIRouter, HTTPException
from fastapi.responses import JSONResponse
import sys
import os
sys.path.append("..")
from ultralytics import YOLO
import tensorflow
from pydantic import BaseModel
import time
from cv.nn import core
import base64
import uuid
import easyocr


router = APIRouter(tags=["Model"])
print(os.getcwd())
normalizer_model = YOLO('cv/models/normalizer.pt')
classifier_model = tensorflow.keras.models.load_model('cv/models/best_model.keras')
text_model = YOLO('cv/models/best.pt')
reader = easyocr.Reader(['ru'])

# Mодель Pydantic для ожидаемых данных.
class ImageData(BaseModel):
    image: str  # Изображение в формате base64


@router.post("/detect")
async def detect_image(data: ImageData):
    try:
        image_bytes = base64.b64decode(data.image)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Ошибка декодирования base64") from e

    unique_filename = f"{uuid.uuid4()}.png"

    os.makedirs('uploaded_images', exist_ok=True)
    file_path = os.path.join('uploaded_images', unique_filename)

    with open(file_path, 'wb') as image_file:
        image_file.write(image_bytes)

    result = core.main(
        doc=file_path,
        normalizer_model=normalizer_model,
        classifier_model=classifier_model,
        text_model=text_model,
        debugging=False,
        reader=reader,
        launch_type="linux"
    )
    try:
        temp = result["error"]
        return JSONResponse(content=temp, status_code=400)
    except KeyError:
        print(result)
        return JSONResponse(status_code=200, content=result)
