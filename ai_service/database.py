from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://nextjs_user:Agepi85183@localhost:3306/ai_db"
engine_ai = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocalAI = sessionmaker(autocommit=False, autoflush=False, bind=engine_ai)
BaseAI = declarative_base()


# Prisma Database
SQLALCHEMY_PRISMA_DATABASE_URL = "mysql+pymysql://nextjs_user:Agepi85183@localhost:3306/nextjs_auth_db"
engine_prisma = create_engine(SQLALCHEMY_PRISMA_DATABASE_URL)
SessionLocalPrisma = sessionmaker(autocommit=False, autoflush=False, bind=engine_prisma)
BasePrisma = declarative_base()


def init_ai_database():
    from .models import Base as BaseAI
    BaseAI.metadata.create_all(bind=engine_ai)