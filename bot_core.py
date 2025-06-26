import os
import tweepy
import sqlite3
import time
import requests
from dotenv import load_dotenv

# Загрузка ключей
load_dotenv()

# 🔑 Twitter API
auth = tweepy.OAuth1UserHandler(
    consumer_key=os.getenv("CONSUMER_KEY"),
    consumer_secret=os.getenv("CONSUMER_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)
api = tweepy.API(auth)

# Инициализация БД
conn = sqlite3.connect('bot_dms.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS replied_users (user_id TEXT PRIMARY KEY)''')
conn.commit()

# 🔥 DeepSeek API (генерация комментариев)
def generate_comment_with_deepseek(post_text, lang="en"):
    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json"
    }
    prompt = (
        f"Write a friendly 1-sentence comment in {lang} for a social media post about: {post_text[:100]}. "
        "Use hashtags like #Creativity #SupportSmallArtists."
    )
    data = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        return f"🚀 Great post about {post_text[:20]}! #SupportCreators"  # Fallback
    except Exception as e:
        print(f"❌ DeepSeek Error: {e}")
        return "🌟 Interesting content! #KeepCreating"

# 💌 Ответ на личные сообщения
def check_and_reply_to_dms():
    try:
        dms = api.get_direct_messages(count=5)
        for dm in dms:
            sender_id = dm.message_create["sender_id"]
            cursor.execute("SELECT 1 FROM replied_users WHERE user_id=?", (sender_id,))
            if not cursor.fetchone():
                reply = "👋 Hi! I'm a promo bot for small creators! Send your post for a review!"
                api.send_direct_message(sender_id, reply)
                cursor.execute("INSERT INTO replied_users VALUES (?)", (sender_id,))
                conn.commit()
                print(f"📩 Replied to {sender_id}")
    except Exception as e:
        print(f"❌ DM Error: {e}")

# 🔍 Поиск по хэштегам + AI-комментарии
def search_and_comment(hashtag="NFT", count=3):
    try:
        tweets = api.search_tweets(q=f"#{hashtag}", result_type="recent", count=count)
        for tweet in tweets:
            if not tweet.user.following:
                api.create_friendship(tweet.user.id)  # Подписка
            comment = generate_comment_with_deepseek(tweet.text, tweet.lang)
            api.update_status(
                status=comment,
                in_reply_to_status_id=tweet.id,
                auto_populate_reply_metadata=True
            )
            print(f"💬 Commented (Language: {tweet.lang}): {comment[:50]}...")
    except Exception as e:
        print(f"❌ Search Error: {e}")

# ♻ Основной цикл
def run_bot():
    while True:
        check_and_reply_to_dms()
        search_and_comment(hashtag="NFT")  # Меняйте хэштег
        time.sleep(300)  # Пауза 5 минут

if __name__ == "__main__":
    print("🤖 Бот запущен! Для остановки: Ctrl+C")
    run_bot()
