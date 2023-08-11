""" imports """
from email.utils import parseaddr
from fastapi import FastAPI, HTTPException
from db import SQLite

def is_valid_email(email):
    """ Check validity of the email """
    try:
        parseaddr(email)
        return True
    except:
        return False

app = FastAPI()

def get_return_data(lst: list) -> dict | HTTPException:
    """ function to parse the table data according to assignment's response """

    if len(lst) == 0:
        return HTTPException(status_code=404, detail='entry not found.')
    
    if lst[0][4] == 'primary':
        primary_id = lst[0][0]
    else:
        primary_id = lst[0][3]

    email_list = []
    phone_list = []
    secondary_id_list = []

    for item in lst:
        if item[4] != 'primary':
            secondary_id_list.append(item[0])
        if item[1] not in phone_list:
            phone_list.append(item[1])
        if item[2] not in email_list:
            email_list.append(item[2])

    return {
        'contact':{
            "primaryContactId": primary_id,
			"emails": email_list,
			"phoneNumbers": phone_list,
			"secondaryContactIds": secondary_id_list,
        }
    }


@app.get('/identify')
def root(email: str | None = None, phoneNumber : int | None = None) -> dict | HTTPException:
    """ Main function containing the functional implementation """
    db = SQLite('test_data.sqlite3')

    if email and not is_valid_email(email):
        return HTTPException(status_code=400, detail='invalid email. try again.')

    if email is None and phoneNumber is None:
        return HTTPException(status_code=400, detail='both email \
                             and phoneNumber cannot be empty. try again.')

    if email is None or phoneNumber is None:
        # one of the two is none i.e. check for entries in db
        if email is None:
            res = db.run_query(f'SELECT * FROM contacts WHERE phoneNumber={phoneNumber}')
            return get_return_data(res)
        # phoneNumber is None:
        res = db.run_query(f'SELECT * FROM contacts WHERE email={email}')
        return get_return_data(res)
    else: # if both are not null -> 4 cases: [00,01,10,11]
        # if one of the entry is found in db: write the other in db and return result
        email_entry = db.run_query(f'SELECT * FROM contacts WHERE email={email}')
        phone_entry = db.run_query(f'SELECT * FROM contacts WHERE phoneNumber={phoneNumber}')
        # 00: both not found: create new entry
        if len(email_entry) == 0 and len(phone_entry) == 0:
            new_entry = db.run_query(f"INSERT INTO contacts (phoneNumber, email, \
                                     linkedId, linkPrecedence) VALUES ('{phoneNumber}',\
                                     '{email}',NULL,'primary')")
            return get_return_data(db.run_query(f'SELECT * FROM contacts WHERE phoneNumber={phoneNumber}'))
        if len(email_entry) and len(phone_entry) == 0:
            # create new entry
            for entry in email_entry:
                if entry[3] is not None:
                    linked_id = entry[3]
                    break
            db.run_query(f"INSERT INTO contacts (phoneNumber, email, linkedId, linkPrecedence)\
                         VALUES ('{phoneNumber}','{email}','{linked_id}','secondary')")
            return get_return_data(db.run_query(f'SELECT * FROM contacts WHERE phoneNumber={phoneNumber}'))
        elif len(phone_entry) and len(email_entry) == 0:
            # create new entry
            for entry in phone_entry:
                if entry[3] is not None:
                    linked_id = entry[3]
                    break
            db.run_query(f"INSERT INTO contacts (phoneNumber, email, linkedId, linkPrecedence)\
                         VALUES ('{phoneNumber}','{email}','{linked_id}','secondary')")
            return get_return_data(db.run_query(f'SELECT * FROM contacts WHERE phoneNumber={phoneNumber}'))
        # else:# if both found, 2 cases:
        # if both found in different rows, merge them
        # check for entries with different linkedId 
        # and make them one if there are more than one
        IDs = db.run_query(f'SELECT DISTINCT(linkedId) FROM contacts WHERE email={email}')
        id = str(IDs[0]) + ',' + str(IDs[1])
        change_in_id = db.run_query(f'SELECT id FROM contacts \
                                    WHERE id IN [{id}] ORDER BY createdAt')
        # now change the contents of 2nd ID to the first
        # as both persons are the same
        db.run_query(f"UPDATE TABLE contacts SET linkPrecedence='secondary', linkedId={change_in_id[0]}\
                        WHERE id={change_in_id[1]} AND linkPrecedence='primary'")
        db.run_query(f"UPDATE TABLE contacts SET linkedId={change_in_id[0]}\
                        WHERE linkedId={change_in_id[1]} AND linkPrecedence='secondary")

    # data = db.run_query('SELECT * FROM contacts')
    # print(data)
    # return {'message':'Hello'}
