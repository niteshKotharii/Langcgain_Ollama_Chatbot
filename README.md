# Heart Health Chatbot ❤️  

This is a heart health assistant developed by **Metafied**. It provides **brief, clear, and informative** responses related to heart health, offering tips on diet, exercise, and lifestyle while advising immediate medical help for serious symptoms.

## 🚀 Features  
- **Concise Responses** (2-3 sentences)  
- **Heart Health Tips** on diet, exercise, and lifestyle  
- **Emergency Advice** for critical symptoms like chest pain  
- **AI-powered chatbot** using `LangChain`, `OllamaLLM`, and `Flask`  
- **Multilingual Support** – Translates responses into multiple languages  
- **Text-to-Speech (TTS) Support** – Converts responses into audio using `gTTS`  

## 🛠️ Setup  
1. Clone the repository:  
   ```bash
   git clone https://github.com/niteshKotharii/Langchain_Ollama_Chatbot.git
   ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the chatbot:
    ```bash
    python3 main.py
    ```

## 📝 Usage  
- Type your heart health queries in the chatbot.  
- The chatbot provides responses in **English** by default.
- You can specify a language preference (e.g., `hi` for Hindi, `fr` for French).
- The chatbot also generates **audio responses** in the selected language.
- Type **"exit"** to quit the conversation.  

## 📌 Supported Languages
The chatbot can provide responses in the following languages:
- English (`en`)
- Hindi (`hi`)
- French (`fr`)
- Spanish (`es`)
- German (`de`)
- Italian (`it`)
- Portuguese (`pt`)
- Chinese (`zh`)
- Japanese (`ja`)
- Korean (`ko`)
- Russian (`ru`)
- Arabic (`ar`)
- Bengali (`bn`)
- Gujarati (`gu`)
- Marathi (`mr`)
- Tamil (`ta`)
- Telugu (`te`)
- Urdu (`ur`)

## 📌 API Endpoints
### **Chat Endpoint**
**Route:** `/chat`  
**Method:** `GET`  
**Request Body (JSON):**
```json
{
    "question": "What foods are good for heart health?",
    "language": "hi"
}
```
**Response (JSON):**
```json
{
    "text": "हृदय स्वास्थ्य के लिए हरी साग, पूरी अनाज, और मछली मछली मछली मछली मछली मछली मछली मछली",
    "audio": "http://localhost:5000/response.mp3"
}
```

### **Audio File Endpoint**
**Route:** `/<filename>`  
**Method:** `GET`  
**Description:** Serves the generated audio file in MP3 format.

## 📈 Example Usage
```bash
You: What foods are good for heart health?  
Bot: Leafy greens, whole grains, and fatty fish are great for heart health.  
Bot (Audio): *Plays the response in selected language*
```

## 🤝 Contributing
Feel free to submit issues or pull requests!

