from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import auth
from app.db.base_class import Base
from app.db.session import engine

#create the tables if does not exist
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Shoplite")

app.mount("/static", StaticFiles(directory="static"), name="static")

#routes
#public routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])




@app.get("/")
def read_root(): 
    return {"message": "Welcome to Shoplite!"}