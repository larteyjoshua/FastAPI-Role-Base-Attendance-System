from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.security.hashing import Hash
from app.models import model 
from app.utils import schemas

def create(request: schemas.CreateUser, db: Session):
    user = db.query(model.User).filter(model.User.email == request.email).first()
    if user:
        raise HTTPException(status_code= 303,
                            detail =f"User with the email { request.email} already exist")
    else: 
        new_user = model.User(name =request.name,
                              email = request.email,
                              location = request.location,
                              gpsAddress = request.gpsAddress,
                              password = Hash.bcrypt(request.password)
                              )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

def register(request: schemas.CreateUser, db: Session):
    user = db.query(model.User).filter(model.User.email == request.email).first()
    if user:
        raise HTTPException(status_code= 303,
                            detail =f"User with the email { request.email} already exist")
    else: 
        new_user = model.User(name =request.name,
                              email = request.email,
                              location = request.location,
                              gpsAddress = request.gpsAddress,
                              isActive = False,
                              password = Hash.bcrypt(request.password)
                              )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


def show(id: int, db: Session):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not available")
    return user

# def showLoginUser(current_user, db: Session):
#     loginUser =db.query(model.User, model.Sensor).outerjoin(model.Sensor).filter(model.User.id == current_user.id).first()
#     if not loginUser:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"User with the id {id} is not available")
#     return loginUser
  

def get_all(db: Session):
    users = db.query(model.User).filter(model.User.user_role == None).all()
    return users

def get_all_admin(db: Session):
    admin = db.query(model.User).filter(model.User.user_role is not None).all()
    return admin

def destroy(id: int, db: Session):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")
    db.delete(user)
    db.commit()
    return user


def update(id: int, request: schemas.ShowUser, db: Session):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    user.name =request.name
    user.email = request.email
    user.location = request.location
    user.gpsAddress = request.gpsAddress
    user.isActive = request.isActive
    db.commit()
    db.refresh(user)
    return user


def suspend_or_Approve_user(id: int, request: schemas.SuspendOrApproveUser, db: Session):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} not found")

    user.isActive = request.isActive
    db.commit()
    db.refresh(user)
    return user

def is_active(user: schemas.ShowUser) -> bool:
        return user.isActive
    
def get_by_email(db: Session, request):
    user = db.query(model.User).filter(model.User.email ==request).first()
    return user

def authenticate( db: Session ,request):
        user = get_by_email(db, request.username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Invalid Credentials")
        elif not Hash.verify(user.password, request.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Incorrect password")
        return user

def showUser(db: Session, email: str ):
    user = db.query(model.User).filter(model.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {email} is not available")
    return user

def get_by_name(name: str, db: Session):
    user = db.query(model.User).filter(
        model.User.name ==name).first()
    return user


# def passwordRecover( email: str, db: Session, url:str):
#     user = db.query(model.User).filter(model.User.email == email).first()
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this email does not exist in the system.",
#         )
#     token = generate_password_recovery_token(email=user.email)

#     link = f"{url}?token={token}"
#     passwordRecoveryEmail.passwordRevovery(user.email, user.fullName, link)
#     return {"msg": "Password recovery email sent"}

# def passwordReset(token: str, new_password: str, db: Session):
#     email = verify_password_reset_token(token)
#     if not email:
#         raise HTTPException(status_code=400, detail="Invalid token")
#     user = db.query(model.User).filter(model.User.email == email).first()
#     if not user:
#         raise HTTPException(
#             status_code=404,
#             detail="The user with this username does not exist in the system.",
#         )
#     elif not is_active(user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     user.password = Hash.bcrypt(new_password)
#     db.add(user)
#     db.commit()
#     return {"msg": "Password updated successfully"}
   