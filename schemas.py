from pydantic import BaseModel
from typing import List

class UserSchema(BaseModel):
    name        : str
    admin       : bool
    password    : str

    class Config:
        orm_mode = True
        

class PostDefault(BaseModel):
    name        : str
    admin       : bool

    class Config:
        orm_mode = True


class CreateCompany(PostDefault):
    comp_name        : str

    class Config:
        orm_mode = True


class CreateDepartment(PostDefault):
    dep_name        : str
    company_id      : int

    class Config:
        orm_mode = True

class CreateEmployee(PostDefault):
    emp_name            : str
    surname             : str
    job_title           : str
    department_id       : int

    class Config:
        orm_mode = True


class Search(PostDefault):
    text    :   str

    class Config:
        orm_mode = True