import requests
import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# 1. API Keys Render ke system se apne aap uthegi
API_KEY = os.environ.get("GEMINI_API_KEY")
BOT_TOKEN = "8896347343:AAGgQkLDpLx8mJe4zEqD5Csyqdg-VFJuvs8"

# Gemini 2.5 Flash ka sahi URL
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        update = request.get_json()
        
        if "message" in update and "text" in update["message"]:
            chat_id = update["message"]["chat"]["id"]
            user_text = update["message"]["text"]
            
            # Dhasu instruction bina loop ke directly chalne ke liye
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"You are ANKIT-AI, an advanced AI system created by Ankit Yadav. Respond warmly like a close brother in Hindi/Hinglish. Never repeat 'Hello Ankit'. Answer this query directly: {user_text}"
                    }]
                }]
            }
            
            headers = {'Content-Type': 'application/json'}
            
            try:
                response = requests.post(URL, json=payload, headers=headers)
                res_data = response.json()
                
                if response.status_code == 200:
                    bot_reply = res_data['candidates'][0]['content']['parts'][0]['text']
                else:
                    bot_reply = "Bhai thoda server load hai, 1 minute baad try karo!"
                
                # Telegram par wapass reply bhej rahe hain (Corrected spelling here)
                tele_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                requests.post(tele_url, json={"chat_id": chat_id, "text": bot_reply})
                
            except Exception as e:
                pass
                
        return jsonify({"status": "success"})
    return "Ankit-AI 2.5 Backend is Running Live!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
