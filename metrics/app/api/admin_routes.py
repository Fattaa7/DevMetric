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

