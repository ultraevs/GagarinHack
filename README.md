# GagarinHack
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)![Golang](https://img.shields.io/badge/go-%23007ACC.svg?style=for-the-badge&logo=go&logoColor=white)![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)![TensorFlow](https://img.shields.io/badge/tensorflow-%23007ACC.svg?style=for-the-badge&logo=tensorflow)<img src="https://raw.githubusercontent.com/ultralytics/assets/main/logo/Ultralytics_Logotype_Reverse.svg" width="150" height="auto" style="filter: invert(100%) sepia(100%) saturate(0%) hue-rotate(188deg) brightness(94%) contrast(88%);">



# [Ссылка на готовое решение](https://gagarin.shmyaks.ru/)

### Задача: разработать сервис, позволяющий в режиме работы по api с определенной вероятностью классифицировать фото-сканы автомобильных документов по их типам - определить вероятности соответствия конкретному типу.

## Используемый стек технологий:
- [GO-Backend](https://github.com/ultraevs/GagarinHack/tree/main/go-backend) - Реализован с использванием [GO](https://go.dev/) и фреймворка [Gin](https://github.com/gin-gonic/gin). Задачей модуля является реализация API для взаимодействия с frontend модулем.
- [Python-Backend](https://github.com/ultraevs/GagarinHack/tree/main/python-backend) - Реализован с использованием [Python](https://www.python.org/) и фреймворка [Fast-API](https://fastapi.tiangolo.com/ru/) - Задачей модуля является обеспечение взаимодействия бекенда сайта и cv модели.
- [Frontend](https://github.com/ultraevs/GagarinHack/tree/main/frontend) - Реализован с использованием [React](https://ru.legacy.reactjs.org/). Задачай является предоставление красивого и функционалоного интерфейса для пользователя.
- [Deployment](https://github.com/ultraevs/GagarinHack/tree/main/deployment) - Реализован с использованием [Docker-Compose](https://www.docker.com/). Задачей модуля является возможность быстрого и безошибочного развертывания приложения на любом сервере.
- [CV](https://github.com/ultraevs/GagarinHack/tree/main/python-backend/cv) - Реализован с использованием [YOLOv8](https://docs.ultralytics.com/ru/models/yolov8/). Задачей модуля является распознавание типа документа на предоставленных фото пользователя.

## Функционал решения

- Загрузка одного/нескольких документов.
- История распознаваний для каждого пользователя
  
## Запуск решения
```sh
    git clone https://github.com/tesseract-ocr/tesseract.git
    cd tesseract
    ./autogen.sh
    ./configure --prefix=/путь к GagarinHack/GagarinHack/python-backend/
    make
    sudo make install

    cd GagarinHack/deployment
    docker-compose build
    docker-compose up -d
```
