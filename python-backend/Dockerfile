FROM python:3.11.5
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN apt update -y
RUN apt upgrade -y
COPY tesseract/ ./python-backend/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install fastapi uvicorn
RUN pip install ultralytics tensorflow
RUN pip install python-multipart
RUN apt-get install ffmpeg libsm6 libxext6 libleptonica-dev  -y
COPY . .
RUN pip install pytesseract
ENV LD_LIBRARY_PATH=/usr/src/app/tesseract/.libs:$LD_LIBRARY_PATH
ENV LD_LIBRARY_PATH=/path/to/tesseract/libs:/path/to/leptonica/libs:$LD_LIBRARY_PATH
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
