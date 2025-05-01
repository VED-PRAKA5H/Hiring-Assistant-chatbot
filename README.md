# 💼 TalentScout Hiring Assistant Chatbot

An intelligent AI-powered chatbot designed to assist **TalentScout**, a fictional recruitment agency, with the **initial screening of candidates**. The chatbot collects essential candidate details, understands their tech stack, and dynamically generates technical questions to assess their capabilities — all within a seamless Gradio-based UI.

---

## 🚀 Features

- 📥 Collects candidate information (name, contact, experience, tech stack, etc.)
- 🧠 Auto-generates technical questions based on declared technologies
- 🤖 Maintains conversational context and handles fallbacks gracefully
- 🎨 Built with a user-friendly Gradio interface
- 🔐 Ensures data privacy & simulates secure data handling
- 🛠️ Powered by LLMs (I used Cohere since it free for many api call)(OpenAI, Hugging Face, etc.)
- ☁️ Easy to run locally, with deployment

---

## 🏗️ Project Structure

```text
talentscout-chatbot/
├── assets/  
│   ├── img.png
│   └── demo.mp4                 
├── data  # Prompt templates and examples
│   ├── aichatlog.json
│   ├── form.json
│   └── formchatlog.json
├── src/
│   ├── __init__.py
│   ├── app.py                   # Gradio interface and app logic
│   ├── chatbot.py               # LLM conversation logic
│   ├── prompts.py               # Prompt construction
│   ├── utils.py                 # Helpers for validation, fallback, etc.
│   └── context_manager.py       # Handles conversation state
├── .env                         # API keys (not committed)
├── requirements.txt             # Python dependencies
└── README.md                    # This file

```

---

## 🧩 Tech Stack

| Layer         | Tools                                |
|---------------|--------------------------------------|
| UI            | Gradio                               |
| LLM           | Cohere / OpenAI GPT-4                |
| Prompting     | Manual prompt engineering            |
| Backend       | Python, langchain, faker             |
| Deployment    | AWS, HuggingFace Transformers Spaces |

---

## 🛠️ Installation Instructions

1. **Clone the repo**

```bash
git clone https://github.com/VED-PRAKA5H/Hiring-Assistant-chatbot.git
cd Hiring-Assistant-chatbot
```

2. **Set up virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: activate the virtual environment
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Add your API keys**

Create a `.env` file and add your LLM API key:

```
COHERE_API_KEY=your-key
OPENAI_API_KEY=your-key-here
```

---

## 💬 How to Use

1. Run the chatbot

```bash
python -m src.app
```

2. Open the link (usually `http://localhost:7860`) in your browser.

3. Take interview! The bot will:
   - Greet you
   - Collect your name, contact, experience, tech stack, etc.
   - Generate 3–5 custom technical questions
   - Ask questions based on your tech stack
   - Gracefully end when you say something like "I want to exit the interview"

---

## 📄 Prompt Design

Prompts are modular and stored under `/prompts/`. Each is dynamically filled based on the candidate's inputs.

- **Gathering Info Prompt**: Guides the bot to ask for structured inputs in a friendly tone.
- **Tech Stack Prompt**: Dynamically inserts candidate's declared tools/languages to create specific questions.

Example:

```
Generate 3 Python questions for "candidate_123 with 2 years of experience in Django and NumPy".
```

---

## 🔐 Data Handling
Used the `faker` library:
- No real user data is transferred to llm.
- Simulated or anonymized data is used for demonstration.
- Code is designed with GDPR-style privacy in mind.
- Sensitive fields are validated and masked if needed.

---

## 🧠 Challenges & Solutions

| Challenge                                        | Solution                                                                             |
|--------------------------------------------------|--------------------------------------------------------------------------------------|
| Storing candidate information                    | Used separate `json` file for this stage.                                            |
| Storing student response                         | Used separate `json` file for this stage.                                            |
| Transition from general question to tech question | just start after general query using `if` condition then use only llm bot for query. |
| Model system prompt                              | read many website.                                                                   |

---

## 🎥 Demo

You can view it live on **[Hugging Face Spaces](https://huggingface.co/spaces/vedface/Hiring-Assistant-chatbot)**
showcasing the chatbot in action.

---

## 🔮 Possible Enhancements

- 🌐 **Multilingual Support** via Hugging Face translation pipelines
- 😊 **Sentiment Detection** to assess confidence levels
- 📊 **Candidate Summary Report** generated post-chat
- 💾 **Database integration** to store candidate data securely
- 🎨 Improved UI styling with custom CSS & dark mode

---

## 🤝 Contributing

Pull requests and feedback are welcome! Just make sure to:

- Follow clean code practices
- Add clear commit messages
- Write concise docstrings and comments

---

## 📜 License

MIT License © Ved Prakash

