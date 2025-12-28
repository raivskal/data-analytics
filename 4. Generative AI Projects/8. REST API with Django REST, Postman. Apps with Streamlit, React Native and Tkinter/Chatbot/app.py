import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Initialize Chat Model
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=GOOGLE_API_KEY
)

# Streamlit app setup
st.set_page_config(page_title="Chat with AI", layout="wide")
st.title("Chat with AI Assistant")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content="You are a helpful AI assistant")
    ]

# Chat UI
st.write("---")
for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)

# User input at the bottom
with st.container():
    prompt = st.text_input(
        "Your message:", placeholder="Type your message here...", key="input_field")
    if st.button("Send", key="send_button"):
        if prompt.strip():
            # Add user message to the chat history
            st.session_state.chat_history.append(HumanMessage(content=prompt))

            # Generate AI response
            with st.chat_message("assistant"):
                st.markdown("_Generating response..._")
                result = model.invoke(st.session_state.chat_history)
                response = result.content
                st.session_state.chat_history.append(
                    AIMessage(content=response))

                # Replace placeholder with actual response
                st.rerun()
