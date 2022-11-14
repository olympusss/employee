from pydantic import BaseModel
from typing import List

class UserSchema(BaseModel):
    name        : str
    admin       : bool
    password    : str

    class Config:
        orm_mode = True
        