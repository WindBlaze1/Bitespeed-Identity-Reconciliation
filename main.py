"""imports"""
from fastapi import FastAPI
from db import SQLite

app = FastAPI()

@app.get('/identify')
def root(email:str|None=None, phoneNumber:int|None=None):
    """ Main function containing the functional implementation """
    db = SQLite('test_data.sqlite3')
    data = db.run_query('SELECT * FROM contacts')
    print(data)
    return {'message':'Hello'}
