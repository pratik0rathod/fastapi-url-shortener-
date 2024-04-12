from fastapi import APIRouter,HTTPException

auth_route =  APIRouter(
    prefix="/auth",
    tags=['Auth']
    )

shortner_route = APIRouter(
    prefix="/url-shortner",
    tags = ['Shortner']
    )




@auth_route.get('/me')
async def me():
    raise  HTTPException(status_code=400,detail={"error":"This route being developed"})

@auth_route.post('/login')
async def login():
    raise  HTTPException(status_code=400,detail={"error":"This route being developed"})
    

@auth_route.post('/register')
async def register():
    raise  HTTPException(status_code=400,detail={"error":"This route being developed"})


# Url shortner 

@shortner_route.get("/all")
async def all_url():
    raise  HTTPException(status_code=400,detail={"error":"This route being developed"})


@shortner_route.get("/get/{item_id}")
async def create_url():
    raise  HTTPException(status_code=400,detail={"error":"This route being developed"})

@shortner_route.get("/search/")
async def create_url():
    raise  HTTPException(status_code=400,detail={"error":"This route being developed"})


@shortner_route.post("/create")
async def create_url():
    raise  HTTPException(status_code=400,detail={"error":"This route being developed"})

@shortner_route.delete("/delete/{item_id}")
async def create_url():
    raise  HTTPException(status_code=400,detail={"error":"This route being developed"})
