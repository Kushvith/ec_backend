


from pydantic import BaseModel, EmailStr

#shared properties
class UserBase(BaseModel):
    email: EmailStr
    name: str

#recieve from client
class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


#properties to return to client

class UserInDBBase(UserBase):
    id: int
    is_active: int
    is_admin: int
    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str