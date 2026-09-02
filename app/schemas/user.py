from pydantic import BaseModel , EmailStr , field_validator , Field 
from typing import Optional ,Annotated , List
from app.utils.validators import validate_password_strength
from app.models.user import User 
from datetime import datetime 


class UserRegister(BaseModel):
    fname : str
    lname  : str
    email : EmailStr
    password : str
    phone : Annotated[
        str ,
        Field(
            min_length=10, 
            max_length=10 , 
            pattern=r"[6-9]\d{9}$"
        )
    ]
    @field_validator("password")
    @classmethod
    def validate_password_strengths(cls , password :str) -> str:
        return validate_password_strength(password)
    
class ResetPasswordRequest(BaseModel):
    email : EmailStr
    otp : str
    password : str
    @field_validator("password")
    @classmethod
    def validate_password(cls , password : str)-> str:
        return validate_password_strength(password)

class LoginUserRequest(BaseModel):
    email : EmailStr
    password : str
class LoginUserResponse(BaseModel):
    access_token : str
    refresh_token: str
    token_type : str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class UserUpdate(BaseModel):
    fname : Optional[str] = None
    lname : Optional[str] = None
    phone : Optional[str]= None
    is_active : Optional[bool] = None
    roleId : Optional[str] = None

class UpdatedUserResponse(BaseModel):
    fname : str
    lname : str
    phone : str
    roleId : str
    is_active : bool
    email : EmailStr
    is_emailverified : bool

class UserResponse(BaseModel):
    id: str
    fname: Optional[str] = None
    lname: Optional[str] = None
    email: EmailStr
    roleId: str
    phone: Optional[str] = None
    is_active: bool
    is_emailverified: bool
    last_loginAt: Optional[datetime] = None
    createdAt: datetime
    updatedAt: Optional[datetime] = None

class ChangePassword(BaseModel):
    userId : str
    old_password : str
    new_password : str
    @field_validator("new_password")
    @classmethod
    def validate_password(cls , new_password : str)-> str:
        return validate_password_strength(new_password)

class UserGetResponse(BaseModel):
    success : bool
    page : int
    limit : int
    total : int
    pages : int
    data : List[UserResponse]

class DeleteorRestoreUserResponse(BaseModel):
    message: str
    email : EmailStr