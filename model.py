from typing import List
from pydantic import BaseModel

class ContactInfo(BaseModel):
    """ warpping this around another clas """
    primaryContactId: int
    emails: List[str]
    phoneNumbers: List[int]
    secondaryContactIds: List[int]

class ContactResponse(BaseModel):
    """ class to define the return type """
    contact: ContactInfo
