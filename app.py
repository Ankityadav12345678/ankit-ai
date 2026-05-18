import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# ⚠️ Agar tumhari kal wali API Key isse alag hai toh yahan badal dena
API_KEY = "AIzaSyCy-deh-OU6ELDhTpT4rxqRMaNmQCKhrFs"
BOT_TOKEN = "8896347343:AAGgQkLDpLx8mJe4zEqD5Csyqdg-VFJuvs8"

# Ekdum stable Google v1 API Endpoint
URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        update = request.get_json()
        if "message" in update and "text" in update["message"]:
            chat_id = update["message"]["chat"]["id"]
            user_text = update["message"]["text"]
            
            # Google AI Studio ka ekdum correct payload format
            payload = {
                "contents": [{
                    "parts": [{"text": user_text}]
                }]
            }
            headers = {"Content-Type": "application/json"}
            
            try:
                response = requests.post(URL, json=payload, headers=headers, timeout=10)
                gemini_data = response.json()
                
                # Jawab nikalne ka sahi tarika
                if 'candidates' in gemini_data and len(gemini_data['candidates']) > 0:
                    bot_reply = gemini_data['candidates'][0]['content']['parts'][0]['text']
                elif 'error' in gemini_data:
                    bot_reply = f"Google API Error: {gemini_data['error']['message']}"
                else:
                    bot_reply = f"Gemini system block: {json.dumps(gemini_data)}"
                    
            except Exception as e:
                bot_reply = f"Server Connection error: {str(e)}"

            # Telegram par answer bhejna
            telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            telegram_payload = {"chat_id": chat_id, "text": bot_reply}
            requests.post(telegram_url, json=telegram_payload)
            
        return jsonify({"status": "success"})
    return "<h1>Ankit AI Server is Running Live!</h1>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
