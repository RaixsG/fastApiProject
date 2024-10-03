import os
from fastapi import Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from .models import ModelTask, ModelCategory, ModelUser
from .schemas import (
    TaskSchema,
    TaskCreateSchema,
    CreateUserSchema,
    CreateCategorySchema
)

from config.pagination import paginate, PageParams
from config.images_settings import save_image_base64, generate_unique_image_name, delete_image

# TASKS
def getAllTasks(db: Session):
    try:
        response = db.query(ModelTask).all()
        if response is None: return {'message': 'Tasks not found' }
        return response
    except Exception as e:
        return {
            'message': f"Error in the request: {str(e)}"
        }

def getByIdTask(db: Session, id: int, request: Request):
    try:
        response = db.query(ModelTask).get(id)
        if not response:
            return {
                'message': 'Task not found'
            }
        task_schema = TaskSchema.from_orm(response, request)
        return task_schema
    except Exception as e:
        return {
            'message': f"Error in the request: {str(e)}"
        }

def createTask(data: TaskSchema, db: Session, request: Request):
    try:
        image_url = None
        
        if data.image_base64:
            # Generar un nombre único para la imagen
            image_name = generate_unique_image_name(data.name)
            # Guardar la imagen en el servidor local
            image_path = save_image_base64(data.image_base64, image_name, folder="assets/tasks")
            
            # Obtener la URL pública de la imagen
            base_url = request.base_url  # http://localhost:8000/
            image_url = f"{base_url}static/{image_path.replace('assets/', '').replace(os.sep, '/')}"
                
        instance = ModelTask(
            name=data.name,
            description=data.description,
            status=data.status,
            category=data.category,
            user=data.user,
            image=image_url
        )
        db.add(instance)
        db.commit()
        db.refresh(instance)
        
        return instance
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e.orig))

def updateTask(task_id: int, data: TaskCreateSchema, db: Session, request: Request):
    try:
        # Buscar la tarea existente en la base de datos
        instance = db.query(ModelTask).filter(ModelTask.id == task_id).first()

        if not instance:
            raise HTTPException(status_code=404, detail="Task not found")

        # Variable para manejar la nueva URL de la imagen
        image_url = instance.image  # Mantenemos la imagen actual si no se sube una nueva
        
        # Variable para renombrar la imagen
        image_name = instance.name
        
        if image_name.name != data.name:
            image_name = generate_unique_image_name(data.name)
            image_path = save_image_base64(data.image_base64, image_name)
            
            # Obtener la URL pública de la imagen
            base_url = request.base_url  # http://localhost:8000/
            image_url = f"{base_url}static/{image_path.replace('assets/', '').replace(os.sep, '/')}"
        
        # Si se está actualizando la imagen, eliminar la anterior
        if data.image_base64:
            if instance.image:  # Eliminar la imagen anterior
                delete_image(instance.image)
            
            # Generar un nuevo nombre único para la imagen
            image_name = generate_unique_image_name(data.name)
            image_path = save_image_base64(data.image_base64, image_name)
            
            # Obtener la URL pública de la imagen
            base_url = request.base_url  # http://localhost:8000/
            image_url = f"{base_url}static/{image_path.replace('assets/', '').replace(os.sep, '/')}"        

        # Actualizar los demás campos de la tarea
        instance.name = data.name
        instance.description = data.description
        instance.status = data.status
        instance.category = data.category
        instance.user = data.user
        instance.image = image_url  # Actualizamos la ruta de la imagen

        db.commit()
        db.refresh(instance)
        return instance
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

def deleteTask(id: int, db: Session):
    try:
        instance = db.query(ModelTask).get(id)
        # instance = getByIdTask(id, db)
        if not instance:
            return {
                'message': 'Task not found'
            }
        db.delete(instance.id)
        db.commit()
        return {
            'message': 'Task deleted successfully'
        }
    except Exception as e:
        return {
            'message': f"Error in the request: {str(e)}"
        }

def pagination(page: int, size: int, db: Session, request: Request):
    try:
        page_params = PageParams(page=page, size=size)
        
        query = db.query(ModelTask)
        query_schema = [TaskSchema.from_orm(task, request) for task in query]
        
        return paginate(page_params, query, TaskSchema)
    except Exception as e:
        return {
            'message': f"Error in the request: {str(e)}"
        }


# CATEGORY
def getAllCategories(db: Session):
    try:
        response = db.query(ModelCategory).all()
        if response is None: return {'message': 'Categories not found' }
        return response
    except Exception as e:
        return {
            'message': f"Error in the request: {str(e)}"
        }

def getByIdCategory(id: int, db: Session):
    try:
        response = db.query(ModelCategory).get(id)
        if not response:
            return {
                'message': 'Category not found'
            }
        return response
    except Exception as e:
        return {
            'message': f"Error in the request: {str(e)}"
        }

def createCategory(data: CreateCategorySchema, db: Session):
    try:
        instance = ModelCategory(
            name=data.name
        )
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance
    except Exception as e:
        return {
            'message': f"Error in the request: {str(e)}"
        }

def updateCategory(id: int, data: CreateCategorySchema, db: Session):
    try:
        instance = db.query(ModelCategory).get(id) #get no soporta async
        instance.name = data.name
        db.commit()
        db.refresh(instance)
        return instance
    except Exception as e:
        return {
            'message': f"Error in the request: {str(e)}"
        }

def deleteCategory(id: int, db: Session):
    try:
        instance = db.query(ModelCategory).get(id)
        if not instance:
            return {
                'message': "Category not found"
            }
        db.delete(instance)
        db.commit()
        return {
            'message': 'Category deleted successfully'
        }
    except Exception as e:
        return {
            'message': f"Error in the request: {str(e)}"
        }


# USERS
def getAllUsers(db: Session):
    try:
        response = db.query(ModelUser).all()
        if response is None: return {'message': 'Users not found' }
        return response
    except Exception as e:
        return {
            'message': f"Error in the request: {str(e)}"
        }

def getByIdUser(id: int, db: Session):
    try:
        response = db.query(ModelUser).get(id)
        if not response:
            return {
                'message': 'User not found'
            }
        return response
    except Exception as e:
        return {
            'message': f"Error in the request: {str(e)}"
        }

def createUser(data: CreateUserSchema, db: Session):
    try:
        instance = ModelUser(
            name=data.name,
            username=data.username,
            email=data.email,
            website=data.website
        )
        if not instance:
            return {
                'message': 'Failed to create user'
            }
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance
    except IntegrityError as e:
        db.rollback()
        return {'message': "Integrity error: Duplicate entry or constraint violation"}
    except Exception as e:
        return {'message': f"Unexpected error: {str(e)}"}

def updateUser(id: int, data: CreateUserSchema, db: Session):
    try:
        instance = db.query(ModelUser).get(id)
        instance.name = data.name
        instance.username = data.username
        instance.email = data.email
        instance.website = data.website
        db.commit()
        db.refresh(instance)
        return instance
    except Exception as e:
        return {
            'message': f"Error in the request: {str(e)}"
        }

def deleteUser(id: int, db: Session):
    try:
        instance = db.query(ModelUser).get(id)
        if not instance:
            return {
                'message': 'User not found'
            }
        db.delete(instance)
        db.commit()
        return {
            'message': 'User deleted successfully'
        }
    except Exception as e:
        return {
            'message': f"Error in the request: {str(e)}"
        }

