from fastapi import FastAPI, Query, Path, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from task import router
# from upload_file.router import router as upload_router

from pydantic import BaseModel

from config.jwt_manager import create_token, validate_token

app = FastAPI()

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['name'] != "admin":
            raise HTTPException(status_code=401, detail="Unauthorized")

class User(BaseModel):
    name: str
    password: str

#Para cambiar el nombre de la aplicacion
app.title = "Practica con FastAPI"
#Para cambiar la version de la aplicacion
app.version = "0.0.1"


app.include_router(router, prefix='/api/tasks')
# app.include_router(upload_router, prefix='/upload_file')


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
    


#@app.get("/")
#async def root():
#    return {"message": "Hello World"}
#
#
#@app.get("/hello/{name}")
#async def say_hello(name: str):
#    return {"message": f"Hello {name}"}
