from fastapi import Request, HTTPException, Depends, status
from jose import jwt, JWTError
from datetime import datetime

from users.dao import UsersDAO

from users.auth import SECRET_KEY, ALGORITHM

def get_token(request: Request):
    token = request.cookies.get("user_access_token")

    if not token:
        raise HTTPException(status_code=401)

    return token



async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
    except JWTError as e:
        raise e
        print("Token error")
        raise HTTPException(status_code=401)

    expire: str = payload.get("exp")

    if not expire or (int(expire) < datetime.utcnow().timestamp()):
        print("Token expired")
        raise HTTPException(status_code=401)


    user_id: int = payload.get("sub")
    if not user_id:
        print("User id not")
        raise HTTPException(status_code=401)

    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        print("User not")
        raise HTTPException(status_code=401)

    return user
