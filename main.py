from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from flask import Flask, request, jsonify, send_file
from gtts import gTTS
from googletrans import Translator  
import os
import asyncio


# Template for the model's response
template = """
You are Kokoro, a friendly and empathetic heart health assistant developed by Metafied. Your role is to provide actionable and accurate information about heart health, including symptoms, medical advice, dietary recommendations, and lifestyle changes. 

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

# Initialize the model and Flask app
app = Flask(__name__)

model = OllamaLLM(model="llama3.2")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Translator for translation
translator = Translator()


def generate_audio(text, filename="response.mp3", lang="en"):
    audio_path = "./" + filename 
    
    tts = gTTS(text=text, lang=lang)  
    tts.save(audio_path)


# Global variable for context
context = ""  

@app.route('/chat', methods=['GET'])  
async def chat():
    global context

    # Get user input from the request
    data = request.get_json()
    user_input = data.get('question', '').strip().lower()
    speaker = data.get('speaker', True)
    language = data.get('language', 'en')  # Accept the 'language' parameter

    result = chain.invoke({"context": context, "question": user_input})

    context = f"{context}\nUser: {user_input}\nAI: {result}"

    # If the requested language is Hindi, translate the result synchronously
    if language == 'hi':
        result = translator.translate(result, src='en', dest='hi').text  # Synchronous translation



    # Generate audio from the response in the specified language
    audio_filename = "response.mp3"  
    generate_audio(result, filename=audio_filename, lang=language)

    # Return both the audio file URL and text response as a JSON
    return jsonify({
        'text': result,
        'audio': request.host_url + audio_filename  
    })

# Route to serve the audio file
@app.route('/<filename>', methods=['GET'])
def serve_audio(filename):
    audio_path = f"./{filename}"
    if os.path.exists(audio_path):
        return send_file(audio_path, mimetype='audio/mp3')
    return jsonify({'error': 'Audio file not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
