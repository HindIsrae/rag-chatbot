# app.py
import streamlit as st
from rag_chain import answer

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="MY RAG",
    page_icon="💡",
    layout="centered",
)

# ---- CUSTOM CSS FOR DARK MODE ----
st.markdown("""
<style>
/* Full dark background */
[data-testid="stAppViewContainer"] {
    background-color: #212121;
    color: #f0f0f0;
}

/* Hide Streamlit header & footer */
header, footer { visibility: hidden; }

/* Center the chat container */
.main-container {
    max-width: 600px;
    margin: auto;
    padding: 2rem 1rem;
}

/* Input and button styling */
.stTextInput>div>div>input {
    background-color: #2e2e2e;
    color: #f0f0f0;
    border: 1px solid #444;
    border-radius: 4px;
}
.stButton>button {
    background-color: #ff5722;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
}

/* Chat bubbles */
.chat-user {
    background-color: #37474f;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.5rem;
}
.chat-bot {
    background-color: #455a64;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ---- PAGE CONTENT ----
with st.container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center; color:#ffcc80;'>CHATBOT</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#bbb;'>Your local RAG chatbot powered by Mistral</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Chat
    if "history" not in st.session_state:
        st.session_state.history = []

    query = st.text_input("Ask your question…", key="input")
    send = st.button("Send")

    if send and query:
        response = answer(query)
        st.session_state.history.append((query, response))
        st.session_state.input = ""

    for user_q, bot_a in st.session_state.history:
        st.markdown(f"<div class='chat-user'><strong>You:</strong> {user_q}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='chat-bot'><strong>Bot:</strong> {bot_a}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
