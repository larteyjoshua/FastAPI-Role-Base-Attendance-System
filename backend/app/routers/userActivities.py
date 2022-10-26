from fastapi import APIRouter, Depends, Security, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.utils import schemas, dbConnection
from app.security import token
from app.repository import users, roles, attendance, userRoles
from app.utils.userRolesObjects import Role
from app.utils.InitialUser import User
from app.security import oauth2
from typing import List

router = APIRouter()
get_db = dbConnection.get_db

@router.get('/user/profile', response_model=schemas.ShowUser, tags = ['Admin', 'User'])
async def get_user(db: Session = Depends(get_db), current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["roleName"], Role.USER["roleName"]],
    )):
    return users.show(current_user.id, db)

@router.post('/user/add', response_model=schemas.ShowUser, tags = ['Admin',])
async def create_user(request:schemas.CreateUser, db: Session = Depends(get_db), current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["roleName"]],
    )):
    return users.create(request, db)

@router.delete('/user/{id}',  response_model=schemas.ShowUser, tags = ['Admin'])
async def destroy(id: int, db: Session = Depends(get_db),  current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["roleName"]],
    )):
    return users.destroy(id, db)

@router.put('/user/suspend',  response_model=schemas.ShowUser, tags = ['Admin'])
async def suspend(request:schemas.SuspendOrApproveUser, db: Session = Depends(get_db),  current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["roleName"]],
    )):
    return users.suspend_or_Approve_user(request.id, request, db)

@router.put('/user/approve',  response_model=schemas.ShowUser, tags = ['Admin'])
async def approve(request:schemas.SuspendOrApproveUser, db: Session = Depends(get_db),  current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["roleName"]],
    )):
    return users.suspend_or_Approve_user(request.id, request, db)

@router.get('/user/attendance/all', response_model=List[schemas.ShowAttendance], tags = ['Admin'])
async def get_all_attendance(db: Session = Depends(get_db),  current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["roleName"]],
    )):
    return attendance.get_all(db)

@router.put('/user/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowUser, tags = ['Admin',])
async def update(id: int, request: schemas.CreateUser, db: Session = Depends(get_db), current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[ Role.SUPER_ADMIN["roleName"]],
    )):
    return users.update(id, request, db)

@router.post('/user/register', response_model=schemas.ShowUser, tags = ['User',])
async def create_register(request:schemas.CreateUser, db: Session = Depends(get_db), current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[Role.USER["roleName"]],
    )):
    return users.register(request, db)

@router.post('/user/attendance/signIn', response_model=schemas.ShowAttendance, tags = ['Admin','User',])
async def sign_in(request:schemas.CreateAttendance, db: Session = Depends(get_db), current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["roleName"], Role.USER["roleName"]],
    )):
    return attendance.signIn(request, db)

@router.post('/user/attendance/signOut', response_model=schemas.ShowAttendance, tags = ['Admin','User',])
async def sign_in(request:schemas.CreateAttendance, db: Session = Depends(get_db), current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["roleName"], Role.USER["roleName"]],
    )):
    return attendance.signOut(request, db)

@router.get('/user/attendance/AllByUser', response_model=List[schemas.ShowAttendance], tags = ['Admin','User',])
async def user_attendance(db: Session = Depends(get_db), current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["roleName"], Role.USER["roleName"]],
    )):
    return attendance.show(current_user.id, db)

@router.delete('/user/attendance/{id}', response_model=schemas.ShowAttendance, tags = ['Admin'])
async def destroy(id: int, db: Session = Depends(get_db),  current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["roleName"]],
    )):
    return attendance.destroy(id, db)

@router.get('/user/',  response_model=List[schemas.ShowUser], tags = ['Admin'])
async def all(db: Session = Depends(get_db), current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[ Role.SUPER_ADMIN["roleName"]],
    )):
    return users.get_all(db)

@router.get('/admin/',  response_model=List[schemas.ShowUser], tags = ['Admin'])
async def all(db: Session = Depends(get_db), current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[ Role.SUPER_ADMIN["roleName"]],
    )):
    return users.get_all_admin(db)

@router.put('/role/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UpdateRole, tags = ['Admin'])
async def update(id: int, request: schemas.UpdateRole, db: Session = Depends(get_db), current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[ Role.SUPER_ADMIN["roleName"]],
    )):
    return roles.update(id, request, db)

@router.get('/role/',  response_model=List[schemas.ShowRole], tags = ['Admin'])
async def all(db: Session = Depends(get_db), current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[ Role.SUPER_ADMIN["roleName"]],
    )):
    return roles.get_all(db)

@router.post('/userRole/',  response_model=schemas.UserRoleBase, tags = ['Admin'])
async def assign_user_role(request: schemas.UserRoleBase, db: Session = Depends(get_db), current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["roleName"]],
    )):
    return userRoles.create(request, db)

@router.get('/userRole/', response_model=List[schemas.UpdateRole],  tags = ['Admin'] )
async def all(db: Session = Depends(get_db), current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["roleName"]],
    )):
    return userRoles.get_all(db)


@router.put('/userRole/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.UserRoleBase, tags = ['Admin'])
async def update(id: int, request: schemas.UserRoleBase, db: Session = Depends(get_db), current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["roleName"]],
    )):
    return userRoles.update(id, request, db)

@router.delete('/userRole/{id}', response_model=schemas.UserRoleBase,  tags = ['Admin'])
async def destroy(id: int, db: Session = Depends(get_db), current_user: schemas.ShowUser = Security(
        oauth2.get_current_active_user,
        scopes=[Role.SUPER_ADMIN["roleName"]],
    )):
    return userRoles.destroy(id, db)


