from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.auth import router as auth_router
from .routes.auto_tag import router as auto_tag_router
from .routes.feedback import router as feedback_router
from .routes.conversation import router as conversation_router
from .routes.auto_subtask import router as auto_subtask_router
from .routes.aitask import router as aitask_router
from .routes.user import router as user_router
from .routes.dashboard import router as dashboard_router
from .routes.tasklist import router as tasklist_router
from .routes.tag import router as tag_router
from .routes.subtask import router as subtask_router
from .routes.task import router as task_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(auto_tag_router)
app.include_router(feedback_router)
app.include_router(conversation_router)
app.include_router(auto_subtask_router)
app.include_router(aitask_router)
app.include_router(user_router)
app.include_router(dashboard_router)
app.include_router(tasklist_router)
app.include_router(tag_router)
app.include_router(subtask_router)
app.include_router(task_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}
