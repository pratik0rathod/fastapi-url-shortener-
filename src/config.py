import os

from dotenv import load_dotenv,dotenv_values

if load_dotenv():
    config = dotenv_values("../.env") 
    for entity in config:
        os.environ[entity] = config.get(entity)