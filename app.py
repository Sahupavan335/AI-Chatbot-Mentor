import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# ---------------- CONFIG ----------------
st.set_page_config(
    page_icon="🎓",
    layout="wide",
)

# Load API Key
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")

# ---------------- STYLES ----------------
st.markdown("""
<style>

/* ===== App Base ===== */
.stApp {
    background-color: #0B1020;
    color: #E5E7EB;
    font-family: 'Inter', sans-serif;
}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {
    background-color: #0F172A;
}

/* ===== Headings ===== */
h1, h2, h3 {
    color: #F9FAFB;
}

/* ===== Glass Cards ===== */
.card {
    background-color: #111827;
    padding: 1.6rem;
    border-radius: 18px;
    border: 1px solid #1F2937;
    box-shadow: 0 0 40px rgba(59,130,246,0.15);
}

/* ===== Gradient Cards ===== */
.gradient-blue {
    background: linear-gradient(135deg, #3B82F6, #A855F7);
    color: white;
    padding: 1.8rem;
    border-radius: 18px;
}

/* ===== Buttons ===== */
.stButton > button {
    background: linear-gradient(135deg, #3B82F6, #A855F7);
    color: white;
    border-radius: 999px;
    padding: 0.6rem 1.6rem;
    border: none;
    font-weight: 600;
}

.stButton > button:hover {
    filter: brightness(1.15);
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("""
<div style="padding:1rem;">
    <h3>🎓 AI Mentor</h3>
    <p style="color:#9CA3AF; font-size:0.9rem;">
        Focused learning.<br>One module at a time.
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# ---------------- HERO ----------------
st.markdown("""
<div class="card">
    <h1 style="text-align:center;">🤖 AI Chatbot Mentor</h1>
    <p style="color:#9CA3AF; font-size:1.05rem; text-align:center;">
        Your personalized AI learning assistant — structured, focused, and mentor-driven.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------- MODULE SELECTION ----------------
modules = [
    "Python", "SQL", "PowerBI", "EDA (Exploratory Data Analysis)",
    "Machine Learning", "Deep Learning",
    "Generative AI (Gen-AI)", "NLP", "OpenCV", "Agentic AI"
]

st.markdown("## 📚 Choose Your Learning Path")

selected_module = st.selectbox(
    "Select a module to start your mentoring session",
    ["-- Select a Module --"] + modules
)

# ---------------- MULTI-MODULE CHAT STATE ----------------
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}

if "current_module" not in st.session_state:
    st.session_state.current_module = None

# ---------------- CHAT SECTION ----------------
if selected_module != "-- Select a Module --":

    # Switch to new "page" when module changes
    if st.session_state.current_module != selected_module:
        st.session_state.current_module = selected_module
        st.session_state.chat_histories.setdefault(selected_module, [])

    messages = st.session_state.chat_histories[selected_module]

    st.divider()

    st.markdown(f"""
    <div class="gradient-blue">
        <h2>Welcome to {selected_module}</h2>
        <p style="opacity:0.9;">
            I’m your dedicated AI mentor for <b>{selected_module}</b>.
            Ask questions, explore concepts, or solve problems step by step.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 💬 Mentoring Chat")
    st.markdown(
        "<p style='color:#9CA3AF;'>Ask questions strictly related to the selected module.</p>",
        unsafe_allow_html=True
    )

    # Display previous messages for this module
    for msg in messages:
        role = "user" if isinstance(msg, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(msg.content)

    # User input
    if prompt := st.chat_input(f"Ask about {selected_module}..."):
        messages.append(HumanMessage(content=prompt))
        with st.chat_message("user"):
            st.markdown(prompt)

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2
        )

        system_instruction = f"""
        ROLE:
        You are an AI mentor dedicated to the module "{selected_module}".

        PRIMARY OBJECTIVE:
        Provide accurate and focused mentoring ONLY for questions related to "{selected_module}".

        SCOPE RULES (VERY IMPORTANT):

        1) LEARNING QUESTIONS:
        - If the user asks a clear question or gives a task that is directly about "{selected_module}",
        you SHOULD answer clearly and helpfully.

        2) CASUAL CONVERSATION (ALLOWED):
        - If the user sends casual or social messages such as:
        hi, hello, ok, okay, thanks, thank you, bye, goodbye, how are you
        - You MAY respond briefly and politely.
        - Keep responses short and general.
        - Do NOT introduce new learning topics.
        - Do NOT shift into another module.

        3) OUT-OF-SCOPE LEARNING QUESTIONS (STRICTLY FORBIDDEN):
        You MUST NOT answer:
        - Questions about any other module
        - Questions from related or adjacent domains
        - General programming, AI, data science, or technical topics outside "{selected_module}"

        FORBIDDEN RESPONSE BEHAVIOR:
        - Do NOT try to partially answer out-of-scope questions
        - Do NOT redirect to another module
        - Do NOT explain why you are refusing

        MANDATORY REFUSAL RESPONSE:
        If the user input is a learning or technical question that is NOT related to "{selected_module}",
        respond with EXACTLY this sentence and nothing else:

        "Sorry, I don't know about this question. Please ask something related to the selected module."

        FINAL SELF-CHECK BEFORE ANSWERING:
        Before responding, internally decide:
        - Is this a "{selected_module}" learning question? -> Answer it
        - Is this casual conversation? -> Reply briefly and politely
        - Is this a learning question outside "{selected_module}"? -> Use the refusal sentence
        """

        chat_context = [SystemMessage(content=system_instruction)] + messages

        with st.chat_message("assistant"):
            try:
                response = llm.invoke(chat_context)
                st.markdown(response.content)
                messages.append(AIMessage(content=response.content))
            except Exception as e:
                st.error(f"Error connecting to Gemini: {e}")

    # ---------------- CHAT HISTORY DOWNLOAD and CLEAR CONVERSATION ----------------
    if messages:
        history_text = f"--- AI Mentoring Session: {selected_module} ---\n\n"
        for m in messages:
            role = "USER" if isinstance(m, HumanMessage) else "MENTOR"
            history_text += f"{role}: {m.content}\n\n"

        st.sidebar.download_button(
            label="📥 Download Chat History",
            data=history_text,
            file_name=f"{selected_module}_session.txt",
            mime="text/plain"
        )

        if st.sidebar.button("🗑 Clear Conversation"):
            st.session_state.chat_histories[selected_module] = []
            st.rerun()
