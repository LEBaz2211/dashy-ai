import chromadb
from sqlalchemy.orm import Session
from . import schemas, crud

# Initialize ChromaDB
client = chromadb.Client()
collection = client.create_collection("user_knowledge")

# Extract knowledge
def extract_knowledge_from_message(message: str):
    # Simple example of extracting knowledge
    if "project" in message:
        return {"type": "project", "content": message}
    return None

# Add knowledge to the database and ChromaDB
def store_knowledge(db: Session, user_id: str, message: str):
    knowledge = extract_knowledge_from_message(message)
    if knowledge:
        # Store in the database
        knowledge_data = schemas.UserKnowledgeCreate(user_id=user_id, **knowledge)
        crud.create_user_knowledge(db, knowledge_data)

        # Store in ChromaDB
        collection.add(
            documents=[knowledge_data.content],
            ids=[knowledge_data.user_id],
            metadatas=[{"type": knowledge_data.type}]
        )
        print(f"Stored knowledge: {knowledge_data.dict()}")
