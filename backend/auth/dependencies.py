from fastapi import Depends, HTTPException

from fastapi.security import OAuth2PasswordBearer

from backend.auth.jwt_handler import verify_access_token


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


def get_current_user(

    token: str = Depends(oauth2_scheme)

):

    payload = verify_access_token(token)

    if payload is None:

        raise HTTPException(

            status_code=401,

            detail="Invalid or expired token"

        )

    return payload

# =====================================================
# ROLE CHECK
# =====================================================

def require_roles(*allowed_roles):

    def role_checker(
        current_user: dict = Depends(get_current_user)
    ):

        if current_user["role"] not in allowed_roles:

            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this resource."
            )

        return current_user

    return role_checker