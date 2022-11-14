from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from connection import Base, engine, get_db
from models import User
from schemas import UserSchema

app = FastAPI()


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
