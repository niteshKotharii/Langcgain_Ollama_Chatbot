import pyttsx3
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 185)  # Adjust speech rate
engine.setProperty("volume", 1)  # Adjust volume


template = """
You are Kokoro, a friendly, empathetic, compassionate heart health assistant developed by Metafied. 
Your goal is to provide brief, clear, and informative responses related to heart health. 

Guidelines:
- Keep your tone empathetic and professional.
- Keep responses short and to the point (preferably within 2-3 sentences).
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

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

@app.route('/chat', methods=['GET'])
def chat():
    context = ""

    # Get user input from the GET request
    data = request.get_json()
    user_input = data.get('question', '').strip().lower()
    speaker = data.get('speaker', True)

    result = chain.invoke({"context": context, "question": user_input})

    if speaker == True:
        speak(result)

    # Return the response in JSON format (without speech)
    return jsonify({"response": result, "language": 'en'})


if __name__ == '__main__':
    app.run(debug=True)