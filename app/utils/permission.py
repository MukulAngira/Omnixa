from fastapi import Depends, HTTPException, status

from app.utils.deps import get_current_user
from app.models.permission import Permission
from app.models.rolepermission import RolePermission
from app.models.role import Role
from beanie import PydanticObjectId


def require_permission(permission_name: str):

    async def checker(current_user=Depends(get_current_user)):
        if current_user.roleId:
            try:
                role = await Role.find_one(Role.id == PydanticObjectId(current_user.roleId))
                if role and role.name.lower() == 'admin':
                    return current_user
            except:
                pass

        permission = await Permission.find_one(
            Permission.name == permission_name
        )

        if not permission:
            # Auto-create the permission if it doesn't exist to prevent 404
            permission = Permission(name=permission_name)
            await permission.insert()

        role_permission = await RolePermission.find_one(
            RolePermission.roleId == current_user.roleId,
            RolePermission.permissionId == str(permission.id)
        )
        
        if not role_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action."
            )

        return current_user

    return checker