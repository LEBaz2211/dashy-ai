import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
SQLALCHEMY_PRISMA_DATABASE_URL = os.getenv("SQLALCHEMY_PRISMA_DATABASE_URL")

engine_ai = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocalAI = sessionmaker(autocommit=False, autoflush=False, bind=engine_ai)
BaseAI = declarative_base()

engine_prisma = create_engine(SQLALCHEMY_PRISMA_DATABASE_URL)
SessionLocalPrisma = sessionmaker(autocommit=False, autoflush=False, bind=engine_prisma)
BasePrisma = declarative_base()

def init_ai_database():
    from .models import BaseAI
    BaseAI.metadata.create_all(bind=engine_ai)

def get_db_ai():
    db = SessionLocalAI()
    try:
        yield db
    finally:
        db.close()

def get_db_prisma():
    db = SessionLocalPrisma()
    try:
        yield db
    finally:
        db.close()
