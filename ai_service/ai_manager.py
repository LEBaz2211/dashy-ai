import json
from openai import OpenAI
from sqlalchemy.orm import Session
from datetime import datetime
from . import crud, schemas

# Initialize LLM Client
def query_llm(messages, model="MaziyarPanahi/Llama-3-8B-Instruct-32k-v0.1-GGUF"):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7
    )
    return completion.choices[0].message.content

# Clean and parse JSON
def clean_and_parse_json(json_string):
    try:
        json_string = json_string.strip()
        if json_string.startswith('"') and json_string.endswith('"'):
            json_string = json_string[1:-1].replace('\\"', '"')
        json_string = json_string.replace('\n', '')
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}")

# Correct malformed JSON
def correct_json_parsing(malformed_json, max_retries=3):
    correction_prompt = f"""
    The assistant has responded with a malformed JSON. The malformed JSON string is given below:{malformed_json}
    Your task is to return a corrected and well-formatted JSON that matches the intended structure.

    Ensure that it is a valid JSON array containing function names and arguments directly as key-value pairs.
    """

    messages = [
        {"role": "system", "content": """
         You are an expert in correcting JSON parsing errors. You must only output JSON-formatted text, with no other words.
         Always output in this example format:
            [
                {"name": "function_name", "arg1": "value1", "arg2": "value2"},
                {"name": "function_name", "arg1": "value1", "arg2": "value2"}
            ]
         where function_name is the name of the function and arg1, arg2, etc. are the arguments.
            """},
        {"role": "user", "content": correction_prompt}
    ]

    retries = 0
    while retries < max_retries:
        corrected_response = query_llm(messages)
        try:
            return clean_and_parse_json(corrected_response)
        except ValueError as e:
            print(f"Correction attempt {retries + 1} failed: {e}")
            retries += 1
    raise ValueError(f"Failed to correct JSON after {max_retries} attempts.")

# Create function response prompt
def create_function_response_prompt(messages, function_results):
    messages.append({"role": "user", "content": f"Function calls executed. Here's the response:\n{json.dumps(function_results, indent=2)}. Answer the initial question NOW."})
    return messages

# Extract knowledge from message
def extract_knowledge_from_message(message: str):
    if "project" in message:
        return {"type": "project", "content": message}
    return None

# Store knowledge in the database
def store_knowledge(db: Session, user_id: str, message: str):
    knowledge = extract_knowledge_from_message(message)
    if knowledge:
        knowledge_data = schemas.UserKnowledgeCreate(user_id=user_id, **knowledge)
        crud.create_user_knowledge(db, knowledge_data)

# Conversation Manager
class ConversationManager:
    def __init__(self, db: Session, user_id: str):
        self.db = db
        self.user_id = user_id
        self.model = "MaziyarPanahi/Llama-3-8B-Instruct-32k-v0.1-GGUF"
        # self.model = "int2eh/llama-3-8B-Instruct-function-calling-v0.2-Q6_K-GGUF"
        self.function_schemas = {
            "store_knowledge": {
                "name": "store_knowledge",
                "description": """
                Store knowledge about the user and ONLY about the user, or what he is doing.
                You should never use this function to store knowledge about the assistant or something you are explaining.
                Bad Examples: 
                - store_knowledge("The assistant is running on a server.")
                - store_knowledge("SEO is the process of optimizing your online content so that a search engine likes to show it as a top result for searches of a certain keyword.")
                Good Example: store_knowledge("The user is working on a new project around AI and ML")
                """,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "description": "Knowledge type, e.g. project, object, etc."},
                        "content": {"type": "string", "description": "Content of the knowledge."},
                    },
                    "required": ["type", "content"]
                }
            }
        }

    def create_system_prompt(self):
        example_JSON_output = """
        [
            {"name": "store_knowledge", "type": "project", "content": "The user is working on a new project around AI and ML"},
            {"name": "store_knowledge", "type": "object", "content": "The user mentioned he has a new laptop, a MacBook Pro."},
        ]

        Other EXAMPLE JSON output:
        [
            {"name": "store_knowledge", "type": "family", "content": "The user has a wife and two kids."},
            {"name": "store_knowledge", "type": "hobby", "content": "The user enjoys playing chess in his free time."},
        ]
        """
        function_list = json.dumps(list(self.function_schemas.values()), indent=2)
        return f"""You are an AI assistant who has access to function calls. You generally simply have a conversation with the user,
          but sometimes you need to perform a function call. Here are the available functions you can call:
        {function_list}
        """

    def query_llm_for_conversation(self, messages):
        llm_response = query_llm(messages, model=self.model)

        # Detect if the AI wants to perform a function call
        if llm_response.startswith("["):
            print("Function call detected.")
            try:
                function_calls = clean_and_parse_json(llm_response)
                # Verify the output format
                for function_call in function_calls:
                    if "name" not in function_call:
                        raise ValueError("Function name not found in function call.")
            except ValueError as e:
                try:
                    function_calls = correct_json_parsing(llm_response)
                except ValueError as correction_error:
                    return [], f"Error correcting JSON: {correction_error}"

            if not isinstance(function_calls, list):
                function_calls = [function_calls]
        else:
            function_calls = []

        return function_calls, llm_response

    def store_knowledge_function(self, knowledge_data):
        store_knowledge(self.db, self.user_id, knowledge_data["content"])

    def start_conversation(self, user_id: str, conversation: list):
        system_prompt = {"role": "system", "content": self.create_system_prompt()}
        user_message = conversation[0]
        messages = [system_prompt, user_message]

        function_calls, ai_response = self.query_llm_for_conversation(messages)

        if not function_calls:
            ai_message = {"role": "assistant", "content": ai_response}
            messages.append(ai_message)
        else:
            function_results = []
            messages.append({"role": "assistant", "content": "ai_response"})
            for function_call in function_calls:
                function_name = function_call.pop("name")
                if function_name == "store_knowledge":
                    print("Storing knowledge...")
                    self.store_knowledge_function(function_call)
                    function_results.append({"name": function_name, "content": "Knowledge stored successfully"})
                else:
                    function_results.append({"name": function_name, "content": "Unknown function"})
            ai_message = {"role": "user", "content": json.dumps(function_results, indent=2) + ". Continue the initial conversation NOW."}
            messages.append(ai_message)
            llm_response = query_llm(messages, model=self.model)
            ai_message = {"role": "assistant", "content": llm_response}
            messages.append(ai_message)

        print(messages[0])
        conversation_data = {
            "user_id": user_id,
            "conversation": messages
        }
        return conversation_data

    def continue_conversation(self, existing_messages, user_message):
        user_message = {"role": "user", "content": user_message, "timestamp": str(datetime.utcnow())}
        messages = existing_messages + [user_message]

        function_calls, ai_response = self.query_llm_for_conversation(messages)

        if not function_calls:
            ai_message = {"role": "assistant", "content": ai_response}
            messages.append(ai_message)
            return messages
        else:
            function_results = []
            for function_call in function_calls:
                function_name = function_call.pop("name")
                if function_name == "store_knowledge":
                    self.store_knowledge_function(function_call)
                    function_results.append({"name": function_name, "content": "Knowledge stored successfully"})
                else:
                    function_results.append({"name": function_name, "content": "Unknown function"})
            ai_message = {"role": "user", "content": json.dumps(function_results, indent=2) + ". Continue the initial conversation NOW."}
            messages.append(ai_message)
            llm_response = query_llm(messages, model=self.model)
            ai_message = {"role": "assistant", "content": llm_response}
            messages.append(ai_message)

        return messages



def correct_auto_tag_json_parsing(malformed_json, max_retries=3):
    correction_prompt = f"""
The assistant has responded with a malformed JSON. The malformed JSON string is given below:{malformed_json}
Your task is to return a corrected and well-formatted JSON that matches the intended structure:

1. Ensure that it is a valid JSON array.
2. Each element should have the following structure:
  - `id` (int): the id of the task.
  - `tags` (list of strings).

Return only the corrected JSON, without any extra explanations.
"""

    messages = [
        {"role": "system", "content": """You are an expert in correcting JSON parsing errors. Return only the corrected JSON, without any extra explanations.
         Always output in this example format:
            [
                {"id": 1, "tags": ["work", "email"]},
                {"id": 2, "tags": ["personal", "shopping"]}
            ]
         """},
        {"role": "user", "content": correction_prompt}
    ]

    retries = 0
    while retries < max_retries:
        corrected_response = query_llm(messages, model="MaziyarPanahi/Llama-3-8B-Instruct-32k-v0.1-GGUF")
        try:
            return clean_and_parse_json(corrected_response)
        except ValueError as e:
            print(f"Correction attempt {retries + 1} failed: {e}")
            retries += 1
    raise ValueError(f"Failed to correct JSON after {max_retries} attempts.")


    old_system_prompt = """
        You are an AI assistant who has function calls. You generally simply have a conversation with the user, but sometimes you need to perform a function call.
        If you want to perform a function call, your output should be in JSON format and JSON only, no other words.
        The user may ask various questions which can be answered by calling the following function:
        {function_list}

        Example JSON output:
        {example_JSON_output}

        You basically have two ways to respond, but if you do one, you cannot do the other in the same response:
        1. If you want to perform a function call, output the JSON-formatted function call.
        2. If you want to continue the conversation, output the response as a normal message.
        If you made a function call in your previous response, you MUST ALWAYS continue the conversation. DO NOT PERFORM ANY FUNCTION CALLS TWICE IN A ROW, You must talk between.
        You must not always perform a function call. For example, if the user asks a question, you should answer it directly, without performing a function call, but if the user
        talks aout himself, a project, an object, etc., you should store that knowledge.
        NEVER MAKE A FUNCTION CALL WHEN THE USER ASKS A QUESTION. ONLY MAKE FUNCTION CALLS WHEN THE USER TALKS ABOUT HIMSELF, A PROJECT, AN OBJECT, ETC.
        """
