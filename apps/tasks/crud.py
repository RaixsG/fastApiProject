from sqlalchemy.orm import Session
from .models import ModelTask, ModelCategory, ModelUser
from .schemas import TaskSchema, CreateUserSchema, CreateCategorySchema

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from config.pagination import paginate, PageParams

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

def getByIdTask(db: Session, id: int):
    try:
        response = db.query(ModelTask).get(id)
        if not response:
            return {
                'message': 'Task not found'
            }
        return response
    except Exception as e:
        return {
            'message': f"Error in the request: {str(e)}"
        }

def createTask(data: TaskSchema, db: Session):
    try:
        instance = ModelTask(
            name=data.name,
            description=data.description,
            status=data.status,
            category=data.category,
            user=data.user
        )
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance
    except Exception as e:
        return {
            'message': f"Error in the request: {str(e)}"
        }

def updateTask(id: int, data: TaskSchema, db: Session):
    instance = db.query(ModelTask).get(id) #get no soporta async
    instance.name = data.name
    instance.description = data.description
    instance.status = data.status
    instance.category = data.category
    instance.user = data.user
    db.commit()
    db.refresh(instance)
    return instance

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

def pagination(page: int, size: int, db: Session):
    page_params = PageParams(page=page, size=size)
    return paginate(page_params, db.query(ModelTask), TaskSchema)


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

