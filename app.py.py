from flask import Flask, render_template, request
import threading
import time
from bot_core import api, search_and_comment

app = Flask(__name__)

# Главная страница с настройками
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# Запуск авто-комментирования
@app.route("/start_commenting", methods=["POST"])
def start_commenting():
    hashtag = request.form.get("hashtag")
    threading.Thread(target=search_and_comment, args=(hashtag,)).start()
    return "✅ Автокомментирование запущено!"

if __name__ == "__main__":
    app.run(debug=True)