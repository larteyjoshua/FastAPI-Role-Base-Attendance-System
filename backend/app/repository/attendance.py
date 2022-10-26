from argparse import Action
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks
from app.models import model
from app.utils import schemas
from datetime import datetime


def signIn(request: schemas.CreateAttendance, db: Session):
    today = datetime.today().strftime('%Y-%m-%d')
    attendance = db.query(model.Attendance).filter(model.Attendance.userId == request.userId and
     (datetime.datetime(model.Attendance.actionTime)).strftime('%Y-%m-%d') < today).first()
    if attendance:
        raise HTTPException(status_code= 303,
                            detail =f"Already SignIn")
    else: 
        new_sign_in = model.Attendance(action=request.action, userId = request.userId)
        db.add(new_sign_in)
        db.commit()
        db.refresh(new_sign_in)
        return new_sign_in

def signOut(request: schemas.CreateAttendance, db: Session):
    today = datetime.today().strftime('%Y-%m-%d')
    attendance = db.query(model.Attendance).filter(model.Attendance.userId == request.userId and
     (datetime.datetime(model.Attendance.actionTime)).strftime('%Y-%m-%d') is today).first()
    if not attendance:
        raise HTTPException(status_code= 303,
                            detail =f"You haven't Sign In today, Sign in First")
    else: 
        new_sign_out = model.Attendance(action = request.action, userId = request.userId)
        db.add(new_sign_out)
        db.commit()
        db.refresh(new_sign_out)
        return new_sign_out

def get_all(db: Session):
    attendances = db.query(model.Attendance).all()
    return attendances

def destroy(id: int, db: Session):
    attendance = db.query(model.Attendance).filter(model.Attendance.id == id).first()
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Attendance with id {id} not found")
    db.delete(attendance)
    db.commit()
    return attendance

def show(id: int, db: Session):
    attendance = db.query(model.Attendance).filter(model.Attendance.userId ==id ).all()
    if not attendance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Role with the id {id} is not available")
    return attendance

