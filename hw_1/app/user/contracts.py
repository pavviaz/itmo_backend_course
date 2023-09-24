from pydantic import BaseModel


class UserLogin(BaseModel):
    """Contract for user login"""

    name: str
    password: str


class UserRegister(BaseModel):
    """Contract for user registration"""

    name: str
    password: str
    email: str
    nickname: str | None = None
