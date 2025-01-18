from fastapi import  HTTPException, status

class UserAlreadyExists(HTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class IncorrectEmailOrPassword(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED,
    detail = "Incorrect email or password"
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


