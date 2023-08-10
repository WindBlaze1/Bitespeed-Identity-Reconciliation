""" imports """
from fastapi import FastAPI, HTTPException
from db import SQLite
from email.utils import parseaddr

def is_valid_email(email):
    """ Check validity of the email """
    try:
        parseaddr(email)
        return True
    except:
        return False

app = FastAPI()

@app.get('/identify')
def root(email: str | None = None, phoneNumber : int | None = None):
    """ Main function containing the functional implementation """
    db = SQLite('test_data.sqlite3')

    if email and not is_valid_email(email):
        return HTTPException(status_code=400, detail='invalid email. try again.')

    if email is None and phoneNumber is None:
        return HTTPException(status_code=400, detail='both email \
                             and phoneNumber cannot be empty. try again.')

    if email is None or phoneNumber is None:
        # one of the two is none i.e. check for entries in db
        pass
    else: # if both are not null -> 2 cases:
        # if one of the entry is found in db: write the other in db and return result
        # if none found, create a new 
        pass


    # data = db.run_query('SELECT * FROM contacts')
    # print(data)
    # return {'message':'Hello'}
