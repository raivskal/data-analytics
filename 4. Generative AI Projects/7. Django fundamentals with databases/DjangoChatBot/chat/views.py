from django.shortcuts import render

# Create your views here.
from .langchain_chat import ask_ai, chat_history


def chat_page(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        ask_ai(user_message)

    return render(request, "chat.html", {
        "history": chat_history
    })
