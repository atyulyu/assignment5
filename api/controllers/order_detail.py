from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import models, schemas


def create(db: Session, order_detail: schemas.OrderDetailCreate):
    db_order = db.query(models.Order).filter(models.Order.id == order_detail.order_id).first()
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == order_detail.sandwich_id).first()

    if not db_order or not db_sandwich:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order or Sandwich not found"
        )

    db_order_detail = models.OrderDetail(**order_detail.dict())
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail


def read_all(db: Session):
    return db.query(models.OrderDetail).all()


def read_one(db: Session, order_detail_id: int):
    order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id).first()
    if not order_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"OrderDetail with id {order_detail_id} not found"
        )
    return order_detail


def update(db: Session, order_detail_id: int, order_detail: schemas.OrderDetailUpdate):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id)
    if not db_order_detail.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"OrderDetail with id {order_detail_id} not found"
        )
    update_data = order_detail.model_dump(exclude_unset=True)
    db_order_detail.update(update_data, synchronize_session=False)
    db.commit()
    return db_order_detail.first()


def delete(db: Session, order_detail_id: int):
    db_order_detail = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_detail_id)
    if not db_order_detail.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"OrderDetail with id {order_detail_id} not found"
        )
    db_order_detail.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
