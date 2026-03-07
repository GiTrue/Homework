from pydantic import BaseModel

class CreateAdv(BaseModel):
    title: str
    description: str
    owner: str

class UpdateAdv(BaseModel):
    title: str | None = None
    description: str | None = None
