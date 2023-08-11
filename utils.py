from email.utils import parseaddr
from fastapi import HTTPException
from model import ContactResponse, ContactInfo

def is_valid_email(email):
    """ Check validity of the email """
    try:
        parseaddr(email)
        return True
    except Exception:
        return False

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

