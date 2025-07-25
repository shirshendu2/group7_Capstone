from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    age: int
    designation: str
    salary: float


class UserLogin(BaseModel):
    email: str
    password: str