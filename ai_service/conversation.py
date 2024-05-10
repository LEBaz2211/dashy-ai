from sqlalchemy.orm import Session
from ai_service import schemas, crud
from ai_service.ai_manager import query_llm, clean_and_parse_json

class ConversationManager:
    def __init__(self, db: Session):
        self.db = db
        self.model = "MaziyarPanahi/Llama-3-8B-Instruct-32k-v0.1-GGUF"

    def store_conversation_message(self, message_data: schemas.ConversationMessageCreate):
        return crud.create_conversation_message(self.db, message_data)

    def query_llm_for_conversation(self, user_query, messages):
        llm_response = query_llm(messages, self.model)
        try:
            function_calls = clean_and_parse_json(llm_response)
        except ValueError as e:
            return f"Parsing error: {e}"

        if not isinstance(function_calls, list):
            function_calls = [function_calls]

        return function_calls
