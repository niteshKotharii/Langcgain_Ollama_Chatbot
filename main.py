from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from flask import Flask, request, jsonify
from deep_translator import GoogleTranslator
from flask_cors import CORS


# Template for the model's response
template = """
You are a friendly and empathetic heart health assistant developed by Metafied. 
Your role is to provide actionable and accurate information about heart health, including symptoms, medical advice, dietary recommendations, and lifestyle changes. 

Guidelines:
- Always maintain an empathetic and professional tone, offering support and reassurance when needed.
- Keep responses concise (ideally 2-3 sentences), prioritizing clarity and actionable advice.
- If the user mentions any symptoms such as chest pain, shortness of breath, dizziness, irregular heartbeat, fatigue, or swelling (among others), suggest suitable lifestyle changes, medications, or dietary adjustments to address these symptoms.
- If the symptoms mentioned are not listed in the guidelines, assess if they could be linked to heart health and provide advice accordingly.
- Regularly offer heart health tips, focusing on diet, exercise, and stress management.

Context: {context}
User: {question}
AI (Concise Response):
"""

# Initialize the Flask app
app = Flask(__name__)

# Initialize the model and the chat prompt template
model = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


# Initialize the context variable to store the conversation history
context = "" 

# Enable CORS for the Flask app
CORS(app)
# Route to handle the chat interaction
@app.route('/chat', methods=['GET'])  
def chat():
    global context

    # Get the user input and language preference from the request
    data = request.get_json()
    user_input = data.get('question', '').strip().lower()
    language = data.get('language', 'en') 

    # Translate the input to English if it's not in English
    if language != "en":
        user_input = GoogleTranslator(source=language, target="en").translate(user_input)

    # Invoke the model to generate a response based on the user input and context
    result = chain.invoke({"context": context, "question": user_input})

    # Update the context with the latest conversation history
    context = f"{context}\nUser: {user_input}\nAI: {result}"

    # Translate the response to the specified language if it's not English
    if language != "en":
        result = GoogleTranslator(source='en', target=language).translate(result)

    # Return the response text and the URL to the audio file
    return jsonify({
        'text': result
    })

# Main block to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
