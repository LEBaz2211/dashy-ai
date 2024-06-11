from sqlalchemy.orm import Session
from fastapi import HTTPException
from ai_service.db.common_models import Dashboard
from ai_service.db.schemas import DashboardCreate

def create_dashboard(db: Session, dashboard: DashboardCreate):
    db_dashboard = Dashboard(**dashboard.dict())
    db.add(db_dashboard)
    db.commit()
    db.refresh(db_dashboard)
    return db_dashboard

def get_dashboard(db: Session, dashboard_id: int):
    return db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()

def delete_dashboard(db: Session, dashboard_id: int):
    db_dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
    db.delete(db_dashboard)
    db.commit()

def update_dashboard(db: Session, dashboard_id: int, dashboard: DashboardCreate):
    db_dashboard = db.query(Dashboard).filter(Dashboard.id == dashboard_id).first()
    if db_dashboard:
        for key, value in dashboard.dict().items():
            setattr(db_dashboard, key, value)
        db.commit()
        db.refresh(db_dashboard)
    return db_dashboard
