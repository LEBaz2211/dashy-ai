import json
from openai import OpenAI

def query_llm(messages, model="MaziyarPanahi/Llama-3-8B-Instruct-32k-v0.1-GGUF"):
    client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7
    )
    return completion.choices[0].message.content

def clean_and_parse_json(json_string):
    try:
        json_string = json_string.strip()
        if json_string.startswith('"') and json_string.endswith('"'):
            json_string = json_string[1:-1].replace('\\"', '"')
        json_string = json_string.replace('\n', '')
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON: {e}")

def correct_json_parsing(malformed_json, max_retries=3):
    correction_prompt = f"""
The assistant has responded with a malformed JSON. The malformed JSON string is given below:{malformed_json}
Your task is to return a corrected and well-formatted JSON that matches the intended structure:

1. Ensure that it is a valid JSON array.
2. Each element should have the following structure:
  - `name` (string): The function name to call.
  - Other key-value pairs should be arguments to the function.

Return only the corrected JSON, without any extra explanations.
"""

    messages = [
        {"role": "system", "content": "You are an expert in correcting JSON parsing errors."},
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
