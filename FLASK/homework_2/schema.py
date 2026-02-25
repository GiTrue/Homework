from pydantic import BaseModel, ValidationError, EmailStr
from errors import HttpError

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class CreateAdv(BaseModel):
    title: str
    description: str

class UpdateAdv(BaseModel):
    title: str | None = None
    description: str | None = None

def validate(schema_cls, data):
    try:
        return schema_cls(**data).model_dump(exclude_unset=True)
    except ValidationError as error:
        raise HttpError(400, error.errors())
