from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.auth import hash_password, verify_password
from fastapi import HTTPException, status

from app.models.metric import Metric


def create_user(db: Session, user_data: UserCreate):
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    hashed_password = hash_password(user_data.password)

    new_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_password, role=user_data.role.value)

    try:
        db.add(new_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    return UserResponse.model_validate(new_user)



def get_user_metric_or_404(db: Session, user: User, metric_id: int) -> Metric:
    metric = db.query(Metric).filter(Metric.user_id == user.id, Metric.id == metric_id).first()
    if not metric:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Metric not found")
    return metric
