import os
import tweepy
from dotenv import load_dotenv

load_dotenv()  # Загружаем ключи из .env

# Авторизация в Twitter
auth = tweepy.OAuth1UserHandler(
    consumer_key=os.getenv("CONSUMER_KEY"),
    consumer_secret=os.getenv("CONSUMER_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)

api = tweepy.API(auth)

# Проверка подключения
try:
    user = api.verify_credentials()
    print(f"✅ Бот авторизован как @{user.screen_name}")
except Exception as e:
    print(f"❌ Ошибка подключения: {e}")
    
    import time

def check_and_reply_to_dms():
    try:
        # Получаем последние 5 ЛС (можно увеличить)
        dms = api.get_direct_messages(count=5)  
        
        for dm in dms:
            sender_id = dm.message_create["sender_id"]
            message_text = dm.message_create["message_data"]["text"]
            
            # Проверяем, не отвечали ли уже (упрощённо)
            if not hasattr(dm, 'is_response'):  
                # Формируем ответ
                reply_message = (
                    "👋 Hi! I'm a promotion bot for small creators!\n"
                    "My mission is to help artists, NFT makers, and startups grow on X.\n\n"
                    "Want me to share your work? Send your post, and my admin will review it! 🚀"
                )
                
                # Отправляем ответ
                api.send_direct_message(sender_id, reply_message)
                print(f"📤 Replied to user {sender_id}")
                
    except Exception as e:
        print(f"❌ Error in DM reply: {e}")
        
        if __name__ == "__main__":
    while True:
        check_and_reply_to_dms()
        time.sleep(300)  # Пауза 5 минут (300 секунд)
        
        import sqlite3

# Создаём БД при первом запуске
conn = sqlite3.connect('bot_dms.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS replied_users (user_id TEXT PRIMARY KEY)''')
conn.commit()

def check_and_reply_to_dms():
    try:
        dms = api.get_direct_messages(count=5)
        for dm in dms:
            sender_id = dm.message_create["sender_id"]
            
            # Проверяем, есть ли user_id в БД
            cursor.execute("SELECT 1 FROM replied_users WHERE user_id=?", (sender_id,))
            if not cursor.fetchone():  # Если ещё не отвечали
                reply_message = "👋 Hi! I'm your friendly promo bot!..."
                api.send_direct_message(sender_id, reply_message)
                
                # Запоминаем отправителя
                cursor.execute("INSERT INTO replied_users VALUES (?)", (sender_id,))
                conn.commit()
                
    except Exception as e:
        print(f"Error: {e}")
        
        def check_dms():
    try:
        dms = api.get_direct_messages(count=5)  # Последние 5 ЛС
        for dm in dms:
            sender_id = dm.message_create["sender_id"]
            text = dm.message_create["message_data"]["text"]
            
            # Проверяем, не отвечали ли уже
            if not dm.message_create.get("is_response", False):
                reply = (
                    "Hi! 👋 I'm a promotion bot for small creators. "
                    "I help artists, NFT creators, and startups grow on X! "
                    "Want me to share your work? Send your post, and my admin will review it! 🚀"
                )
                api.send_direct_message(sender_id, reply)
                print(f"📩 Отправлен ответ пользователю {sender_id}")
    except Exception as e:
        print(f"⚠ Ошибка при проверке ЛС: {e}")

# Проверяем ЛС каждые 5 минут (в продакшене лучше через cron)
while True:
    check_dms()
    time.sleep(300)  # 5 минут
        
# ДипСик
from deepseek_api import DeepSeek  # Примерный импорт (зависит от доступного API)

deepseek = DeepSeek(api_key="7a043564893f42e59bcbdd665d4900f3")

def generate_comment(post_text, lang="en"):
    prompt = f"Write a friendly comment in {lang} for a post about: {post_text}"
    response = deepseek.generate(prompt, max_tokens=50)
    return response.choices[0].text.strip()
        
# Поиск и ответ на комменты
def search_and_comment(hashtag="NFT", count=3):
    try:
        tweets = api.search_tweets(q=f"#{hashtag}", result_type="recent", count=count)
        for tweet in tweets:
            if not tweet.user.following:  # Если ещё не подписаны
                api.create_friendship(tweet.user.id)  # Подписываемся (пункт 2)
            
            lang = tweet.lang  # Определяем язык поста
            comment = generate_comment(tweet.text, lang)
            api.update_status(
                status=comment,
                in_reply_to_status_id=tweet.id,
                auto_populate_reply_metadata=True
            )
            print(f"💬 Прокомментирован пост {tweet.id} на {lang}")
    except Exception as e:
        print(f"⚠ Ошибка: {e}")        
        
        

        
