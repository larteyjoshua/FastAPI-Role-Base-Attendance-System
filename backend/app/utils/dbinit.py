from sqlalchemy.orm import Session
from app.utils import schemas
from app.repository import roles, users, userRoles
from app.utils.userRolesObjects import Role
from app.utils.InitialUser import User
import logging


def databaseInit(db: Session):
    logging.info("Initializing Database with Roles and Super Admin")
 # Create Role If They Don't Exist
    user_role_in = schemas.CreateRole(
        roleName=Role.USER["roleName"], description=Role.USER["description"])
    roles.create(user_role_in, db)

    super_admin_role = schemas.CreateRole(
        roleName=Role.SUPER_ADMIN["roleName"], description=Role.SUPER_ADMIN["description"])
    roles.create(super_admin_role, db)

    # Creating SuperAdmin
    super_admin_ = schemas.CreateUser(
        name=User.SUPER_ADMIN["name"],
        email=User.SUPER_ADMIN["email"],
        location=User.SUPER_ADMIN["location"],
        password=User.SUPER_ADMIN["password"],
        gpsAddress=User.SUPER_ADMIN["gpsAddress"])
    users.create(super_admin_, db)

# # Assign super_admin role to user
    role = roles.role_by_name(Role.SUPER_ADMIN["roleName"], db)
    user = users.get_by_name(User.SUPER_ADMIN["name"], db)

    super_admin_role = schemas.UserRoleBase(userId=user.id, roleId=role.id)
    userRoles.create(super_admin_role, db)

    logging.info("Database init Completed")
    return {"success": "Database Initialization Completed"}
