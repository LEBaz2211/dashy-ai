from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ai_service.db import schemas, prisma_crud
from ai_service.db.database import get_db_prisma

router = APIRouter()

@router.post("/dashboards/", response_model=schemas.Dashboard)
def create_dashboard(dashboard: schemas.DashboardCreate, db: Session = Depends(get_db_prisma)):
    return prisma_crud.create_dashboard(db, dashboard)

@router.get("/dashboards/{dashboard_id}", response_model=schemas.Dashboard)
def get_dashboard(dashboard_id: int, db: Session = Depends(get_db_prisma)):
    db_dashboard = prisma_crud.get_dashboard(db, dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return db_dashboard

@router.delete("/dashboards/{dashboard_id}", response_model=schemas.Dashboard)
def delete_dashboard(dashboard_id: int, db: Session = Depends(get_db_prisma)):
    db_dashboard = prisma_crud.get_dashboard(db, dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    prisma_crud.delete_dashboard(db, dashboard_id)
    return db_dashboard

@router.put("/dashboards/{dashboard_id}", response_model=schemas.Dashboard)
def update_dashboard(dashboard_id: int, dashboard: schemas.DashboardCreate, db: Session = Depends(get_db_prisma)):
    db_dashboard = prisma_crud.get_dashboard(db, dashboard_id)
    if db_dashboard is None:
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return prisma_crud.update_dashboard(db, dashboard_id, dashboard)
