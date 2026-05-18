import requests
import json
import os  # System se secret key uthane ke liye
from flask import Flask, request, jsonify

app = Flask(__name__)

# 🔒 Key yahan nahi rahegi, Render automatic background se uthayega
API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = "8896347343:AAGgQkLDpLx8mJe4zEqD5Csyqdg-VFJuvs8"

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        update = request.get_json()
        if "message" in update and "text" in update["message"]:
            chat_id = update["message"]["chat"]["id"]
            user_text = update["message"]["text"]
            
            # Full Biodata in System Instruction
            payload = {
                "contents": [{
                    "parts": [{"text": user_text}]
                }],
                "systemInstruction": {
                    "parts": [{
                        "text": (
                            "Your name is Ankit-ai. You are a smart, friendly, and helpful AI assistant. "
                            "You were created and developed by Ankit Yadav. Ankit Yadav is a brilliant, "
                            "hardworking, and highly intelligent student who studies in 10th class at KRD School. "
                            "He is an innovative tech-mind who single-handedly built you. He was born on 28 December 2010. "
                            "He belongs to Uttar Pradesh, District Azamgarh, Gram Rupaipur. His family includes his mother "
                            "Rekha Yadav, his father Mukund Lal Yadav, and his supportive younger brother Monu. "
                            "Whenever anyone asks about your owner, creator, developer, or their background, personality, "
                            "school, or birthday, proudly tell them all these correct details with high respect and praise "
                            "for Ankit. Always answer in a cool, respectful, and friendly mix of Hindi and English (Hinglish)."
                        )
                    }]
                }
            }
            headers = {"Content-Type": "application/json"}
            
            try:
                response = requests.post(URL, json=payload, headers=headers, timeout=15)
                gemini_data = response.json()
                
                if 'candidates' in gemini_data and len(gemini_data['candidates']) > 0:
                    bot_reply = gemini_data['candidates'][0]['content']['parts'][0]['text']
                elif 'error' in gemini_data:
                    bot_reply = f"Google API Error: {gemini_data['error']['message']}"
                else:
                    bot_reply = f"System notice: {json.dumps(gemini_data)}"
                    
            except Exception as e:
                bot_reply = f"Server Connection error: {str(e)}"

            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            telegram_payload = {"chat_id": chat_id, "text": bot_reply}
            requests.post(telegram_url, json=telegram_payload)
            
        return jsonify({"status": "success"})
    return "<h1>Ankit AI Server is Running Live!</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
