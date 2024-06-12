import json

auto_tag_prompt_template = """
Example JSON output:
{example_output}

User's tasks:
{tasks}

Previous Feedback:
{feedback}

Respond with a JSON array containing each task id and its tags directly as key-value pairs.
"""

auto_tag_prompt_example_output = """
[
  {"id": 1, "tags": ["work", "email"]},
  {"id": 2, "tags": ["personal", "shopping"]}
]
"""

def generate_auto_tag_prompt(tasks, feedback):
    tasks_json = json.dumps(tasks, indent=2)
    feedback_json = json.dumps(feedback, indent=2)
    prompt = auto_tag_prompt_template.format(tasks=tasks_json, example_output=auto_tag_prompt_example_output, feedback=feedback_json)
    # print(prompt)
    return prompt


auto_subtask_prompt_template = """
Example JSON output:
{example_output}

User's task:
{task}

Previous Feedback:
{feedback}

Respond with a JSON array containing the task id and its subtasks directly as key-value pairs.
"""

auto_subtask_prompt_example_output = """
[
  {"id": 1, "subtasks": ["Setup project", "Install dependencies"]}
]
"""

def generate_auto_subtask_prompt(task, feedback):
    task_json = json.dumps(task, indent=2)
    feedback_json = json.dumps(feedback, indent=2)
    prompt = auto_subtask_prompt_template.format(task=task_json, example_output=auto_subtask_prompt_example_output, feedback=feedback_json)
    return prompt