from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from connection import Base, engine, get_db
from models import User, Company, Department, Employee
from schemas import (
    UserSchema, PostDefault, CreateCompany, CreateDepartment, CreateEmployee, Search)

app = FastAPI()

Base.metadata.create_all(engine)


@app.post("/api/create-user")
async def create_user(user: UserSchema, db: Session = Depends(get_db)):
    new_add = User(**user.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return "Success"
    else:
        return "Error"



@app.get("/api/get-user")
async def get_users(db: Session = Depends(get_db)):
    result = db.query(
        User.id,
        User.name,
        User.admin,
        User.password,
        User.create_At,
        User.update_At
    ).all()
    if result:
        return result
    else:
        return False



# @app.post('/api/create-company')
# async def create_company(req: CreateCompany, db: Session = Depends(get_db)):
#     new_add = Company(
#         name = req.name
#     )
#     db.add(new_add)
#     db.commit()
#     db.refresh(new_add)
#     if new_add:
#         return new_add
#     else:
#         return False



# @app.post('/api/create-department')
# async def create_department(req: CreateDepartment, db: Session = Depends(get_db)):
#     new_add = Department(        
#         name        = req.name,
#         company_id  = req.company_id
#     )
#     db.add(new_add)
#     db.commit()
#     db.refresh(new_add)
#     if new_add:
#         return new_add
#     else:
#         return False


# @app.post('/api/create-employee')
# async def create_employee(req: CreateEmployee, db: Session = Depends(get_db)):
#     new_add = Employee(
#         name            = req.name,
#         surname         = req.surname,
#         job_title       = req.job_title,
#         department_id   = req.department_id  
#     )
#     db.add(new_add)
#     db.commit()
#     db.refresh(new_add)
#     if new_add:
#         return new_add
#     else:
#         return False


# 1
@app.post('/api/get-company-department-count')
async def get_company_department_count(req: PostDefault, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    subq = db.query(func.count(Department.id)).filter(Department.company_id == Company.id).label('department_count')
    res = db.query(
            Company.id,
            Company.name,
            subq
        ).all()
    if res:
        return res
    else:
        return False


# 2
@app.post('/api/get-company-department-list')
async def get_company_department_list(req: PostDefault, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    res = db.query(
            Company.id,
            Company.name,
        ).all()
    new_list = []
    for comp in res:
        comp = dict(comp)
        dep = db.query(Department.id, Department.name).filter(Department.company_id == comp['id']).all()
        comp['department_list'] = list(dep)
        new_list.append(comp)
    res = new_list
    if res:
        return res
    else:
        return False


# 3
@app.post('/api/get-department-employee-count')
async def get_department_employee_count(req: PostDefault, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    subq = db.query(func.count(Employee.id)).filter(Employee.department_id == Department.id).label('employee_count')
    res = db.query(
        Department.id.label('department_id'),
        Department.name.label('department_name'),
        Company.id.label('company_id'),
        Company.name.label('company_name'),
        subq
    ).join(Company, Company.id == Department.company_id).all()
    if res:
        return res
    else:
        return False
    

# 4
@app.post('/api/get-department-employee-list')
async def get_department_employee_list(req: PostDefault, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    res = db.query(
        Department.id.label('department_id'),
        Department.name.label('department_name'),
        Company.id.label('company_id'),
        Company.name.label('company_name')
    ).join(Company, Company.id == Department.company_id).all()
    new_list = []
    for dep in res:
        dep = dict(dep)
        emp = db.query(Employee.id, Employee.name, Employee.surname, Employee.job_title)\
            .filter(Employee.department_id == dep['department_id']).all()
        dep['employee_list'] = list(emp)
        new_list.append(dep)
    res = new_list
    if res:
        return res
    else:
        return False


# 5
@app.post('/api/employee-list')
async def get_employee_list(req: PostDefault, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin:
        return False
    res = db.query(
        Employee.id,
        Employee.name,
        Employee.surname,
        Employee.job_title,
        Company.name,
        Department.name
    ).join(Department, Department.id == Employee.department_id)\
        .join(Company, Company.id == Department.company_id)\
            .all()
    if res:
        return res
    else:
        return False


# 6 - Create
@app.post('/api/create-company')
async def create_company(req: CreateCompany, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    new_add = Company(
        name        = req.comp_name
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return new_add
    else:
        return False


# 6 - Update
@app.put('/api/update-company')
async def update_company(id: int, req: CreateCompany, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    new_update = db.query(Company).filter(Company.id == id)\
        .update({
            Company.name    : req.comp_name
        }, synchronize_session=False)
    db.commit()
    if new_update:
        return "Success"
    else:
        return False



# 6 - Delete
@app.delete('/api/delete-company')
async def delete_company(id: int, req: PostDefault, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    new_delete = db.query(Company).filter(Company.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        return "Success"
    else:
        return False


# 6 - Search
@app.post('/api/search-company')
async def search_company(req: Search, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    res = db.query(Company.id, Company.name).filter(Company.name.like(f"%{req.text}%")).all()
    if res:
        return res
    else:
        return False