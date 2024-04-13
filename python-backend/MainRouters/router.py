from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import JSONResponse
import sys
import os
import base64
import uuid
import easyocr
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, DateTime
from sqlalchemy.sql import func
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('POSTGRES_DB')}"

# Подключение к базе данных
engine = create_engine(DATABASE_URL)
metadata = MetaData()
gagarin_history = Table('gagarin_history', metadata,
                        Column('id', Integer, primary_key=True, autoincrement=True),
                        Column('date', DateTime(timezone=True), default=func.now()),
                        Column('type', String),
                        Column('status', String))
metadata.create_all(engine)  # Создает таблицу, если она не существует

# Импорты моделей
sys.path.append("..")
from ultralytics import YOLO
import tensorflow
from cv.nn import core

router = APIRouter(tags=["Model"])
normalizer_model = YOLO('cv/models/normalizer.pt')
classifier_model = tensorflow.keras.models.load_model('cv/models/best_model.keras')
text_model = YOLO('cv/models/best.pt')
reader = easyocr.Reader(['ru'])

class ImageData(BaseModel):
    image: str

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
    if 'error' in result:
        insert_recognition_result(result, "не успешно")
        return JSONResponse(content=result, status_code=400)
    else:
        print(result)
        insert_recognition_result(result, "успешно")
        return JSONResponse(status_code=200, content=result)

def insert_recognition_result(recognition_result, status):
    doc_type = recognition_result.get('type', 'unknown') if status == "успешно" else None
    with engine.connect() as connection:
        ins_query = gagarin_history.insert().values(
            type=doc_type,
            status=status
        )
        connection.execute(ins_query)