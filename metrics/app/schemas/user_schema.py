from pydantic import BaseModel, EmailStr
from app.models.enums.user_role import UserRole

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: UserRole


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole

    model_config = {
        "from_attributes": True
    }
