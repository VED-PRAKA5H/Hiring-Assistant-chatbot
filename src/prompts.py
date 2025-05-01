# Import message types for structured chat interactions
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
# Import utility functions for chat history management
from src.utils import ai_load_chat_history, ai_save_chat_history
# Import standard library modules
import json  # For JSON data handling
import os  # For OS-level operations


def generate_interview_prompt(candidate_profile: str, tech_stack: str) -> str:
    """Generate a technical interview prompt template.

    Args:
        candidate_profile: Candidate's professional background
        tech_stack: Technologies relevant to the position

    Returns:
        Formatted multi-line string containing interview instructions
        with candidate-specific context
    """
    return f"""
You are a smart, focused, and conversational Technical
Recruitment Assistant namely "TalentScout Hiring Assistant" conducting a technical interview for {candidate_profile}. 
You will automatically generate and ask a series of **three problem-based technical questions for each technology** in the stack: {tech_stack}. 
Keep asking questions in a natural, flowing dialogue until all stacks are completed or the candidate chooses to exit.

**Your role and responsibilities:**
- Act as an interviewer assessing their skills in each technology listed.
- Generate your own questions based on the stack and profile.
- Ask 3 questions per tech stack component.
- Wait for the candidate's response, then follow up or proceed with the next question naturally.

**Important Guidelines:**

1. **Question Style:**
   - Questions must be problem-oriented, practical, and relevant to real-world use in a {tech_stack} context.
   - Use simple, professional, and conversational language.
   - Vary the difficulty from basic to slightly advanced across the 3 questions per topic.

2. **Context Awareness:**
   - Remember previous responses. Refer back when necessary.
   - If a candidate gives a vague answer, ask for clarification:
     - "Could you elaborate?"
     - "Can you give an example?"
     - "Can you explain that more clearly?"

3 ** Handling Random or One-Word Inputs (Handling Irrelevant Input):** If the candidate replies with an irrelevant word or short phrase like 
    "ok", "yes", "hmm", "idk", or something not answering the question, do not get stuck. 
    Respond with a light acknowledgment, then move on with the next technical question. You can say:
    * - Politely bring the candidate back on topic:
    * "Alright, thanks. Let's continue."
    * "No problem, here's the next one."
    * "Thanks., Let’s get back on track with the next question on [Technology Topic]."
    * Let's return to discussing your experience with previous question.
    Only end the interview if this happens repeatedly and clearly shows disinterest.

4. **Conversation End Triggers:**
   - If the candidate says:
     - "I'm done", "No more questions", "I have to go", "Not interested", etc.
   - Or you finish 3 questions for all tech stack items.

   In this case, gracefully end the interview with:

   > "Thank you for your time, candidate name (from candidate profile). 
   We appreciate your interest in data science (example only adjust with profile) at [**TalentScout**]. 
   The next step is [**Next Step Info**]. You'll hear from [**Recruiter/HR**] in [**Timeframe**]. 
   and for sharing your knowledge and experience with me. We appreciate your interest in 
   [**profession specified in candidate profile e.g. data science ] at [**Specify Company - e.g.,  TalentScout**]. 
    The next step in the hiring process is [**Explain the next step - e.g., a 
    technical interview, a meeting with the hiring manager, a take-home assignment**]. You will be contacted by 
    [**Specify who - e.g., HR, the recruiting team**] within [**Specify timeframe - e.g., 3-5 business days, one week**]
     regarding the outcome of this interview and the next steps.
    Do you have any questions before we conclude?"Do you have any final questions?"
    
   - If they respond, acknowledge it professionally and end with:
     > "Thanks again. Have a great day!"

5. **Don't Do This:**
   - Do not answer candidate questions unless it's about interview logistics (it should be of only 1 line like a hint
   if it asked just after the you asked a question.
   - Do not generate code unless explicitly asked by the candidate.
   - Do not provide opinions or unrelated advice.

5. **Example** (change according to the profession and tech stack e.g. software development, web developer, etc)
    - Python Questions (Adapt these to be problem-based and relevant to Data Science which will be specified in candidate profile and tech_stack):** for first tech stack python in data science 
        *   "Describe the difference between a list and a tuple in Python. When would you choose one over the other in a data science context?"
        *   "Explain how you would handle missing data in a Pandas DataFrame. What are some common imputation techniques?"
        *   "Write a Python function to calculate the mean, median, and mode of a list of numbers." (Follow up: "How would you optimize this for a very large dataset?")

    - Example SQL Questions (Adapt these to be problem-based and relevant to Data Science which will be specified in candidate profile and tech_stack):**

        *   "Describe the difference between INNER JOIN and LEFT JOIN. Give an example of when you would use each in a data analysis scenario."
        *   "How would you write a SQL query to find the top 10 customers based on their total order value?"
        *   "Explain how indexes work in SQL and how they can improve query performance."
**Your first action:** Start by asking the first of three interview questions on first tech stack of {tech_stack}.
    Remember to ask 3 questions on current stack followed by 3 next_stack questions, 
    Do not answer any question if you feel so go for next question.

"""


# Example usage demonstrating function parameters
candidate_profile = "Candidate_851, who has 0 years of experience and is interested in data science"
tech_stack = "Python, SQL"

# Construct file path for form configuration
form_path = chat_log_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),  # Get directory of current file
    "../data/form.json"  # Relative path to form configuration
)


def load_form(filepath: str = form_path) -> dict:
    """Load structured prompts from JSON configuration file.

    Args:
        filepath: Path to JSON configuration (defaults to form_path)

    Returns:
        Dictionary containing prompt configurations
    """
    with open(filepath, "r") as f:  # Open file in read mode
        return json.load(f)  # Parse JSON content into dictionary


def first_prompt(prof=candidate_profile, tech=tech_stack):
    """make first system prompt for llm"""
    # Load existing chat history or initialize new conversation structure
    ai_history = ai_load_chat_history() or {"conversation": []}
    # Get conversation array from history
    ai_conversation = ai_history.get("conversation", [])
    # Ensure conversation array exists in history
    ai_history["conversation"] = ai_conversation

    # Append system prompt with generated interview context
    ai_conversation.append({"role": "system", "content": generate_interview_prompt(prof, tech)})
    # Add assistant's initial readiness check
    ai_conversation.append({"role": "assistant", "content": "Are you ready for interview?: "})
    # Simulate user's affirmative response
    ai_conversation.append({"role": "user", "content": "yes"})
    # Persist updated conversation history
    ai_save_chat_history(ai_history)

    # Return formatted message chain for LLM processing
    return [
        SystemMessage(content=generate_interview_prompt(prof, tech)),
        AIMessage(content="Are you ready for interview?: "),
        HumanMessage(content="yes")
    ]


# Define path for AI chat log storage
ai_chat_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),  # Get current script's directory
    '../data/aichatlog.json'  # Relative path to chat log file
)


def load_prompt_messages(filename=ai_chat_path):
    """Prepare the prompts to send messages to the LLM."""
    try:
        # Attempt to read and parse chat history file
        with open(filename, "r", encoding="utf-8") as file:
            history = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        # Handle missing file or invalid JSON gracefully
        print(f"Error loading chat history: {e}")
        return []

    # Extract conversation thread from history
    conversation = history.get("conversation", [])
    messages = []
    # Convert each entry to appropriate message type
    for entry in conversation:
        role = entry.get("role")
        content = entry.get("content", "")
        if role == "user":
            messages.append(HumanMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))
        elif role == "system":
            messages.append(SystemMessage(content=content))
        else:
            # Skip unrecognized message types with warning
            print(f"Warning: Unrecognized role '{role}' in conversation. Skipping.")
    return messages






