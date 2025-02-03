import pyttsx3
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from googletrans import Translator

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 170)  # Adjust speech rate
engine.setProperty("volume", 1)  # Adjust volume

# Initialize Translator
translator = Translator()

# Default language
current_language = "en"

template = """
You are Kokoro, a heart health assistant developed by Metafied. Your goal is to provide **brief, clear, and informative** responses related to heart health. 

Guidelines:
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

async def translate_text(text, lang):
    """Translate text to a given language asynchronously"""
    translated = await asyncio.to_thread(translator.translate, text, dest=lang)
    return translated.text

async def handle_conversation():
    global current_language  # Make the language setting persistent
    context = ""
    print("Welcome to Metafied's kokoro.doctor chatbot! Type 'exit' to quit.")
    
    while True:
        user_input = input("You: ").strip().lower()
        
        # Check if the user wants to change the language
        if user_input == "translate to hindi":
            current_language = "hi"
            print("\nBot: Responses will now be in Hindi.\n")
            continue
        elif user_input == "translate to hinglish":
            current_language = "hinglish"
            print("\nBot: Responses will now be in Hinglish.\n")
            continue
        elif user_input == "translate to english":
            current_language = "en"
            print("\nBot: Responses will now be in English.\n")
            continue
        elif user_input == "exit":
            break
        
        # Generate response in English first
        result = chain.invoke({"context": context, "question": user_input})
        
        # Translate response if needed
        if current_language == "hi":
            result = await translate_text(result, "hi")  # Convert to Hindi
        elif current_language == "hinglish":
            hindi_translation = await translate_text(result, "hi")  # Convert to Hindi first
            result = await translate_text(hindi_translation, "en")  # Convert to Hinglish
        
        print(f"\nBot ({current_language.capitalize()}): {result}\n")
        speak(result)  # Speak the response in the selected language

        context += f"\nUser: {user_input}\nAI: {result}"

if __name__ == "__main__":
    asyncio.run(handle_conversation())  # Properly handle async operations
