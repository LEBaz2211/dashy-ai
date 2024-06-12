from sqlalchemy import Column, LargeBinary, String, Integer, Boolean, DateTime, Enum, ForeignKey, Table, func
from sqlalchemy.orm import relationship
from ai_service.db.database import BasePrisma as Base
import enum

class TaskTypeEnum(str, enum.Enum):
    DEFAULT = 'DEFAULT'
    EMAIL = 'EMAIL'
    COURSE = 'COURSE'

# Many-to-Many relationship between Task and Tag
tag_to_task = Table(
    '_tagtotask', Base.metadata,
    Column('B', Integer, ForeignKey('task.id')),
    Column('A', Integer, ForeignKey('tag.id'))
)

class User(Base):
    __tablename__ = 'user'
    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=True)
    image = Column(LargeBinary, nullable=True)
    emailVerified = Column(DateTime, nullable=True)
    dashboards = relationship("Dashboard", back_populates="user")
    accounts = relationship("Account", back_populates="user")
    sessions = relationship("Session", back_populates="user")

class Dashboard(Base):
    __tablename__ = 'dashboard'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    userId = Column(String(255), ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="dashboards")
    taskLists = relationship("TaskList", back_populates="dashboard")

class TaskList(Base):
    __tablename__ = 'tasklist'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    dashboardId = Column(Integer, ForeignKey('dashboard.id'), nullable=False)
    dashboard = relationship("Dashboard", back_populates="taskLists")
    tasks = relationship("Task", back_populates="taskList")

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    completed = Column(Boolean, default=False)
    taskListId = Column(Integer, ForeignKey('tasklist.id'), nullable=False)
    taskList = relationship("TaskList", back_populates="tasks")
    dueDate = Column(DateTime, nullable=True)
    reminder = Column(DateTime, nullable=True)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
    tags = relationship("Tag", secondary=tag_to_task, back_populates="tasks")
    subtasks = relationship("Subtask", back_populates="task")
    notes = Column(String(255), nullable=True)
    type = Column(Enum(TaskTypeEnum), default=TaskTypeEnum.DEFAULT)
    recipient = Column(String(255), nullable=True)
    emailBody = Column(String(255), nullable=True)
    courseSummary = Column(String(255), nullable=True)

class Subtask(Base):
    __tablename__ = 'subtask'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    completed = Column(Boolean, default=False)
    taskId = Column(Integer, ForeignKey('task.id'), nullable=False)
    task = relationship("Task", back_populates="subtasks")

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    tasks = relationship("Task", secondary=tag_to_task, back_populates="tags")

class Account(Base):
    __tablename__ = 'account'
    id = Column(String(255), primary_key=True)
    userId = Column(String(255), ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="accounts")
    type = Column(String(255), nullable=False)
    provider = Column(String(255), nullable=False)
    providerAccountId = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    access_token = Column(String(255), nullable=True)
    expires_at = Column(Integer, nullable=True)
    token_type = Column(String(255), nullable=True)
    scope = Column(String(255), nullable=True)
    id_token = Column(String(255), nullable=True)
    session_state = Column(String(255), nullable=True)

class Session(Base):
    __tablename__ = 'session'
    id = Column(String(255), primary_key=True)
    sessionToken = Column(String(255), unique=True, nullable=False)
    userId = Column(String(255), ForeignKey('user.id'), nullable=False)
    user = relationship("User", back_populates="sessions")
    expires = Column(DateTime, nullable=False)

class VerificationToken(Base):
    __tablename__ = 'verificationtoken'
    identifier = Column(String(255), primary_key=True)
    token = Column(String(255), unique=True, nullable=False)
    expires = Column(DateTime, nullable=False)
