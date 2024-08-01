# Dashy-AI Backend

This repository contains the backend service for the Dashy-AI application, which provides various AI-powered features and integrations. The backend service is built with FastAPI and serves as an API for managing tasks, subtasks, tags, feedback, and user data. It works in conjunction with the frontend application, Dashy.

## Project Structure

The project is organized as follows:

```
dashy-ai/
├── initialize_database.py
├── ai_service/
│   ├── main.py
│   ├── __init__.py
│   ├── api/
│   │   ├── ai_manager.py
│   │   ├── auth.py
│   │   ├── feedback.py
│   │   ├── knownledge.py
│   │   ├── prompts.py
│   │   ├── subtasks.py
│   │   ├── tagging.py
│   │   └── __init__.py
│   ├── db/
│   │   ├── ai_models.py
│   │   ├── common_models.py
│   │   ├── database.py
│   │   ├── __init__.py
│   │   ├── crud/
│   │   │   ├── aitask.py
│   │   │   ├── conversation.py
│   │   │   ├── dashboard.py
│   │   │   ├── feedback.py
│   │   │   ├── knowledge.py
│   │   │   ├── prompt.py
│   │   │   ├── subtask.py
│   │   │   ├── tag.py
│   │   │   ├── task.py
│   │   │   ├── tasklist.py
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   │   ├── schemas/
│   │   │   ├── ai_task.py
│   │   │   ├── common.py
│   │   │   ├── conversation.py
│   │   │   ├── dashboard.py
│   │   │   ├── feedback.py
│   │   │   ├── knowledge.py
│   │   │   ├── prompt.py
│   │   │   ├── subtask.py
│   │   │   ├── tag.py
│   │   │   ├── task.py
│   │   │   ├── tasklist.py
│   │   │   ├── user.py
│   │   │   └── __init__.py
│   ├── routes/
│   │   ├── aitask.py
│   │   ├── auto_subtask.py
│   │   ├── auto_tag.py
│   │   ├── conversation.py
│   │   ├── dashboard.py
│   │   ├── feedback.py
│   │   ├── subtask.py
│   │   ├── tag.py
│   │   ├── task.py
│   │   ├── tasklist.py
│   │   ├── user.py
│   │   └── __init__.py
│   └── utils/
```

## Getting Started

### Prerequisites

- Python 3.8+
- FastAPI
- SQLAlchemy
- A PostgreSQL database

### Setup and Installation

1. **Clone the repository:**

   ```
   git clone https://github.com/yourusername/dashy-ai.git
   cd dashy-ai
   ```

2. **Install dependencies:**

   ```
   pip install -r requirements.txt
   ```

3. **Environment Variables:**

   Create a `.env` file in the root directory and add the necessary environment variables:

   ```
   SQLALCHEMY_DATABASE_URL=<your_database_url>
   SQLALCHEMY_PRISMA_DATABASE_URL=<your_prisma_database_url>
   SECRET_KEY=<your_secret_key>
   ```

4. **Initialize the Database:**

   Run the script to initialize the database:

   ```
   python initialize_database.py
   ```

### Running the Application

To start the FastAPI application, run:

```
uvicorn ai_service.main:app --reload
```

The application will be available at `http://localhost:8000`.

### Frontend Integration

This backend service is designed to work seamlessly with the Dashy frontend application. Ensure that the frontend is set up and running properly to fully utilize the features provided by the backend.

### Key Features

- **User Authentication:** Secure login and registration.
- **Task Management:** Create, update, delete tasks, and manage task lists.
- **Subtask and Tagging Automation:** Automatically generate subtasks and tags using AI models.
- **Feedback System:** Collect and manage user feedback.
- **AI Conversation Management:** Manage and store AI-driven conversations.

### Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.

### Contact

For any inquiries, please contact [basil@mannaerts.dev](mailto:basil@mannaerts.dev).
