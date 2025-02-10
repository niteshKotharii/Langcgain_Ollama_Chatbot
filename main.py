from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn 
import asyncio

# Template for the model's response
template = """
You are a friendly, caring, and empathetic heart health assistant developed by Metafied.  
Your role is to provide clear, concise, and actionable heart health advice, including symptoms, medical guidance, dietary tips, and lifestyle recommendations.  

Guidelines:  
- Keep responses brief (1-2 sentences), focusing on clarity, medications, diet, and actionability.  
- If the user mentions any heart-related symptoms, provide suitable lifestyle changes, medications, or dietary adjustments to help manage them.  
- If the user asks about an unrelated topic, respond briefly and then gently steer the conversation back to heart health in a natural way.
- Always provide helpful guidance without stating that medical advice cannot be given. Instead, offer general recommendations and suggest when medical attention may be necessary.  
- Support for multiple languages: Respond in the language specified by the user (English, Hindi, Spanish, Telugu).  

Context: {context}  
User ({language}): {question}  
AI Response ({language} - Concise & Clear):  

"""

# Initialize the FastAPI app
app = FastAPI()

# Initialize the model and the chat prompt template
model = OllamaLLM(model="llama3.2", temperature=0.7, max_tokens=30)
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Initialize the context variable to store the conversation history
context = "" 

# Enable CORS for the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Route to handle the chat interaction
@app.post("/chat")
async def chat(request: Request):
    global context

    # Parse the input data
    data = await request.json()
    user_input = data.get('question', '').strip().lower()
    language = data.get('language', 'en')

    if not user_input:
        raise HTTPException(status_code=400, detail="User question is required")

    # Invoke the model to generate a response based on the user input and context
    result = await asyncio.to_thread(chain.invoke, {"context": context, "language": language, "question": user_input})

    # Update the context while ensuring the language is always updated
    context = f"Language: {language}\n{context}\nUser: {user_input}\nAI: {result}"

    # Return the response text
    return JSONResponse(content={'text': result})

# Main block to run the FastAPI app
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
