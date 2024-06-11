import sys
import os

# Add the project directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_service.db.database import init_ai_database

if __name__ == "__main__":
    print("Initializing AI Database...")
    init_ai_database()
    print("AI Database initialized.")