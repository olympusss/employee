from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from connection import Base, engine, get_db
from models import User, Company, Department, Employee
from schemas import (
    UserSchema, PostDefault, CreateCompany, CreateDepartment, CreateEmployee, Search, SearchUser)

app = FastAPI()

Base.metadata.create_all(engine)

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
    db.query(Department).filter(Department.company_id == id).delete(synchronize_session=False)
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


# 7 - Create
@app.post('/api/create-department')
async def create_department(req: CreateDepartment, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    new_add = Department(
        name        = req.dep_name,
        company_id  = req.company_id
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return new_add
    else:
        return False


# 7 - Update
@app.put('/api/update-department')
async def update_department(id: int, req: CreateDepartment, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    new_update = db.query(Department).filter(Department.id == id)\
        .update({
            Department.name         : req.dep_name,
            Department.company_id   : req.company_id 
        }, synchronize_session=False)
    db.commit()
    if new_update:
        return "Success"
    else:
        return False


# 7 - Delete
@app.delete('/api/delete-department')
async def delete_department(id: int, req: PostDefault, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    db.query(Employee).filter(Employee.department_id == id).delete(synchronize_session=False)
    new_delete = db.query(Department).filter(Department.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        return "Success"
    else:
        return False

# 7 - Search
@app.post('/api/search-department')
async def search_department(req: Search, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    res = db.query(Department.id, Department.name).filter(Department.name.like(f"%{req.text}%")).all()
    if res:
        return res
    else:
        return False


# 8 - Create
@app.post('/api/create-employee')
async def create_employee(req: CreateEmployee, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    new_add = Employee(
        name            = req.emp_name,
        surname         = req.surname,
        job_title       = req.job_title,
        department_id   = req.department_id
    )
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return new_add
    else:
        return False


# 8 - Update
@app.put('/api/update-employee')
async def update_employee(id: int, req: CreateEmployee, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    new_update = db.query(Employee).filter(Employee.id == id)\
        .update({
            Employee.name           : req.emp_name,
            Employee.surname        : req.surname,
            Employee.job_title      : req.job_title,
            Employee.department_id  : req.department_id
        }, synchronize_session=False)
    db.commit()
    if new_update:
        return "Success"
    else:
        return False


# 8 - Delete
@app.delete('/api/delete-employee')
async def delete_employee(id: int, req: PostDefault, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    new_delete = db.query(Employee).filter(Employee.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        return "Success"
    else:
        return False


# 8 - Search
@app.post('/api/search-employee')
async def search_department(req: Search, db: Session = Depends(get_db)):
    is_admin = db.query(User).filter(and_(User.name == req.name, User.admin == req.admin)).first()
    if not is_admin or is_admin.admin is False:
        return False
    res = db.query(Employee.id, Employee.name, Employee.surname, Employee.job_title)\
        .filter(Employee.name.like(f"%{req.text}%")).all()
    if res:
        return res
    else:
        return False


# 9 - Create
@app.post("/api/create-user")
async def create_user(user: UserSchema, db: Session = Depends(get_db)):
    new_add = User(**user.dict())
    db.add(new_add)
    db.commit()
    db.refresh(new_add)
    if new_add:
        return "Success"
    else:
        return False


# 9 - Update
@app.put('/api/update-user')
async def update_user(id: int, req: UserSchema, db: Session = Depends(get_db)):
    new_update = db.query(User).filter(User.id == id)\
        .update({
            User.name       : req.name,
            User.admin      : req.admin,
            User.password   : req.password
        }, synchronize_session=False)
    db.commit()
    if new_update:
        return "Success"
    else:
        return False


# 9 - Delete
@app.delete('/api/delete-user')
async def delete_user(id: int, db: Session = Depends(get_db)):
    new_delete = db.query(User).filter(User.id == id)\
        .delete(synchronize_session=False)
    db.commit()
    if new_delete:
        return "Success"
    else:
        return False


# 9 - Search
@app.post('/api/search-user')
async def search_user(req: SearchUser, db: Session = Depends(get_db)):
    res = db.query(User.id, User.name, User.admin)\
        .filter(User.name.like(f"%{req.text}%")).all()
    if res:
        return res
    else:
        return False


# 9 - Get
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
