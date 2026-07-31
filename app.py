from flask import Flask, render_template, request
import requests

app = Flask(__name__)

OPENROUTER_API_KEY = "Sk-or-v1-1a42dee56c2ec435fd0ca2b66f12074730ba774bca7bd2a2b5009cc952848cc6"

def get_aryan_response(user_message):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "google/gemini-2.5-flash", 
        "messages": [{"role": "user", "content": user_message}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()
        return response_json['choices'][0]['message']['content']
    except Exception as e:
        return "Bhai, abhi network mein thodi dikkat hai. Thodi der baad try karna."

@app.route("/", methods=["GET", "POST"])
def home():
    chat_history = []
    
    if request.method == "POST":
        user_message = request.form.get("message")
        if user_message:
            bot_reply = get_aryan_response(user_message)
            chat_history.append({"user": user_message, "bot": bot_reply})
            
    return render_template("index.html", chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
