import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .. import config
#"postgresql://postgres:pratik@localhost/fastapi_todo_db"


URL = os.getenv('DBDRIVER')+"://"+os.getenv('DBUSER')+":"+os.getenv('DBPASSWORD')+'@'+os.getenv('DBHOST')+"/"+os.getenv('DB')
print(URL)

engine = create_engine(url=URL) 

session_local = sessionmaker(bind=engine,autoflush=False,autocommit=False)

Base = declarative_base()

print(session_local)



