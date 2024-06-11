from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.db import prisma_crud
from ai_service.db.database import get_db_prisma
from ai_service.db.schemas import Dashboard, DashboardCreate

router = APIRouter()

@router.post("/dashboards/", response_model=Dashboard)
def create_dashboard(dashboard: DashboardCreate, db: Session = Depends(get_db_prisma)):
    return prisma_crud.create_dashboard(db, dashboard)

@router.get("/dashboards/{dashboard_id}", response_model=Dashboard)
def get_dashboard(dashboard_id: int, db: Session = Depends(get_db_prisma)):
    db_dashboard = prisma_crud.get_dashboard(db, dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return db_dashboard

@router.delete("/dashboards/{dashboard_id}", response_model=Dashboard)
def delete_dashboard(dashboard_id: int, db: Session = Depends(get_db_prisma)):
    db_dashboard = prisma_crud.get_dashboard(db, dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    prisma_crud.delete_dashboard(db, dashboard_id)
    return db_dashboard

@router.put("/dashboards/{dashboard_id}", response_model=Dashboard)
def update_dashboard(dashboard_id: int, dashboard: DashboardCreate, db: Session = Depends(get_db_prisma)):
    db_dashboard = prisma_crud.get_dashboard(db, dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return prisma_crud.update_dashboard(db, dashboard_id, dashboard)
