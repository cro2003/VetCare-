from starlette.middleware.base import BaseHTTPMiddleware
import time
from fastapi import Request

class ResponseTime(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = int((time.perf_counter() - start_time) * 1000)
        response.headers["process-time"] = str(process_time)
        return response