from fastapi import FastAPI
from db import SQLite

app = FastAPI()

@app.get('/identify')
def root(email:str, phoneNumber:int):
    
    return {'message':'Hello'}
