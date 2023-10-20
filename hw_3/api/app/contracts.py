from pydantic import (
    BaseModel,
    EmailStr,
)


class UserLogin(BaseModel):
    """Contract for user login"""

    username: str
    password: str


class UserRegister(BaseModel):
    """Contract for user registration"""

    username: str
    password_1: str
    password_2: str
    email: EmailStr


class UserRequest(BaseModel):
    """Contract for user request,
    It's better to send token via cookies or Bearer
    """

    text: str
    token: str
