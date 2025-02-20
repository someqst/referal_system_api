from pydantic import BaseModel, UUID4


class UserSchema(BaseModel):
    email: str
    password: str


class GetUserSchema(UserSchema):
    id: UUID4
