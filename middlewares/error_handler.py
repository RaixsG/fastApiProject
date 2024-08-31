import time
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse:
        try:
            return await call_next(request)
        except Exception as e:
            # return await super().dispatch(request, call_next)
            return JSONResponse(status_code=500, content={"message": f"Internal Server Error: {str(e)}"})







