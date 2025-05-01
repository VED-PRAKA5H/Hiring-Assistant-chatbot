# Import utility functions and components
from src.utils import ai_load_chat_history, ai_save_chat_history  # AI chat history management
from src.utils import load_chat_history, save_chat_history  # User chat history management
from src.prompts import first_prompt, load_prompt_messages  # Prompt handling
from src.prompts import load_form  # Form configuration loader
from src.context_manager import ContextManager  # Interview state manager
from langchain_cohere import ChatCohere  # Cohere LLM interface
from langchain_core.messages import HumanMessage  # Human message type
from langchain_openai import ChatOpenAI  # OpenAI interface

# ------testing purpose uncomment when use dot env
# from dotenv import load_dotenv
# import os
# # Load environment variables
# load_dotenv()
# cohere_api_key = os.getenv("COHERE_API")
# Initialize LLM
# llm = ChatCohere(cohere_api_key=cohere_api_key, model="command-a-03-2025")

# Load interview form configuration
PROMPTS = load_form()

# Initialize interview context tracker
context = ContextManager()


def custom_llm(api_key1, llm_name):
    """return llm based on user input"""
    if llm_name == 'openai':
        return ChatOpenAI(openai_api_key=api_key1, model="gpt-4-turbo")  # OpenAI GPT-4 model
    elif llm_name == 'cohere':
        return ChatCohere(cohere_api_key=api_key1, model="command-a-03-2025")  # Cohere Command model


def collect_info():
    """First interaction: greet and collect user info (non-AI)."""
    if context.greet:  # Initial greeting state
        context.greet = False  # Mark greeting as completed
        return PROMPTS['greet_user']['prompt'], None  # Return welcome message
    else:
        key, info_question = context.next_info_prompt(PROMPTS)  # Get next question
        if key == 'form_completed':  # All info collected
            return key, PROMPTS['confirmation']['prompt'] + '\n' + PROMPTS['generate_message'][
                'prompt']  # Completion message
        return key, info_question  # Return current question


dkey = []  # Store collected field names
dvalues = []  # Store collected field values


def fill_info(key, user_input, question):
    """Store user responses and update conversation history."""
    history = load_chat_history() or {"conversation": []}  # Load existing history
    conversation = history.get("conversation", [])  # Extract conversation thread

    # Record interaction
    conversation.append({"role": "user", "content": user_input})  # User response
    conversation.append({"role": "assistant", "content": question})  # System question
    history["conversation"] = conversation
    save_chat_history(history)  # Persist conversation

    # Track collected data
    dkey.append(key)  # Store field name
    if user_input.lower() != 'yes':  # Skip affirmative responses
        dvalues.append(user_input)  # Store actual values

    # Update context with collected data
    context.data = {k: v for k, v in zip(dkey, dvalues)}  # Map keys to values


def chatbot(user_input: str, llm):
    """take llm and make interaction"""
    # Load existing AI chat history or initialize empty
    ai_history = ai_load_chat_history() or {"conversation": []}
    ai_conversation = ai_history.get("conversation", [])

    # Record user input in conversation history
    ai_conversation.append({"role": "user", "content": user_input})

    # Prepare message chain for LLM
    prompts = load_prompt_messages()  # Load base prompts
    prompts.append(HumanMessage(content=user_input))  # Add current input

    # Generate AI response and store
    response = llm.invoke(prompts).content  # Invoke LLM
    ai_conversation.append({"role": "assistant", "content": response})

    # Persist updated conversation history
    ai_history["conversation"] = ai_conversation
    ai_save_chat_history(ai_history)
    return response  # Return generated response


def get_first_question_chatbot(llm):
    # Initialization code runs once at startup
    # Generate first question using candidate profile
    ai_response = llm.invoke(first_prompt(context.get_candidate_profile(), context.get_tech_stack())).content

    # Initialize conversation history
    ai_history = ai_load_chat_history() or {"conversation": []}
    ai_conversation = ai_history.get("conversation", [])

    # Store AI's initial question
    ai_conversation.append({"role": "assistant", "content": ai_response})
    ai_history["conversation"] = ai_conversation
    ai_save_chat_history(ai_history)
    return ai_response  # Return first question


def answer_modifier(answer: str):
    # Replace pseudonym with real name if present
    if context.pseudo_name in answer:
        return answer.replace(context.pseudo_name, context.data['full_name'])
    else:
        return answer  # Return unmodified if no pseudonym found
