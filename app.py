import requests
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = "AIzaSyCy-deh-OU6ELDhTpT4rxqRMaNmQCKhrFs"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
system_instruction = "You are ANKIT AI, a sharp, smart, and friendly AI assistant. Reply in natural, casual Hinglish (Hindi written in Latin script) like a close peer or brother. Keep it direct and helpful."

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>ANKIT AI</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; text-align: center; padding: 20px; margin: 0; }
            h2 { color: #38bdf8; font-weight: 600; margin-top: 30px; letter-spacing: 0.5px; }
            .chat-box { max-width: 480px; margin: 20px auto; background: #1e293b; padding: 25px; border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3); border: 1px solid #334155; }
            .input-area { display: flex; gap: 10px; margin-bottom: 20px; }
            input { flex: 1; padding: 12px 16px; border-radius: 8px; border: 1px solid #475569; font-size: 16px; background: #0f172a; color: white; outline: none; }
            input:focus { border-color: #38bdf8; }
            button { padding: 12px 20px; border: none; background: #0284c7; color: white; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: 600; }
            #reply { padding: 16px; background: #334155; border-radius: 10px; font-size: 16px; text-align: left; line-height: 1.6; white-space: pre-wrap; color: #e2e8f0; border-left: 4px solid #38bdf8; }
        </style>
    </head>
    <body>
        <h2>ANKIT AI</h2>
        <div class="chat-box">
            <div class="input-area">
                <input type="text" id="msg" placeholder="Ask anything...">
                <button onclick="askBot()">Send</button>
            </div>
            <div id="reply">Bot 🤖 : Ready bro, ask me anything...</div>
        </div>
        <script>
            async function askBot() {
                let msg = document.getElementById('msg').value;
                let replyDiv = document.getElementById('reply');
                if(!msg.trim()) return;
                replyDiv.innerHTML = "Bot 🤖 : Thinking...";
                let res = await fetch('/chat?q=' + encodeURIComponent(msg));
                let data = await res.json();
                replyDiv.innerHTML = "Bot 🤖 : " + data.reply;
                document.getElementById('msg').value = '';
            }
        </script>
    </body>
    </html>
    '''

@app.route('/chat')
def chat():
    user_input = request.args.get('q', '')
    payload = {
        "contents": [{"parts": [{"text": user_input}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]}
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(URL, headers=headers, data=json.dumps(payload))
        res_json = response.json()
        bot_reply = res_json['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"reply": bot_reply})
    except:
        return jsonify({"reply": "Bhai error aaya, ek baar check karo."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
