from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.user import User
from app.models.metric import Metric
from app.services.auth import get_current_user
from app.schemas.metric_schema import MetricCreate, MetricResponse
from app.models.enums.user_role import UserRole
from app.crud.user_crud import get_user_metric_or_404
from app.schemas.user_schema import UserResponse


router = APIRouter(prefix="/admin", tags=["Admin"])



@router.get("/", response_model=List[MetricResponse], status_code=status.HTTP_200_OK)
async def get_all_metrics(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    metric_list = db.query(Metric).all()
    return metric_list


@router.delete("/{metric_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_metric(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    metric = db.query(Metric).all()
    for m in metric:
        db.delete(m)
    db.commit()
    return None

@router.delete("/user/all", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_users(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    users = db.query(User).all()
    for u in users:
        db.delete(u)
    db.commit()
    return None


@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    user_to_delete = db.query(User).filter(User.id == id).first()
    if not user_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user_to_delete)
    db.commit()    
    return None


@router.get("/user/all", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    users = db.query(User).all()
    return users


@router.get("/user/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user_by_id(id: int = Path(..., title="The ID of the user to retrieve"), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    user_data = db.query(User).filter(User.id == id).first()
    if not user_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return UserResponse.model_validate(user_data)
