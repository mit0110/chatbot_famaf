from fastapi import Depends, HTTPException, status
from app.auth import fastapi_users

optional_current_user = fastapi_users.current_user(active=True, optional=True)

async def get_user_or_redirect(user=Depends(optional_current_user)):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            headers={"Location": "/login"}
        )
    return user