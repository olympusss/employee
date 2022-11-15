from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from connection import Base

class User(Base):
    __tablename__   =   "users"
    id              =   Column(Integer, primary_key=True, index=True)
    name            =   Column(String)
    admin           =   Column(Boolean)
    password        =   Column(String)
    create_At       =   Column(DateTime(timezone=False), default=datetime.now)
    update_At       =   Column(DateTime(timezone=False), default=datetime.now)

class Employee(Base):
    __tablename__   =   "employee"
    id              =   Column(Integer, primary_key=True, index=True) 
    name            =   Column(String)
    surname         =   Column(String)
    job_title       =   Column(String)
    department_id     =   Column(Integer, ForeignKey("department.id"))
    create_At       =   Column(DateTime(timezone=False), default=datetime.now)
    update_At       =   Column(DateTime(timezone=False), default=datetime.now)
    employee_department =   relationship("Department", back_populates="department_employee")


class Company(Base):
    __tablename__   =   "company"
    id              =   Column(Integer, primary_key=True, index=True) 
    name            =   Column(String)
    create_At       =   Column(DateTime(timezone=False), default=datetime.now)
    update_At       =   Column(DateTime(timezone=False), default=datetime.now)
    company_department  = relationship("Department", back_populates="department_company")

class Department(Base):
    __tablename__   =   "department" 
    id              =   Column(Integer, primary_key=True, index=True)
    name            =   Column(String)
    company_id      =   Column(Integer, ForeignKey("company.id"))
    create_At       =   Column(DateTime(timezone=False), default=datetime.now)
    update_At       =   Column(DateTime(timezone=False), default=datetime.now)
    department_employee = relationship("Employee", back_populates="employee_department")
    department_company  = relationship("Company", back_populates="company_department")
