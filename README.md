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
git clone https://github.com/yourusername/talentscout-chatbot.git
cd talentscout-chatbot
```

2. **Set up virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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



