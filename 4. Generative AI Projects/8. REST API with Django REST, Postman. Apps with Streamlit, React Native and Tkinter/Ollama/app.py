import tkinter as tk
from tkinter import scrolledtext
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Initialize the model
model = ChatOllama(
    model="tinyllama",
    temperature=0
)

# Initialize chat history
chat_history = []
system_message = SystemMessage(content="You are helpful AI assistant")
chat_history.append(system_message)

# Function to handle sending messages


def send_message():
    query = user_input.get()
    if query.lower() == "exit":
        root.quit()
    else:
        # Append human message to chat history
        chat_history.append(HumanMessage(content=query))

        # Get AI response
        result = model.invoke(chat_history)
        response = result.content
        chat_history.append(AIMessage(content=response))

        # Display both user and AI messages in the chat window
        chat_box.config(state=tk.NORMAL)
        chat_box.insert(tk.END, f"You: {query}\n")
        chat_box.insert(tk.END, f"AI: {response}\n\n")
        chat_box.config(state=tk.DISABLED)

        # Clear input field
        user_input.delete(0, tk.END)


# Initialize Tkinter window
root = tk.Tk()
root.title("Chat with AI")

# Create chat window (scrolled text)
chat_box = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, width=50, height=20, state=tk.DISABLED)
chat_box.grid(row=0, column=0, padx=10, pady=10)

# Create input field for user messages
user_input = tk.Entry(root, width=50)
user_input.grid(row=1, column=0, padx=10, pady=10)

# Create send button
send_button = tk.Button(root, text="Send", command=send_message)
send_button.grid(row=2, column=0, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
