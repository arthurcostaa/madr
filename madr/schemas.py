from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=256)
    email: EmailStr
    password: str = Field(min_length=5, max_length=256)


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class NovelistSchema(BaseModel):
    name: str = Field(min_length=3, max_length=256)


class NovelistPublic(NovelistSchema):
    id: int
