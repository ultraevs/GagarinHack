FROM python:3.11.5
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt update -y
RUN apt upgrade -y
#COPY tesseract/ ./python-backend/
RUN pip install fastapi uvicorn ultralytics tensorflow pydantic python-multipart easyocr starlette sqlalchemy psycopg2-binary python-dotenv
RUN apt-get install ffmpeg libsm6 libxext6 libleptonica-dev  -y
COPY . .
RUN mkdir uploaded_images
ENV LD_LIBRARY_PATH=/usr/src/app/tesseract/.libs:$LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/path/to/tesseract/libs:/path/to/leptonica/libs:$LD_LIBRARY_PATH
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
