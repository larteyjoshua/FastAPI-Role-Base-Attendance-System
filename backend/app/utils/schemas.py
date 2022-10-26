from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class CreateUser(BaseModel):
    name: str
    email: str
    location: str
    gpsAddress: str
    password: str
    isActive: bool = None

    class Config():
        orm_mode = True

class ShowUser(BaseModel):
    id: int
    name: str
    email: str
    location: str
    gpsAddress: str
    isActive: bool
    dateAdded: datetime
    
    class Config():
        orm_mode = True

class CreateAttendance(BaseModel):
    userId: int
    action: str
    
    class Config():
        orm_mode = True

class ShowAttendance(BaseModel):
    id: int
    userId: int
    action: str
    actionTime: datetime
    
    class Config():
        orm_mode = True

class CreateRole(BaseModel):
    roleName: str
    description: str
    class Config():
        orm_mode = True 
        
class ShowRole(BaseModel):
    id: int
    roleName: str
    description: str
    dateAdded: datetime

    class Config():
        orm_mode = True

class UpdateRole(BaseModel):
    id: int
    description: str
    
    class Config():
        orm_mode = True

class UserRoleBase(BaseModel):
    userId: Optional[int] = None
    roleId: Optional[int] = None

    class Config():
        orm_mode = True

class SuspendOrApproveUser(BaseModel):
    id: int
    isActive: bool
   
    