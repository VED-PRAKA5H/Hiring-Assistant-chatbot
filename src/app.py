# Import chatbot components and utilities
from src.chatbot import collect_info, fill_info, get_first_question_chatbot, chatbot, answer_modifier, custom_llm
from src.utils import load_chat_history, save_chat_history, clear_chat_log
import gradio as gr  # UI framework
import threading  # Background task handling
import sys  # System operations

# Clear chat logs before starting new session
clear_chat_log()

# Initial greeting setup
greeting, _ = collect_info()  # Get first greeting message
history = load_chat_history() or {"conversation": []}  # Load existing history
conversation = history.get("conversation", [])  # Extract conversation thread
history["conversation"] = conversation  # Ensure conversation key exists
conversation.append({"role": "assistant", "content": greeting})  # Add initial greeting
save_chat_history(history)  # Persist initial state

FORM_FILLING = True  # Control flow flag for form completion

# Gradio UI components
model_dropdown = gr.Dropdown(["openai", "cohere"],  # LLM selection
                             value="openai",
                             label="Model Choice"
                             )
api_input = gr.Textbox(label="API Key",  # API key input
                       type="password",
                       placeholder="sk-... or COHERE_API_KEY"
                       )


def mini_chatbot(message, history, model_choice=None, api_key=None):
    try:
        # Handle exit commands
        if message.lower() in ["exit", "quit", "close"]:
            print("Shutting down the server...")
            threading.Thread(target=lambda: sys.exit(0)).start()  # Async shutdown
            return {"role": "assistant", "content": "Goodbye! The app is shutting down."}

        # Validate API credentials
        elif not model_choice or not api_key:
            return {"role": "assistant",
                    "content": "**Please select a model and enter your API key.** Have you entered?"}

        else:
            global FORM_FILLING
            # Form filling phase
            if FORM_FILLING:
                key, question = collect_info()  # Get next form question
                fill_info(key, message, question)  # Store user response

                if key == "form_completed":  # End of form
                    first_ai_qn = get_first_question_chatbot(
                        custom_llm(api_key, model_choice))  # Generate first technical question
                    FORM_FILLING = False  # Switch to interview phase
                    return {"role": "assistant",
                            "content": question + '\n' + first_ai_qn}  # Final form + first question

                else:
                    return {"role": "assistant", "content": question}  # Next form question

            # Interview phase
            else:
                ai_response = chatbot(message, custom_llm(api_key, model_choice))  # Generate technical response
                return {"role": "assistant", "content": answer_modifier(ai_response)}  # Return de-anonymized response

    except Exception as e:
        return {"role": "assistant", "content": f"**Enter correct credentials:**\n {e}"}  # Error handling


# Gradio app configuration
app = gr.ChatInterface(
    fn=mini_chatbot,
    title="🧠 Technical Interview Assistant",
    description="Type 'exit' or 'quit' to stop the app. **🚨Please fill the additional inputs to start!**",
    theme="soft",
    type="messages",
    chatbot=gr.Chatbot(
        type="messages",
        height=500,
        value=[{"role": "assistant", "content": greeting}]  # Initial chat state
    ),
    additional_inputs=[model_dropdown, api_input]  # Extra input components
)

if __name__ == "__main__":
    app.launch()  # Start web server

