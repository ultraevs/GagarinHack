from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from MainRouters.router import router
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time
app = FastAPI(root_path='/cv', docs_url="/cv/swagger", title="GagarinHack")
origins = ["*"]
app.include_router(router)
logging.basicConfig(filename='work.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, rate_limit=100, time_window=60):
        super().__init__(app)
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        requests = self.requests.get(client_ip, [])

        # Очистка старых запросов
        requests = [timestamp for timestamp in requests if current_time - timestamp < self.time_window]
        self.requests[client_ip] = requests

        if len(requests) >= self.rate_limit:
            return Response(content="Too Many Requests", status_code=429)

        self.requests[client_ip].append(current_time)
        response = await call_next(request)
        return response

# Добавление middleware в приложение
app.add_middleware(RateLimitMiddleware, rate_limit=5, time_window=60)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
