from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.db.database import get_db_prisma
from ai_service.db.schemas import Dashboard, DashboardCreate
from ai_service.db.crud import (
    create_dashboard as crud_create_dashboard,
    get_dashboard as crud_get_dashboard,
    delete_dashboard as crud_delete_dashboard,
    update_dashboard as crud_update_dashboard,
)

router = APIRouter()

@router.post("/dashboards/", response_model=Dashboard)
def create_dashboard_route(dashboard: DashboardCreate, db: Session = Depends(get_db_prisma)):
    return crud_create_dashboard(db, dashboard)

@router.get("/dashboards/{dashboard_id}", response_model=Dashboard)
def get_dashboard_route(dashboard_id: int, db: Session = Depends(get_db_prisma)):
    db_dashboard = crud_get_dashboard(db, dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return db_dashboard

@router.delete("/dashboards/{dashboard_id}", response_model=Dashboard)
def delete_dashboard_route(dashboard_id: int, db: Session = Depends(get_db_prisma)):
    db_dashboard = crud_get_dashboard(db, dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    crud_delete_dashboard(db, dashboard_id)
    return db_dashboard

@router.put("/dashboards/{dashboard_id}", response_model=Dashboard)
def update_dashboard_route(dashboard_id: int, dashboard: DashboardCreate, db: Session = Depends(get_db_prisma)):
    db_dashboard = crud_get_dashboard(db, dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return crud_update_dashboard(db, dashboard_id, dashboard)
