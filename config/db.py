from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base

DATA_URL="postgresql://postgres:admin@192.168.18.132:5432/practice_fastapi_db"
engine = create_engine(DATA_URL, echo=True) # echo=True para ver las consultas SQL que se ejecutan
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_database_session():
    try:
        db = SessionLocal()
        yield db # Yield es como un return pero para generadores, pero no termina la ejecución de la función
        # return db # Return termina la ejecución de la función, y retorna el valor
    # except:
    finally:
        db.close()