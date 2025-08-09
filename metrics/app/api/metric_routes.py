from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.user import User
from app.models.metric import Metric
from app.services.auth import get_current_user
from app.schemas.metric_schema import MetricCreate, MetricResponse
from app.crud.user_crud import get_user_metric_or_404
from typing import Optional, List
from app.models.enums.metric_type import MetricType
from app.models.enums.user_role import UserRole
from fastapi import Query

router = APIRouter(prefix="/metric", tags=["Metric"])

@router.post("/", response_model=MetricResponse, status_code=status.HTTP_201_CREATED)
async def create_metric(metric: MetricCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_metric = Metric(type=metric.type.value, description=metric.description, user_id=user.id)
    
    db.add(new_metric)
    db.commit()
    return new_metric



@router.get("/search", response_model=List[MetricResponse])
async def get_metrics_query(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
    metric_type: Optional[str] = Query(None),
    from_date: Optional[datetime] = Query(None),
    to_date: Optional[datetime] = Query(None),
    sort_by: str = Query("timestamp"),
    order: str = Query("desc")
):
    query = db.query(Metric)

    # Restrict non-admins
    if user.role != UserRole.ADMIN:
        query = query.filter(Metric.user_id == user.id)

    # Apply filters
    if metric_type:
        query = query.filter(Metric.type == metric_type)

    if from_date:
        query = query.filter(Metric.timestamp >= from_date)

    if to_date:
        query = query.filter(Metric.timestamp <= to_date)

    # Sorting
    sort_column = getattr(Metric, sort_by, None)
    if sort_column:
        if order.lower() == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)

    # Pagination
    metrics = query.offset(skip).limit(limit).all()

    return metrics


@router.get("/", response_model=List[MetricResponse], status_code=status.HTTP_200_OK)
async def get_all_metrics(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    metric_list = db.query(Metric).filter(Metric.user_id == user.id).all()
    return metric_list


@router.get("/{metric_id}", response_model=MetricResponse, status_code=status.HTTP_200_OK)
async def get_metric(metric_id: int = Path(gt=0), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    metric = get_user_metric_or_404(db, user, metric_id)
    return metric

@router.put("/{metric_id}", response_model=MetricResponse, status_code=status.HTTP_202_ACCEPTED)
async def change_metric(metric_req: MetricCreate, metric_id: int = Path(gt=0), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    metric = get_user_metric_or_404(db, user, metric_id)
    metric.description = metric_req.description
    metric.type = metric_req.type.value

    db.commit()
    db.refresh(metric)
    return metric


@router.delete("/{metric_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_metric(metric_id: int = Path(gt=0), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    metric = get_user_metric_or_404(db, user, metric_id)
    db.delete(metric)
    db.commit()
    return None




