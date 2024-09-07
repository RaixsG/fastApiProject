import time
from fastapi import FastAPI, Query, Depends, Request
from fastapi.responses import JSONResponse
from apps.tasks.routers import router_tasks
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from config.jwt_manager import create_token
from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer

app = FastAPI()
#Para cambiar el nombre de la aplicacion
app.title = "Practica con FastAPI"
#Para cambiar la version de la aplicacion
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
origins = [
    "http://localhost.*.com",
    "https://localhost.*.com",
    "http://localhost",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Una lista de orígenes a los que se les debe permitir realizar solicitudes de origen cruzado. P. ej... Se puede utilizar para permitir cualquier origen.['https://example.org', 'https://www.example.org']['*']
    allow_credentials=True, #  Indicar que las cookies deben ser compatibles con las solicitudes de origen cruzado. El valor predeterminado es . Además, no se puede establecer en para que se permitan las credenciales, se deben especificar los orígenes.Falseallow_origins['*']
    allow_methods=["*"], # Una lista de métodos HTTP que deben permitirse para solicitudes de origen cruzado. El valor predeterminado es . Puede usar para permitir todos los métodos estándar.['GET']['*']
    allow_headers=["*"], # Una lista de encabezados de solicitud HTTP que deben ser compatibles con las solicitudes de origen cruzado. El valor predeterminado es . Puede usar para permitir todos los encabezados. Los encabezados , , y siempre están permitidos para []['*']
)
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response



app.include_router(router_tasks, prefix='/api/tasks')

class User(BaseModel):
    name: str
    password: str

@app.get("/test-query", dependencies=[Depends(JWTBearer())])
def page(page: int = Query(1, gt=1, lt=20), size: int = Query(5, ge=5, le=10)):
    return JSONResponse(content={
        "page": page,
        "size": size
    })
    
@app.get("/test-path/{page}")
def page(page: int): #ge significa que el valor debe ser mayor o igual a 1, le significa que el valor debe ser menor o igual a 20
    return JSONResponse(content={
        "page": page
        # "settings": settings.model_dump_json()
    }, status_code=404)


@app.post("/login/", tags=["Login"])
def login(user: User):
    if user.name == "admin" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(content={
            "message": "Login Success",
            "content": token
        }, status_code=200)
    return JSONResponse(content={
        "message": "Login Failed"
    }, status_code=401)
    
