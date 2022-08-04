
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



'''
#-----------------------------
# run the Postgrs server
import psycopg2
# to return the Postgres table with their volumn title
from psycopg2.extras import RealDictCursor 

while True:
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(host = 'localhost', database='fastapi', 
                                user ='postgres', password='Jimboo1155',
                                cursor_factory=RealDictCursor )

        # Open a cursor to perform database operations
        cursor = conn.cursor()
        print('database connection was succesfull!!!')
        break
    except Exception as error:
        print('database connection was failed!!!')
        print('Erorr : ',  error)
        time.sleep(2)
'''
