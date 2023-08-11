""" imports """
from typing import List
from pydantic import BaseModel

class ContactInfo(BaseModel):
    """ wrapping this around another class """
    primaryContactId: int
    emails: List[str]
    phoneNumbers: List[int]
    secondaryContactIds: List[int]

class ContactResponse(BaseModel):
    """ class to define the return type """
    contact: ContactInfo

class Data(BaseModel):
    """ class to get to post request data """
    phoneNumber: int | None = None
    email: str | None = None