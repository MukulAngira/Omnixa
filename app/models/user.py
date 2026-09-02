from beanie import Document
from pydantic import EmailStr
from typing import Optional

from datetime import datetime , timezone

class User(Document):
    fname : str
    lname : str 

    email : EmailStr
    password : str

    roleId : Optional[str] = None

    is_active :bool = True
    is_emailverified : bool = False 

    phone : str 
    last_loginAt : Optional[datetime]= None
    createdAt : datetime = datetime.now(timezone.utc)
    deletedAt : Optional[datetime] = None
    deletedAt : Optional[datetime] = None

    class Settings:
        name = "users"
        indexes = [
            "email",
            "phone",
            "roleId"
        ]
