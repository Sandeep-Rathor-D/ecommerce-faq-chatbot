import streamlit as st
from chatbot import get_answer
import pandas as pd

# Page config
st.set_page_config(page_title="🛍️ AskMe - FAQ Bot", layout="centered")

st.title("🛍️ AskMe: E-commerce FAQ Chatbot")
st.markdown("Welcome! Ask any question about our services, orders, or products.")

# Load FAQ questions for samples
df = pd.read_csv('faq_data.csv')
sample_questions = df['question'].head(5).tolist()  # pick first 5 as samples

# Show sample questions
st.markdown("#### 💡 Try one of these questions:")
cols = st.columns(5)
for idx, question in enumerate(sample_questions):
    if cols[idx].button(question[:30] + ("..." if len(question) > 30 else "")):
        st.session_state.user_input = question

# Custom CSS for chat styling
st.markdown("""
    <style>
    .chat-wrapper { padding-top: 20px; }
    .chat-message {
        padding: 12px 18px; margin: 10px 0; border-radius: 10px;
        max-width: 90%; font-size: 16px; line-height: 1.6; color: #000;
    }
    .user { background-color: #d4edda; align-self: flex-end; }
    .bot  { background-color: #e2e3e5; }
    .chat-container { display: flex; flex-direction: column; }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_input" not in st.session_state:
    st.session_state.user_input = ""
if "show_fallback_button" not in st.session_state:
    st.session_state.show_fallback_button = False

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.session_state.user_input = ""
    st.session_state.show_fallback_button = False
    st.rerun()



# Input field (keyed so we can programmatically set it)
query = st.text_input("Ask your question:", key="user_input", label_visibility="collapsed")

# Handle query
if query:
    response = get_answer(query)
    st.session_state.chat_history.append(("🧑 You", query))
    st.session_state.chat_history.append(("🤖 Bot", response))

    # Show fallback contact button if no good match
    if response.startswith("Sorry"):
        st.session_state.show_fallback_button = True
    else:
        st.session_state.show_fallback_button = False

# Display chat history
st.markdown("<div class='chat-wrapper'>", unsafe_allow_html=True)
for sender, msg in st.session_state.chat_history:
    css = "user" if "You" in sender else "bot"
    st.markdown(
        f"<div class='chat-message {css} chat-container'><strong>{sender}:</strong><br>{msg}</div>",
        unsafe_allow_html=True
    )
st.markdown("</div>", unsafe_allow_html=True)

# Fallback support button
if st.session_state.get("show_fallback_button"):
    if st.button("📞 Contact Support"):
        st.info("Our support team has been notified! We’ll get back to you shortly.")

# 👍👎 Feedback
st.markdown("---")
st.markdown("### Was this response helpful?")
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("👍 Yes"):
        st.success("Thanks for your feedback!")
with col2:
    if st.button("👎 No"):
        st.warning("We'll use this to improve future responses.")
