from flask import Flask, render_template, request
from threading import Thread
from bot_core import search_and_comment

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/start_bot", methods=["POST"])
def start_bot():
    hashtag = request.form.get("hashtag", "#NFT")
    Thread(target=search_and_comment, args=(hashtag,)).start()
    return f"✅ Бот запущен! Отслеживаем хэштег: {hashtag}"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)