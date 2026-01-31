from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt import PyJWTError
from pydantic import BaseModel
from typing import Optional
from settings import settings
security = HTTPBearer()

class TokenData(BaseModel):
    user_id: str

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to extract and verify the current user from JWT token.
    Returns the user_id if valid, raises HTTP 401 if invalid.
    Updated to work with Better Auth tokens which may have different field names.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the token using the BETTER_AUTH_SECRET
        payload = jwt.decode(
            credentials.credentials,
            settings.better_auth_secret,
            algorithms=["HS256"]
        )

        print(f"Decoded JWT payload: {payload}")  # Debug logging

        # Better Auth may use different field names for user ID
        # Try multiple possible field names
        user_id: str = payload.get("user_id") or payload.get("sub") or payload.get("id") or payload.get("userId")

        if user_id is None:
            print("No user_id found in token payload")  # Debug logging
            raise credentials_exception

        token_data = TokenData(user_id=user_id)
    except PyJWTError as e:
        print(f"JWT decode error: {str(e)}")  # Debug logging
        raise credentials_exception

    return token_data.user_id

def verify_user_id_match(token_user_id: str, path_user_id: str) -> None:
    """
    Verify that the user_id in the JWT token matches the user_id in the path parameter.
    Raises HTTP 403 if they don't match.
    """
    if token_user_id != path_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match user ID in path"
        )