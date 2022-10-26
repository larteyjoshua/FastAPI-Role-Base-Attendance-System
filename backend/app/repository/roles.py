from sqlalchemy.orm import Session
from fastapi import HTTPException, status, BackgroundTasks
from app.models import model
from app.utils import schemas


def create(request: schemas.CreateRole, db: Session):
    role = db.query(model.Role).filter(model.Role.roleName == request.roleName).first()
    if role:
        raise HTTPException(status_code= 303,
                            detail =f"Role with the name { request.roleName} already exist")
    else: 
        new_role = model.Role(roleName=request.roleName, description = request.description)
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return new_role


def show(id: int, db: Session):
    role = db.query(model.Role).filter(model.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Role with the id {id} is not available")
    return role

def get_all(db: Session):
    roles = db.query(model.Role).all()
    return roles

def destroy(id: int, db: Session):
    role = db.query(model.Role).filter(model.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    role.delete(synchronize_session=False)
    db.commit()
    return{"success": f"Role with the name {role.name} Deleted"}


def update(id: int, request: schemas.UpdateRole, db: Session):
    role = db.query(model.Role).filter(model.Role.id == id).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Role with id {id} not found")
     
    role.description = request.description
    db.commit()
    db.refresh(role)
    return role

def role_by_name(roleName: str, db: Session):
    role = db.query(model.Role).filter(model.Role.roleName == roleName).first()
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Role with the id {roleName} is not available")
    return role