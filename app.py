from flask import Flask, render_template_string, request
import google.generativeai as genai

app = Flask(__name__)

GEMINI_API_KEY ="AQ.Ab8RN6JrZDx6hedRbpWAzcySLR2F3RFcn8CoUe2F68mYiIzBdw"

genai.configure(api_key=GEMINI_API_KEY)

# Latest supported model identifier
model = genai.GenerativeModel('gemini-2.0-flash')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aryan AI Support</title>
    <style>
        body { font-family: sans-serif; background-color: #f0f2f5; padding: 10px; margin: 0; }
        .chat-box { max-width: 100%; background: white; padding: 15px; border: 1px solid #ccc; }
        .msg { margin-bottom: 15px; padding: 10px; border-radius: 5px; word-wrap: break-word; }
        .user { background-color: #d1e7dd; border-left: 4px solid #0f5132; }
        .bot { background-color: #e2e3e5; border-left: 4px solid #41464b; }
        input[type="text"] { width: 95%; padding: 10px; margin-bottom: 10px; font-size: 16px; border: 1px solid #ccc; }
        input[type="submit"] { width: 100%; padding: 12px; background-color: #007bff; color: white; border: none; font-size: 16px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="chat-box">
        <h2 style="text-align: center; color: #333;">Aryan Support</h2>
        {% if chat_history %}
            {% for chat in chat_history %}
                <div class="msg user"><strong>Tum:</strong> {{ chat.user }}</div>
                <div class="msg bot"><strong>Aryan:</strong> {{ chat.bot }}</div>
            {% endfor %}
        {% else %}
            <p style="text-align: center; color: #666;">Namaste! Main tumhari kya madad kar sakta hoon?</p>
        {% endif %}
        <form method="POST" action="/">
            <input type="text" name="message" placeholder="Apna sawaal likho..." required>
            <br>
            <input type="submit" value="Message Bhejo">
        </form>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    chat_history = []
    
    if request.method == "POST":
        user_message = request.form.get("message")
        if user_message:
            try:
                response = model.generate_content(user_message)
                bot_reply = response.text
            except Exception as e:
                bot_reply = f"Gemini Error: {str(e)}"
                
            chat_history.append({"user": user_message, "bot": bot_reply})
            
    return render_template_string(HTML_TEMPLATE, chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
