import tkinter as tk
import ttkbootstrap as ttk
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from tkinter.scrolledtext import ScrolledText

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


def send_message(event=None):  # Allow event parameter for binding
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


# Initialize Tkinter window with ttkbootstrap style
root = ttk.Window(themename="flatly")  # Choose "flatly" for a light background

# Set window title
root.title("Chat with AI")

# Set initial window size and make it resizable
root.geometry("800x600")  # Start with a larger size (800x600)
root.minsize(800, 600)    # Allow resizing but not smaller than 800x600

# Define a larger font
large_font = ("Helvetica", 18)

# Create a custom style for the button
style = ttk.Style()
style.configure("Custom.TButton", font=("Helvetica", 20), padding=10)

# Create chat window (scrolled text) with larger font
chat_box = ScrolledText(
    root,
    wrap=tk.WORD,
    font=large_font,
    state=tk.DISABLED
)
chat_box.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

# Create input field for user messages with larger font
user_input = ttk.Entry(root, width=55, font=large_font)
user_input.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

# Create send button with custom font style
send_button = ttk.Button(
    root, text="Send", style="Custom.TButton", command=send_message)
send_button.grid(row=1, column=1, padx=20, pady=10)

# Bind the Enter key to the send_message function
user_input.bind("<Return>", send_message)  # Bind Enter to send_message

# Configure grid to make it resizable
root.grid_columnconfigure(0, weight=1)  # Make the input field expand
root.grid_rowconfigure(0, weight=1)     # Make the chat box expand

# Run the Tkinter event loop
root.mainloop()
