import json  # JSON handling
import os  # File system operations
from faker import Faker  # Fake data generation

# Define paths for chat logs
chat_log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/formchatlog.json')  # User chat log
ai_chat_log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/aichatlog.json')  # AI chat log

faker = Faker()  # Initialize fake data generator


def ensure_log_directory_exists(chat_path=chat_log_path):
    """Ensure the log directory exists before reading/writing."""
    log_dir = os.path.dirname(chat_path)  # Extract directory path
    os.makedirs(log_dir, exist_ok=True)  # Create directory if missing


def load_chat_history():
    """Load chat history from file (create empty if missing or corrupted)."""
    ensure_log_directory_exists()  # Check directory exists
    if not os.path.exists(chat_log_path):  # File doesn't exist
        save_chat_history({"conversation": []})  # Create empty chat log
    try:
        with open(chat_log_path, 'r', encoding='utf-8') as f:
            return json.load(f)  # Load JSON data
    except json.JSONDecodeError:  # Handle corrupted files
        print("Warning: Chat log was corrupted or empty. Resetting...")
        save_chat_history({"conversation": []})  # Reset chat log
        return {"conversation": []}  # Return empty structure


def save_chat_history(history):
    """Save chat history to file."""
    ensure_log_directory_exists()  # Verify directory exists
    with open(chat_log_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4)  # Write pretty-printed JSON


def anonymize_candidate_info(candidate_data):
    """Anonymize candidate information."""
    return {
        "name": f"Candidate_{faker.random_int(min=100, max=999)}",  # Random candidate ID
        "email": faker.email(),  # Fake email
        "phone": f"XXX-XXX-{faker.random_number(digits=4, fix_len=True)}",  # Partially masked phone
        "experience": candidate_data.get('experience', ""),  # Original experience
        "position": candidate_data.get('position', ""),  # Original position
        "location": candidate_data.get('location', ""),  # Original location
        "tech_stack": candidate_data.get('tech_stack', "")  # Original tech stack
    }


def ai_ensure_log_directory_exists(chat_path=ai_chat_log_path):
    """Ensure the log directory exists before reading/writing."""
    log_dir = os.path.dirname(chat_path)  # Extract directory path from filepath
    os.makedirs(log_dir, exist_ok=True)  # Create directory if missing


def ai_load_chat_history():
    """Load chat history from file (create empty if missing or corrupted)."""
    ai_ensure_log_directory_exists()  # Verify directory structure
    if not os.path.exists(ai_chat_log_path):  # Check file existence
       ai_save_chat_history({"conversation": []})  # Initialize empty log
    try:
        with open(ai_chat_log_path, 'r', encoding='utf-8') as f:
            return json.load(f)  # Read JSON data
    except json.JSONDecodeError:  # Handle corrupted files
        print("Warning: Chat log was corrupted or empty. Resetting...")
        ai_save_chat_history({"conversation": []})  # Reset file
        return {"conversation": []}  # Return empty structure


def ai_save_chat_history(history):
    """Save chat history to file."""
    ai_ensure_log_directory_exists()  # Confirm directory exists
    with open(ai_chat_log_path, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4)  # Write formatted JSON


def clear_chat_log():
    """Reset the AI chat log and Chat Log file to an empty conversation."""
    with open(ai_chat_log_path, 'w', encoding='utf-8') as f:
        json.dump({"conversation": []}, f, indent=4)  # Clear AI chat log
    with open(chat_log_path, 'w', encoding='utf-8') as f:
        json.dump({"conversation": []}, f, indent=4)  # Clear user chat log
