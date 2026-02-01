import streamlit as st
from nltk.chat.util import Chat, reflections
import nltk

# ----------------------------
# NLTK SETUP
# ----------------------------
@st.cache_resource
def download_nltk():
    nltk.download("punkt")

download_nltk()

# ----------------------------
# CHATBOT PATTERNS
# ----------------------------
pairs = [
    [r"(.*)my name is (.*)", ["Hello %2 😊 How are you today?"]],
    [r"(hi|hey|hello|hola|holla)(.*)", ["Hello 👋", "Hey there 😄"]],
    [r"how are you(.*)", ["I'm doing great! How about you? 😊"]],
    [r"(.*)help(.*)", ["Sure! Tell me what you need help with 🤝"]],
    [r"(.*)your name ?", ["I'm GlobalBot 🤖"]],
    [r"(.*)created you ?", ["I was created using Python 🐍 and NLTK"]],
    [r"(.*)(sports|game)", ["I love cricket 🏏"]],
    [r"bye|quit|exit", ["Goodbye 👋 See you soon!"]],
    [r"(.*)", ["I'm not sure I understand 🤔 Can you rephrase?"]],
]

chatbot = Chat(pairs, reflections)

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="GlobalBot", layout="centered")

# ----------------------------
# CSS
# ----------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #667eea, #764ba2);
}
.chat-box {
    max-width: 700px;
    margin: auto;
}
.user {
    background: #4f46e5;
    color: white;
    padding: 10px;
    border-radius: 15px;
    margin: 6px 0;
    text-align: right;
}
.bot {
    background: #e5e7eb;
    color: black;
    padding: 10px;
    border-radius: 15px;
    margin: 6px 0;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# TITLE
# ----------------------------
st.title("💬 GlobalBot – Chatbot")

# ----------------------------
# SESSION STATE
# ----------------------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ----------------------------
# CHAT DISPLAY
# ----------------------------
st.markdown('<div class="chat-box">', unsafe_allow_html=True)

for msg in st.session_state.chat:
    role = msg["role"]
    css = "user" if role == "user" else "bot"
    st.markdown(
        f'<div class="{css}">{msg["text"]}</div>',
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------
# INPUT FORM (FIX)
# ----------------------------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message")
    send = st.form_submit_button("Send")

if send and user_input.strip():
    # User message
    st.session_state.chat.append({
        "role": "user",
        "text": user_input
    })

    # Bot response
    reply = chatbot.respond(user_input.lower())
    if reply is None:
        reply = "Can you say that again? 🙂"

    st.session_state.chat.append({
        "role": "bot",
        "text": reply
    })

    st.rerun()
