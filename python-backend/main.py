from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from MainRouters.router import router
import logging
app = FastAPI(root_path='/cv', docs_url="/cv/swagger", title="GagarinHack")
origins = ["*"]
app.include_router(router)
logging.basicConfig(filename='work.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
