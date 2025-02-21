from pydantic import BaseModel, UUID4, EmailStr


class UserSchema(BaseModel):
    email: EmailStr
    password: str


class GetUserSchema(UserSchema):
    id: UUID4
