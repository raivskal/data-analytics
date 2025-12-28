import os
from django.conf import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import markdown

# Initialize model once
model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=settings.GOOGLE_API_KEY
)

chat_history = [
    SystemMessage(content="You are a helpful AI assistant")
]


def ask_ai(user_input: str):
    chat_history.append(HumanMessage(content=user_input))
    result = model.invoke(chat_history)

    ai_markdown = result.content
    ai_html = markdown.markdown(ai_markdown)

    chat_history.append(AIMessage(content=ai_html))

    return ai_html, chat_history
