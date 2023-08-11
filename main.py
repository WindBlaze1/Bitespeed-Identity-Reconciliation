""" imports """
from fastapi import FastAPI, HTTPException
from model import ContactResponse, Data
from db import SQLite
from utils import get_return_data,is_valid_email

app = FastAPI()


@app.post('/identify', response_model=ContactResponse)
def root(request: Data):
    """ Main function containing the whole functional implementation """
    db = SQLite('test_data.sqlite3')
    email = request.email
    phoneNumber = request.phoneNumber
    print('request received with params: ',request)

    if email is None and phoneNumber is None:
        raise HTTPException(status_code=400, detail='both email \
and phoneNumber cannot be empty. try again.')

    if email and not is_valid_email(email):
        raise HTTPException(status_code=400, detail='invalid email. try again.')


    if email is None or phoneNumber is None:
        # one of the two is none i.e. check for entries in db
        if email is None:
            res = db.run_query(f'SELECT * FROM contacts WHERE phoneNumber={phoneNumber}')
            return get_return_data(res)
        # phoneNumber is None:
        res = db.run_query(f"SELECT * FROM contacts WHERE email='{email}'")
        return get_return_data(res)
    # else: # if both are not null -> 4 cases: [00,01,10,11]
    email_entry = db.run_query(f"SELECT * FROM contacts WHERE email='{email}'")
    phone_entry = db.run_query(f"SELECT * FROM contacts WHERE phoneNumber={phoneNumber}")
    # 00: both not found: create new entry and return
    print('phone_entry:',phone_entry)
    print('email_entry:',email_entry)
    if len(email_entry) == 0 and len(phone_entry) == 0:
        print('case: both new entries, adding to db...')
        db.run_query(f"INSERT INTO contacts (phoneNumber, email, \
                                    linkedId, linkPrecedence) VALUES ({phoneNumber},\
                                    '{email}',NULL,'primary')")
        return get_return_data(db.run_query(f"SELECT * FROM contacts WHERE phoneNumber={phoneNumber} OR email='{email}'"))
    # 01: email present but phone is not: make a new secondary entry
    if len(email_entry) and len(phone_entry) == 0:
        # create new entry
        print('case 01')
        for entry in email_entry:
            if entry[3] is not None:
                linked_id = entry[3]
            else:
                linked_id = entry[0]
            break
        print(linked_id)
        db.run_query(f"INSERT INTO contacts (phoneNumber, email, linkedId, linkPrecedence)\
                        VALUES ({phoneNumber},'{email}','{linked_id}','secondary')")
        return get_return_data(db.run_query(f"SELECT * FROM contacts WHERE id={linked_id} OR linkedId={linked_id}"))
    # 10: phone present but email is not: make a new secondary entry
    if len(phone_entry) and len(email_entry) == 0:
        # create new entry[row]
        print('case 10')
        for entry in phone_entry:
            if entry[3] is not None:
                linked_id = entry[3]
            else:
                linked_id = entry[0]
            break
        print(linked_id)
        db.run_query(f"INSERT INTO contacts (phoneNumber, email, linkedId, linkPrecedence)\
                        VALUES ({phoneNumber},'{email}','{linked_id}','secondary')")
        return get_return_data(db.run_query(f"SELECT * FROM contacts WHERE id={linked_id} OR linkedId={linked_id}"))
    # elif both found[11], 3 cases:
    print('case 11')
    # Case 1: an entry is already present which contains both:
    res = db.run_query(f"SELECT * FROM contacts WHERE phoneNumber={phoneNumber} AND email='{email}'")
    if len(res) != 0:
        # then update the UpdatedAt value of the row
        res = res[0]
        if res[3] is not None:
            linked_id = res[3]
        else:
            linked_id = res[0]
        db.run_query(f"UPDATE contacts SET updatedAt = DATETIME('now') \
                     WHERE phoneNumber={phoneNumber} AND email='{email}'")
        return get_return_data(db.run_query(f"SELECT * FROM contacts WHERE id={linked_id} OR linkedId={linked_id}"))
    # Case 2&3: More than 1 entry present:
    # if both found in different rows, merge them
    # check for entries with different linkedId
    # and make them one if there are more than one[ie 2]
    IDs = db.run_query(f"SELECT DISTINCT(linkedId) FROM contacts \
                       WHERE (phoneNumber={phoneNumber} OR email='{email}') AND linkedId IS NOT NULL")
                                                                            # Null linkedId is for primary
    # Case 2: linked id is same for all
    # add the new entry and return
    if len(IDs) == 1:
        db.run_query(f"INSERT INTO contacts (phoneNumber, email, linkedId, linkPrecedence)\
                        VALUES ({phoneNumber},'{email}','{IDs[0][0]}','secondary')")
        return get_return_data(db.run_query(f"SELECT * FROM contacts \
                                            WHERE phoneNumber={phoneNumber} OR email='{email}'"))
    # Case 3: linked id is different: need to combine both the results
    #         into the one which was earlier updated
    id = str(IDs[0][0]) + ',' + str(IDs[1][0])
    # get both the primary IDs sorted acc to creation time
    change_in_id = db.run_query(f'SELECT id FROM contacts \
                                WHERE id IN ({id}) ORDER BY createdAt')
    print(change_in_id)
    # the latter one and all its connections will be set to the former one
    # so that the person is one and not two
    db.run_query(f"UPDATE contacts SET linkPrecedence='secondary', linkedId={change_in_id[0][0]}\
                    WHERE id={change_in_id[1][0]} AND linkPrecedence='primary'")
                    # change primary of second ID
    db.run_query(f"UPDATE contacts SET linkedId={change_in_id[0][0]}\
                    WHERE linkedId={change_in_id[1][0]} AND linkPrecedence='secondary'")
                    # change all secondary of the second ID to point to first ID
    linked_id = change_in_id[0][0]
    return get_return_data(db.run_query(f"SELECT * FROM contacts WHERE id={linked_id} OR linkedId={linked_id}"))
