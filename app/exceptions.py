from fastapi import  HTTPException, status

class Fobridden(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "You are not allowed to do this action"
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

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


class NotFound(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "We cand found, what you fetch"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


