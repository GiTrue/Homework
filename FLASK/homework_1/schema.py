from pydantic import BaseModel, ValidationError
from errors import HttpError

class CreateAdv(BaseModel):
    title: str
    description: str
    owner: str

class UpdateAdv(BaseModel):
    title: str | None = None
    description: str | None = None
    owner: str | None = None

def validate(schema_cls, data):
    try:
        return schema_cls(**data).model_dump(exclude_unset=True)
    except ValidationError as error:
        raise HttpError(400, error.errors())
