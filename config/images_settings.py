import os
import base64
import uuid
from io import BytesIO
from PIL import Image, ImageFile
from slugify import slugify  # Si quieres usar nombres amigables para los archivos
from fastapi import HTTPException

# Configurar Pillow para manejar imágenes truncadas
ImageFile.LOAD_TRUNCATED_IMAGES = True

ALLOWED_EXTENSIONS = {"JPEG", "JPG", "PNG"}

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 1MB

def generate_unique_image_name(name: str) -> str:
    """Genera un nombre único para la imagen usando UUID."""
    unique_id = uuid.uuid4()
    image_name = f"{slugify(name)}-{unique_id}.jpeg"
    return image_name

def delete_image(image_path: str):
    """Elimina la imagen del servidor si existe."""
    if image_path and os.path.exists(image_path):
        os.remove(image_path)

def remove_base64_header(image_base64: str) -> str:
    if "," in image_base64:
        return image_base64.split(",")[1]  # Quitar el encabezado 'data:image/jpeg;base64,'
    return image_base64

def fix_base64_padding(b64_string: str) -> str:
    # Asegurarse de que el padding sea correcto
    missing_padding = len(b64_string) % 4
    if missing_padding:
        b64_string += '=' * (4 - missing_padding)
    return b64_string

def save_image_base64(image_base64: str, name: str, folder: str = "assets/", new_size: tuple = (1920, 1080)) -> str:

    # Remover encabezado de base64 si existe
    image_base64 = remove_base64_header(image_base64)
    
    # Corregir padding en la cadena base64
    image_base64 = fix_base64_padding(image_base64)
    
    # Decodificar imagen base64
    image_data = base64.b64decode(image_base64)
    
    # Verificar el tamaño de la imagen (decodificada)
    image_size = len(image_data)  # Tamaño en bytes
    if image_size > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="Tamaño de imagen no permitido. Máximo 1MB.")
    
    image = Image.open(BytesIO(image_data))
    
    # Verificar el formato de la imagen
    if image.format not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes JPEG, JPG y PNG.")

    # Redimensionar imagen
    image.thumbnail(new_size)

    # Crear carpeta si no existe
    os.makedirs(folder, exist_ok=True)

    # Guardar la imagen con un nombre amigable
    image_name = f"{slugify(name)}.webp"
    image_path = os.path.join(folder, image_name)

    # Guardar imagen en formato JPEG
    # image.save(image_path, format="JPEG", optimize=True)
    image.save(image_path, format="WEBP", quality=60, method=4)

    return image_path  # Devolvemos la ruta donde se guardó la imagen
