from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# pip install -qU langchain-ollama

model = ChatOllama(
    model="tinyllama",
    temperature=0
)

chat_history = []

system_message = SystemMessage(content="You are helpful AI assistant")
chat_history.append(system_message)

# chat loop
while True:
    query = input("You: ")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))

    result = model.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))
    print(f"AI response: {response}")

print("----- Message history ------")
print(chat_history)
