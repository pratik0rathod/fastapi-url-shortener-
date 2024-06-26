import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .. import config
#"postgresql://postgres:pratik@localhost/fastapi_todo_db"


URL = os.getenv('DBDRIVER')+"://"+os.getenv('DBUSER')+":"+os.getenv('DBPASSWORD')+'@'+os.getenv('DBHOST')+"/"+os.getenv('DB')

engine = create_engine(url=URL) 

session_local = sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base = declarative_base()

def get_db():
    db =  session_local()
    try:
        yield db
    except Exception as e:
        db.close()
        raise e

