import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# ⚠️ Yahan " " ke andar apni vahi asli sahi wali API Key dhyan se paste karo
API_KEY = "AIzaSyCy-deh-OU6ELDhTpT4rxqRMaNmQCKhrFs"
BOT_TOKEN = "8896347343:AAGgQkLDpLx8mJe4zEqD5Csyqdg-VFJuvs8"

# Google ka ekdum latest working combo (v1beta + gemini-1.5-flash)
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        update = request.get_json()
        if "message" in update and "text" in update["message"]:
            chat_id = update["message"]["chat"]["id"]
            user_text = update["message"]["text"]
            
            # Google API Request Structure
            payload = {
                "contents": [{
                    "parts": [{"text": user_text}]
                }]
            }
            headers = {"Content-Type": "application/json"}
            
            try:
                response = requests.post(URL, json=payload, headers=headers, timeout=15)
                gemini_data = response.json()
                
                # Jawab ko extract karna
                if 'candidates' in gemini_data and len(gemini_data['candidates']) > 0:
                    bot_reply = gemini_data['candidates'][0]['content']['parts'][0]['text']
                elif 'error' in gemini_data:
                    bot_reply = f"Google API Error: {gemini_data['error']['message']}"
                else:
                    bot_reply = f"System notice: {json.dumps(gemini_data)}"
                    
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
