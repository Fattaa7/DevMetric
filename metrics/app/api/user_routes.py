from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserResponse
from app.dependencies import get_db
from app.crud.user_crud import create_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)
