from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.utils import schemas, dbConnection
from app.security import token
from app.repository import users

router = APIRouter(tags=['User-Authentication'])
get_db = dbConnection.get_db

@router.post('/register')
async def registration(request: schemas.CreateUser, db: Session = Depends(get_db)):
 return users.register(request, db)


@router.post('/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(dbConnection.get_db)):
    user= users.authenticate(db, request)
    
    if not users.is_active(user):
            raise HTTPException(status_code=400, detail="Inactive user")
        
    if not user.user_role:
            role = "USER"
    else:
        role = user.user_role.role.roleName
        print(role)
    access_token = token.create_access_token(data={"email": user.email, "role":role})
    return {
        "access_token": access_token, 
            "token_type": "bearer",
        "role": role
            }