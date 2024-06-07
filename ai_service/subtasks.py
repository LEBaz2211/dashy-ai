from ai_service.prompts import generate_auto_subtask_prompt
from ai_service.ai_manager import correct_auto_subtask_json_parsing, query_llm, clean_and_parse_json
from sqlalchemy.orm import Session
from ai_service import crud, schemas
import json

class AutoSubtasking:
    def __init__(self, db_ai: Session):
        self.db_ai = db_ai
        # self.model = "MaziyarPanahi/Llama-3-8B-Instruct-32k-v0.1-GGUF"
        self.model = "llama3-70b-8192"

    def auto_subtask_tasks(self, tasks, user_id: str, related_tasks: list):
        # Retrieve relevant feedback for "auto_subtask" tasks
        feedback_list = crud.get_feedback(self.db_ai, task_type="auto_subtask")
        print(feedback_list)

        # Find the best and worst feedback based on ratings
        best_feedback = None
        worst_feedback = None
        for feedback in feedback_list:
            if feedback.rating >= 0 and (best_feedback is None or feedback.timestamp > best_feedback.timestamp):
                best_feedback = feedback
            if feedback.rating <= 5 and (worst_feedback is None or feedback.timestamp > worst_feedback.timestamp):
                worst_feedback = feedback

        # Get the AI tasks associated with the best and worst feedback
        best_ai_task = crud.get_ai_task(self.db_ai, best_feedback.ai_task_id) if best_feedback else None
        worst_ai_task = crud.get_ai_task(self.db_ai, worst_feedback.ai_task_id) if worst_feedback else None

        # Prepare feedback information
        feedback = [
            {"ai_output": best_ai_task.ai_output, "feedback": best_feedback.feedback, "rating": best_feedback.rating} if best_feedback else {},
            {"ai_output": worst_ai_task.ai_output, "feedback": worst_feedback.feedback, "rating": worst_feedback.rating} if worst_feedback else {}
        ]
        
        prompt = generate_auto_subtask_prompt(tasks, feedback)
        messages = [
            {"role": "system", "content":
              """You are an AI assistant that automatically generates subtasks for tasks. You must only output JSON-formatted text, with no other words. 
              You must always output in this example format:
                [
                    {"id": 10, "subtasks": ["Setup project", "Install dependencies"]},
                    {"id": 24, "subtasks": ["Create wireframes", "Design logo"]}
                ]
             """},
            {"role": "user", "content": prompt}
        ]

        llm_response = query_llm(messages, self.model)
        try:
            function_calls = clean_and_parse_json(llm_response)
        except ValueError as e:
            return f"Parsing error: {e}"

        if not isinstance(function_calls, list):
            function_calls = [function_calls]

        # Verify the output format and correct if necessary
        for function_call in function_calls:
            if "id" not in function_call or "subtasks" not in function_call:
                print("Invalid output format for {function_call}. Correcting...")
                llm_response = correct_auto_subtask_json_parsing(llm_response)
                function_calls = clean_and_parse_json(llm_response)

        if not isinstance(function_calls, list):
            function_calls = [function_calls]

        # Store AI Task Result
        output = json.dumps(function_calls, indent=2)
        ai_task_data = schemas.AITaskCreate(
            task_type="auto_subtask",
            user_id=user_id,
            related_task_id=related_tasks,
            ai_output=output
        )
        ai_task = crud.create_ai_task(self.db_ai, ai_task_data)

        return function_calls, ai_task.id
