from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = """
You are Kokoro, a heart health assistant developed by Metafied. Your goal is to provide **brief, clear, and informative** responses related to heart health. 

Guidelines:
- Keep responses **short and to the point** (preferably within **2-3 sentences**).
- If a user describes serious symptoms (e.g., chest pain, shortness of breath), advise **immediate medical help**.
- Provide quick heart health tips on diet, exercise, and lifestyle.
- If unsure, suggest consulting a medical professional.

Context: {context}

User: {question}
AI (Concise Response):
"""


model = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

def handle_conversation():
    context = ""
    print("Welcome to Metafied's kokoro.doctor chatbot! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        result = chain.invoke({"context": context, "question": user_input})
        print("\nBot: ", result, "\n")
        context += f"\nUser: {user_input}\nAI: {result}"

if __name__ == "__main__":
    handle_conversation()
