import shutil
from typing import List
from fastapi import APIRouter, File, UploadFile

routers = APIRouter()

@routers.post('/upload_file/')
def upload_file(file: bytes = File()):
    return {
        'file_size': len(file)
    }

@routers.post('/upload_file_class/')
def upload_file(file: UploadFile): #UploadFile proporcionada por FastAPI que facilita el manejo de archivos subidos, permitiendo acceder a atributos como el nombre del archivo (filename), el tamaño del archivo (size), y los encabezados del archivo (headers). 
    return {
        'file': file.file, # file object
        'file_name': file.filename, # name of the file
        'file_size': file.size, # size of the file
        'file_headers': file.headers # headers of the file,
    }

@routers.post('/upload_file_write/')
def upload_file(file: UploadFile):
    
    with open("assets/file.jpg", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {
        'file_name': file.filename, # name of the file
    }

@routers.post('/upload_file_write_array/')
def upload_file(images: List[UploadFile] = File()):
    
    for image in images:
        with open(f"assets/{image.filename}", "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    
    return {
        'file_names': [image.filename for image in images]
    }