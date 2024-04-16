import re
import random
from datetime import datetime,timedelta
from fastapi import HTTPException
from . import database,schema,models,auth
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.encoders import jsonable_encoder
import string

def generate_alias():
    urlstring = string.digits + string.ascii_letters
    temp = [random.choice(urlstring) for _ in range(0,4)]
    return "".join(temp)

def create_shorturl(db:Session,userid:int,data:schema.ShortUrl):
    try:
        if data.alias is None:
            data.alias = generate_alias()    
            while db.query(models.ShortUrls).filter(models.ShortUrls.alias == data.alias).first() is not None:
                data.alias = generate_alias()
        
        user = auth.get_dbuser(db,userid)      
        
        my_url_model =  models.ShortUrls(url = str(data.url),alias = data.alias,expire_on =data.expire_on,author=user.id) 
       
       
        if data.expire_on:
            if data.expire_on < timedelta(0):
                raise HTTPException(status_code=400,detail={"error":"timedelta should be possitive"})
            
        if db.query(models.ShortUrls).filter(models.ShortUrls.alias == my_url_model.alias).first() is not None:
            raise HTTPException(status_code=409,detail={"error":"please choice another alias its already taken by someone"})
        
        db.add(my_url_model)
        db.commit()

        return {"Sucess":"Url created successfully at: http://localhost:8000/"+my_url_model.alias}
    
    except HTTPException as e:
        raise e
    
    except Exception as e:

        print(e)
        
        raise HTTPException(status_code=500,detail={"error":"sorry this dev is too dumb to handle this error"})


def get_url(db:Session,url:str):
    try:
        urlmodel = db.query(models.ShortUrls).filter(models.ShortUrls.alias == url).first()
      
        if urlmodel:
            if urlmodel.expire_on is not None:
                if urlmodel.created_on + urlmodel.expire_on <= datetime.now():                    
                    raise HTTPException(status_code=403,detail={"error":"url expired"})

            urlmodel.total_clicks = urlmodel.total_clicks + 1
            db.add(urlmodel)
            db.commit() 
            return urlmodel.url
        
        raise HTTPException(status_code=404,detail={"error":"Page not found"})
    
    except HTTPException as e:
       raise e
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500,detail={"error":"sorry this dev is too dumb to handle this error"})


def get_all_url(db:Session,userid:int):
    return jsonable_encoder(db.query(models.ShortUrls).filter(models.ShortUrls.author == userid).all()) 

def get_url_by_id(db:Session,userid:int,item_id:int):
    item = db.query(models.ShortUrls).filter(models.ShortUrls.author == userid,models.ShortUrls.id == item_id).first()
    if item is not None:
        return jsonable_encoder(item)
    raise HTTPException(status_code=404,detail={"error":"Item not found"})

def delete_url_by_id(db:Session,userid:int,item_id:int):
    item = db.query(models.ShortUrls).filter(models.ShortUrls.author == userid,models.ShortUrls.id == item_id).first()
    
    if item is not None:
        db.delete(item)
        db.commit()
        return {"success":"Item deleted successfully"}
    raise HTTPException(status_code=404,detail={"error":"Item not found"})

def search_url(db:Session,userid:int,search_term:schema.UrlFilter):
    urls = select(models.ShortUrls)
    urls = search_term.filter(urls)
    urls = urls.filter(models.ShortUrls.author == userid)
    results = db.execute(urls)
    return jsonable_encoder(results.scalars().all())