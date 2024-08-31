from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from config.db import Base, engine, get_database_session
from config.pagination import PagedResponseSchema

from apps.tasks.schemas import TaskSchema, TaskCreateSchema, CreateCategorySchema, CreateUserSchema
from apps.tasks import crud

Base.metadata.create_all(bind=engine)

router_tasks = APIRouter()

@router_tasks.get('/list', status_code=status.HTTP_200_OK, tags=['Tasks'], response_model=PagedResponseSchema)
def get_all_tasks(page: int, size: int, db: Session = Depends(get_database_session)):
    return crud.pagination(page, size, db)

# Lo que se agrega en la ruta, son PARAMETROS para realizar filtrados
@router_tasks.get('/unique/{id}', status_code=status.HTTP_200_OK, tags=['Tasks'])
def get(id: int, db: Session = Depends(get_database_session)):
    return crud.getByIdTask(db, id)

# Los parametros QUERY y no se agregar en la ruta, van directo en la funcion, se pueden usar como
# @router_tasks.get('/unique/', status_code=status.HTTP_200_OK, tags=['Tasks'])
# def get_category(category: str, db: Session = Depends(get_database_session)):
#     return crud.pagination(page, size, db)


@router_tasks.post('/create_task/', status_code=status.HTTP_201_CREATED, tags=['Tasks'])
def post(task: TaskCreateSchema, db: Session = Depends(get_database_session)):
    instance = crud.createTask(task, db)
    return {
        'task': instance
    }

@router_tasks.put('/update/{id}', status_code=status.HTTP_200_OK, tags=['Tasks'])
def update(id: int, task: TaskCreateSchema, db: Session = Depends(get_database_session)):
    instance = crud.updateTask(id, task, db)
    return {
        instance
    }

@router_tasks.delete('/delete/{id}', status_code=status.HTTP_200_OK, tags=['Tasks'])
def delete(id: int, db: Session = Depends(get_database_session)):
    response =  crud.deleteTask(id, db)
    return  response


# Routes Categories
@router_tasks.get('/categories', status_code=status.HTTP_200_OK, tags=['Categories'])
def get_all_categories(db: Session = Depends(get_database_session)):
    return crud.getAllCategories(db)

@router_tasks.get('/categories/{id}', status_code=status.HTTP_200_OK, tags=['Categories'])
def get_category(id: int, db: Session = Depends(get_database_session)):
    return crud.getByIdCategory(id, db)

@router_tasks.post('/categories', status_code=status.HTTP_201_CREATED, tags=['Categories'])
def post_category(category: CreateCategorySchema, db: Session = Depends(get_database_session)):
    return crud.createCategory(category, db)

@router_tasks.put('/categories/update/{id}', status_code=status.HTTP_200_OK, tags=['Categories'])
def update_category(id: int, category: CreateCategorySchema, db: Session = Depends(get_database_session)):
    return crud.updateCategory(id, category, db)

@router_tasks.delete('/categories/delete/{id}', status_code=status.HTTP_200_OK, tags=['Categories'])
def delete_category(id: int, db: Session = Depends(get_database_session)):
    return crud.deleteCategory(id, db)


# Routes Users
@router_tasks.get('/users', status_code=status.HTTP_200_OK, tags=['Users'])
def get_all_users(db: Session = Depends(get_database_session)):
    return crud.getAllUsers(db)

@router_tasks.get('/users/{id}', status_code=status.HTTP_200_OK, tags=['Users'])
def get_user(id: int, db: Session = Depends(get_database_session)):
    return crud.getByIdUser(id, db)

@router_tasks.post('/users', status_code=status.HTTP_201_CREATED, tags=['Users'])
def post_user(user: CreateUserSchema, db: Session = Depends(get_database_session)):
    return crud.createUser(user, db)

@router_tasks.put('/users/update/{id}', status_code=status.HTTP_200_OK, tags=['Users'])
def update_user(id: int, user: CreateUserSchema, db: Session = Depends(get_database_session)):
    return crud.updateUser(id, user, db)

@router_tasks.delete('/users/delete/{id}', status_code=status.HTTP_200_OK, tags=['Users'])
def delete_user(id: int, db: Session = Depends(get_database_session)):
    return crud.deleteUser(id, db)

