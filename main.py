""" imports """
from email.utils import parseaddr
from fastapi import FastAPI, HTTPException
from model import ContactResponse, ContactInfo, Data
from db import SQLite

def is_valid_email(email):
    """ Check validity of the email """
    try:
        parseaddr(email)
        return True
    except:
        return False

app = FastAPI()

def get_return_data(lst: list) -> ContactResponse | HTTPException:
    """ function to parse the table data according to assignment's response """

    if len(lst) == 0:
        raise HTTPException(status_code=404, detail='entry not found.')
    
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

    return ContactResponse(
        contact=ContactInfo(
            primaryContactId=primary_id,
            emails=email_list,
            phoneNumbers=phone_list,
            secondaryContactIds=secondary_id_list
        )
    )


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
        # if one of the entry is found in db: write the other in db and return result
    email_entry = db.run_query(f"SELECT * FROM contacts WHERE email='{email}'")
    phone_entry = db.run_query(f'SELECT * FROM contacts WHERE phoneNumber={phoneNumber}')
    # 00: both not found: create new entry and return
    if len(email_entry) == 0 and len(phone_entry) == 0:
        db.run_query(f"INSERT INTO contacts (phoneNumber, email, \
                                    linkedId, linkPrecedence) VALUES ({phoneNumber},\
                                    '{email}',NULL,'primary')")
        return get_return_data(db.run_query(f'SELECT * FROM contacts WHERE phoneNumber={phoneNumber}'))
    # 01: email present but phone is not: make a new secondary entry
    if len(email_entry) and len(phone_entry) == 0:
        # create new entry
        for entry in email_entry:
            if entry[3] is not None:
                linked_id = entry[3]
                break
        db.run_query(f"INSERT INTO contacts (phoneNumber, email, linkedId, linkPrecedence)\
                        VALUES ({phoneNumber},'{email}','{linked_id}','secondary')")
        return get_return_data(db.run_query(f"SELECT * FROM contacts WHERE email='{email}'"))
    # 01: phone present but email is not: make a new secondary entry
    if len(phone_entry) and len(email_entry) == 0:
        # create new entry
        for entry in phone_entry:
            if entry[3] is not None:
                linked_id = entry[3]
                break
        db.run_query(f"INSERT INTO contacts (phoneNumber, email, linkedId, linkPrecedence)\
                        VALUES ({phoneNumber},'{email}','{linked_id}','secondary')")
        return get_return_data(db.run_query(f'SELECT * FROM contacts WHERE phoneNumber={phoneNumber}'))
    # elif both found[11], 3 cases:
    # Case 1: an entry is already present which contains both:
    res = db.run_query(f"SELECT * FROM contacts WHERE phoneNumber={phoneNumber} AND email='{email}'")
    if len(res) != 0:
        # then update the UpdatedAt value of the row
        db.run_query(f"UPDATE TABLE contacts SET updatedAt = NOW() \
                     WHERE phoneNumber={phoneNumber} AND email='{email}'")
        return get_return_data(db.run_query(f'SELECT * FROM contacts WHERE phoneNumber={phoneNumber}'))
    # Case 2&3: More than 1 entry present:
    res = db.run_query(f"SELECT * FROM contacts WHERE phoneNumber={phoneNumber} OR email='{email}'")
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
                        VALUES ({phoneNumber},'{email}','{IDs[0]}','secondary')")
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
    db.run_query(f"UPDATE TABLE contacts SET linkPrecedence='secondary', linkedId={change_in_id[0][0]}\
                    WHERE id={change_in_id[1][0]} AND linkPrecedence='primary'")
                    # change primary of second ID
    db.run_query(f"UPDATE TABLE contacts SET linkedId={change_in_id[0][0]}\
                    WHERE linkedId={change_in_id[1][0]} AND linkPrecedence='secondary")
                    # change all secondary of the second ID to point to first ID

    # data = db.run_query('SELECT * FROM contacts')
    # print(data)
    # return {'message':'Hello'}
