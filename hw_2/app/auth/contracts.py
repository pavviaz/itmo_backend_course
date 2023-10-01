from pydantic import (
    BaseModel,
    model_validator,
    field_validator,
    ValidationInfo,
    EmailStr,
)

from app.settings import PASSWD_MIN_LEN, PASSWD_MAX_LEN


class Token(BaseModel):
    """It's better to send token via cookies or Bearer"""

    token: str


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

    @field_validator("password_1")
    @classmethod
    def check_pw(cls, v: str, info: ValidationInfo) -> str:
        if not v:
            raise ValueError(f"{info.field_name} is empty")

        if PASSWD_MIN_LEN > len(v):
            raise ValueError(f"{info.field_name} is too short")

        if PASSWD_MAX_LEN < len(v):
            raise ValueError(f"{info.field_name} is too long")

        return v

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserRegister":
        pw1 = self.password_1
        pw2 = self.password_2

        if pw1 != pw2:
            raise ValueError("Passwords do not match")

        return self
