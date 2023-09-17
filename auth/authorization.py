from fastapi import HTTPException
import logging

from .exceptions import PermissionDenied
from .models import User


logger = logging.getLogger('auth')


class Authorization:

    # class attributes are Permission names
    Staff = "Staff"
    Admin = "Admin"
    SpiderLaunch = "SpiderLaunch"
    DontHave = "DontHave"

    async def has_permissions(self, user:User, *requred_permissions: str) -> bool:
        """Function checks to make sure the user has every permission 
        required to access the resource. Raises and HTTPException and logs
        a PermissionDenied error with the user's UUID.
        """
        user_perms = await user.permissions.all()
        permission_names = {perm.perm for perm in user_perms}

        if not all(perm in permission_names for perm in requred_permissions):
            logger.error(repr(PermissionDenied(user.access_id)))
            raise HTTPException(status_code=403, detail="Forbidden")
        return