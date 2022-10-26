from fastapi import FastAPI, Depends
from app.utils.config import settings
from app.routers import authenticationActivities, userActivities
from fastapi.middleware.cors import CORSMiddleware
from app.utils.dbinit import databaseInit
from app.utils import dbConnection
from sqlalchemy.orm import Session

app = FastAPI(
    title =settings.PROJECT_NAME
)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
get_db = dbConnection.get_db

@app.get("/db-startup")
async def dbSetup(db: Session = Depends(get_db)):
    return databaseInit(db)
    
@app.get("/")
async def root():
    return {"message": "Hello World"}

app.include_router(authenticationActivities.router)
app.include_router(userActivities.router)