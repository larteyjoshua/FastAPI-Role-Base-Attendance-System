from sqlalchemy import Column, Integer, String, ForeignKey,DateTime, Boolean, Text
from app.utils.dbConnection import Base

from sqlalchemy.orm import relationship

from datetime import datetime


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key =True, index = True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    location = Column(String,  nullable=True)
    gpsAddress = Column(String,  nullable=True)
    password = Column(String)
    dateAdded = Column(DateTime, default=datetime.now)
    isActive = Column(Boolean(), default=True)

    user_role = relationship("UserRole", back_populates="user", uselist=False)
    attendant = relationship("Attendance", back_populates="action_by", uselist=False)

class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key = True, index = True)
    userId = Column(Integer,ForeignKey("users.id"))
    action = Column(String,  nullable=False)
    actionTime = Column(DateTime, default=datetime.now)

    action_by =relationship("User", back_populates="attendant", uselist=False)
    


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key =True, index = True)
    roleName = Column(String)
    description = Column(Text)
    dateAdded =  Column(DateTime, default=datetime.now, onupdate=datetime.now)

class UserRole(Base):
    __tablename__ = "userRoles" 
    userId = Column(Integer,ForeignKey("users.id"), primary_key=True, nullable=False, index = True)
    roleId = Column(Integer, ForeignKey("roles.id"), primary_key=True,nullable=False, index =  True)
    role = relationship("Role")
    user = relationship("User", back_populates="user_role", uselist=False)
