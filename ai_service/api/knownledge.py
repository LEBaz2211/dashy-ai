import chromadb
from sqlalchemy.orm import Session

from ..db import crud
from ..db import schemas

client = chromadb.Client()
collection = client.create_collection("user_knowledge")


def extract_knowledge_from_message(message: str):
    if "project" in message:
        return {"type": "project", "content": message}
    return None


def store_knowledge(db: Session, user_id: str, message: str):
    knowledge = extract_knowledge_from_message(message)
    if knowledge:
        knowledge_data = schemas.UserKnowledgeCreate(user_id=user_id, **knowledge)
        crud.create_user_knowledge(db, knowledge_data)

        collection.add(
            documents=[knowledge_data.content],
            ids=[knowledge_data.user_id],
            metadatas=[{"type": knowledge_data.type}]
        )
        print(f"Stored knowledge: {knowledge_data.dict()}")
