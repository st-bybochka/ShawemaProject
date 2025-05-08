from pydantic import BaseModel, EmailStr, field_validator

from app.validators import PasswordValidator


class UserLoginSchema(BaseModel):
    email: EmailStr
    hashed_password: str

    @field_validator("hashed_password")
    def validate_password(cls, value: str) -> str:
        return PasswordValidator.validate_password(value)

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str

    class Config:
        from_attributes = True

