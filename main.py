from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from flask import Flask, request, jsonify, send_file
from gtts import gTTS
import os
import time

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


# Directory for saving audio files
AUDIO_DIR = "audio_files"

# Ensure the audio directory exists
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

def generate_audio(text, filename="response.mp3"):
    """Generate an audio file from the provided text using gTTS"""
    audio_path = os.path.join(AUDIO_DIR, filename)
    print(f"Saving audio file to {audio_path}")
    
    tts = gTTS(text=text, lang="en")  # You can change 'en' to other languages if needed
    tts.save(audio_path)

# Global variable for context
context = ""  

@app.route('/chat', methods=['GET'])  
def chat():
    global context

    # Get user input from the request
    data = request.get_json()
    user_input = data.get('question', '').strip().lower()
    speaker = data.get('speaker', True)

    result = chain.invoke({"context": context, "question": user_input})

    context = f"{context}\nUser: {user_input}\nAI: {result}"

    # Generate a dynamic audio file name using timestamp
    timestamp = int(time.time())
    audio_filename = f"response_{timestamp}.mp3"
    
    generate_audio(result, audio_filename)
    
    # Return both the audio file URL and text response as a JSON
    return jsonify({
        'text': result,
        'audio': request.host_url + AUDIO_DIR + "/" + audio_filename 
    })

# Route to serve the audio file
@app.route('/audio_files/<filename>', methods=['GET'])
def serve_audio(filename):
    audio_path = os.path.join(os.getcwd(), AUDIO_DIR, filename)
    if os.path.exists(audio_path):
        return send_file(audio_path, mimetype='audio/mp3')
    return jsonify({'error': 'Audio file not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
