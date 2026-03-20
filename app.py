import streamlit as st

# Import all modules
from voice import get_voice_input, speak_output
from data import get_context
from ai import get_ai_response


st.set_page_config(page_title="AI Farming Assistant", page_icon="🌾")

st.title("🌾 AI Farming Assistant")
st.write("Ask your question by voice or text in your own language")

# 🔹 Option: Text input (for testing/demo safety)
user_input = st.text_input("Type your question (or use voice):")

# 🔹 Button to trigger voice input
if st.button("🎙️ Use Voice Input"):
    query, language = get_voice_input()
    st.write(f"🗣️ You said: {query} ({language})")

    context = get_context(query)
    response = get_ai_response(query, context, language)

    st.subheader("🤖 AI Advice")
    st.write(response)

    speak_output(response, language)


# 🔹 Text input flow (fallback)
if user_input:
    # Default language = English (can improve later)
    language = "en"

    st.write(f"📝 You typed: {user_input}")

    context = get_context(user_input)
    response = get_ai_response(user_input, context, language)

    st.subheader("🤖 AI Advice")
    st.write(response)

    speak_output(response, language)