import pyttsx3
import asyncio
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from googletrans import Translator
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 185)  # Adjust speech rate
engine.setProperty("volume", 1)  # Adjust volume

# Get the available voices
voices = engine.getProperty('voices')
# Set the female voice - example with "Samantha"
for voice in voices:
    if "Samantha" in voice.name:
        engine.setProperty('voice', voice.id)
        break

# Initialize Translator
translator = Translator()

# Default language
current_language = "en"

template = """
You are Kokoro, a friendly, emphathetic, compassionate heart health assistant developed by Metafied. 
Your goal is to provide brief, clear, and informative responses related to heart health. 

Guidelines:
- Keep your tone Emphathetic, com
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

@app.route('/chat', methods=['POST'])
async def chat():
    global current_language  # Make the language setting persistent
    context = ""
    
    # Get user input from the POST request
    data = request.get_json()
    user_input = data.get('question', '').strip().lower()
    language = data.get('language', 'en').strip().lower()

    # Handle language change request
    if language in ["hi", "hinglish", "en"]:
        current_language = language

    # Generate response in English first
    result = chain.invoke({"context": context, "question": user_input})

    # Speak the response in the selected language
    speak(result)

    # Return the response in JSON format
    return jsonify({"response": result, "language": current_language})

if __name__ == '__main__':
    app.run(debug=True)
