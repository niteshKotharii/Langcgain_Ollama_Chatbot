from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from flask import Flask, request, jsonify
from flask_cors import CORS


# Template for the model's response
template = """
You are a friendly and empathetic heart health assistant developed by Metafied.  
Your role is to provide clear, concise, and actionable heart health advice, including symptoms, medical guidance, dietary tips, and lifestyle recommendations.  

Guidelines:
- Maintain an empathetic and professional tone, offering reassurance when needed.  
- Keep responses brief (2-3 sentences), focusing on clarity and actionability.  
- If the user mentions any heart-related symptoms, provide suitable lifestyle changes, medications, or dietary adjustments to help manage them.  
- If symptoms are unclear or not explicitly linked to heart health, assess their relevance and offer guidance accordingly.    
- Regularly provide heart health tips on diet, exercise, and stress management.  
- Support for multiple languages: Respond in the language specified by the user (English, Hindi, Spanish, Telugu).  

Context: {context}  
User ({language}): {question}  
AI Response ({language} - Concise & Clear): 

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

    # Invoke the model to generate a response based on the user input and context
    result = chain.invoke({"context": context, "language": language, "question": user_input})

    # Update the context while ensuring the language is always updated
    context = f"Language: {language}\n{context}\nUser: {user_input}\nAI: {result}"

    # Return the response text and the URL to the audio file
    return jsonify({
        'text': result
    })

# Main block to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
