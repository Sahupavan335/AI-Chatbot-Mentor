# 🎓 AI Chatbot Mentor (Multi-Module Learning Assistant)

An interactive **AI-powered mentoring chatbot** built with **Streamlit + Langchain + Gemini (Google Generative AI)** that provides **module-specific learning guidance** with **isolated chat sessions per module**.

Each learning module works like its **own chat page**, ensuring focused mentoring without topic mixing.

---

## 🚀 Features

- 🧠 **Module-Specific Mentorship**
  - Python
  - SQL
  - Power BI
  - EDA (Exploratory Data Analysis)
  - Machine Learning
  - Deep Learning
  - Generative AI
  - NLP
  - OpenCV
  - Agentic AI

- 📄 **Separate Chat Pages per Module**
  - Each module has its **own chat history**
  - Switching modules feels like navigating to a new page
  - Returning to a module restores its previous conversation

- 🔒 **Strict Scope Control**
  - Answers only related to the selected module
  - Casual messages (hi, ok, thanks, bye) are handled politely
  - Cross-module or unrelated questions are refused automatically

- 🎨 **Modern Neon Dark UI**
  - Glassmorphism cards
  - Gradient highlights
  - Dark, eye-friendly theme
  - Clean UX hierarchy

- 📥 **Chat History Export**
  - Download module-wise chat history as `.txt`

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit  
- **LLM:** Google Gemini (`gemini-2.5-flash`)  
- **Framework:** LangChain  
- **Styling:** Custom CSS (Neon Dark Theme)  
- **State Management:** `st.session_state`  

---

## 📂 Project Structure

```text
├── app.py                # Main Streamlit application
├── .env                  # Environment variables (API keys)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

## 🧠 How It Works

1. Select a learning module
2. A new chat page is created for that module
3. Ask questions strictly related to the selected module
4. Switch modules → new chat
5. Return to a module → previous chat restored

## 🔐 Scope Enforcement Logic

- ✅ Answers module-related questions
- ✅ Responds politely to casual messages
- ❌ Refuses unrelated technical questions with a fixed response:
  - Sorry, I don't know about this question. Please ask something related to the selected module.

## 📈 Future Enhancements

- 📊 Learning progress tracking
- 🧪 Quiz & practice mode per module
- 💾 Persistent chat storage (database)
- 🌗 Light / Dark theme toggle
- 🔎 Module keyword-based validation

## 👨‍💻 Author

### Sahu Pavan
🎓 B.Tech CSE (Data Science)
💡 Interested in AI, ML, GenAI & Backend Development

- LinkedIn: linkedin.com/in/sahu-pavan

