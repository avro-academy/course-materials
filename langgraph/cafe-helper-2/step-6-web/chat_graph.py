"""A chatbot as a LangGraph graph: one node that calls the model. The state is the list of messages.

    python chat_graph.py
"""
from langchain_ollama import ChatOllama
from langgraph.graph import END, START, MessagesState, StateGraph

llm = ChatOllama(model="qwen3:4b-instruct", temperature=0)


def chatbot(state: MessagesState):
    system = ("system", "You are Café Helper for Corner Café in Sydney. Answer in one or two short sentences.")
    return {"messages": [llm.invoke([system] + state["messages"])]}


graph = StateGraph(MessagesState)
graph.add_node("chatbot", chatbot)
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)
app = graph.compile()

history = []
for text in ["Hi! I'm Sam.", "What's my name?"]:
    result = app.invoke({"messages": history + [("user", text)]})
    history = result["messages"]  # the whole conversation, with the new reply added
    print("You:", text)
    print("Bot:", history[-1].content)

print()
print(len(history), "messages:", [type(m).__name__ for m in history])
