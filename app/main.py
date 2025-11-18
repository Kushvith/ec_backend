from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Shoplite")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root(): 
    return {"message": "Welcome to Shoplite!"}