from sqlalchemy import text

from backend.database import engine

from backend.auth.security import verify_password
from backend.auth.jwt_handler import create_access_token

def login_user(username: str, password: str):

    with engine.connect() as connection:

        result = connection.execute(
            text("""
                SELECT
                    username,
                    password_hash,
                    role,
                    is_active
                FROM users
                WHERE username = :username
            """),
            {"username": username}
        ).fetchone()

        if result is None:
            return None

        if not result.is_active:
            return None

        if not verify_password(password, result.password_hash):
            return None
        
        print("Username:", username)
        print("DB Username:", result.username)
        print("Password Check:", verify_password(password, result.password_hash))
        
        token = create_access_token(
            {
                "username": result.username,
                "role": result.role
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "username": result.username,
            "role": result.role
        }
    
