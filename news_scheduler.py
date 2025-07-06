import os
import requests
import schedule
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
client_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_news():
    prompt = (
        "צור הודעת חדשות בפורמט הבא:\n"
        "📰 כותרת קצרה\n"
        "📡 מקור\n"
        "💡 למה זה חשוב לקהל ליברלי-דמוקרטי בישראל"
    )
    response = client_ai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "אתה כתב חדשות בעברית מזווית ליברלית-דמוקרטית"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    print("נשלח:", response.status_code)

def job():
    news = generate_news()
    send_to_telegram(news)

# תזמון אוטומטי: כל 15 דקות בין 08:00 ל־23:30
for hour in range(8, 24):
    for minute in [0, 15, 30, 45]:
        schedule_time = f"{hour:02d}:{minute:02d}"
        schedule.every().day.at(schedule_time).do(job)

print("הבוט רץ... (לסיום לחץ Ctrl+C)")
while True:
    schedule.run_pending()
    time.sleep(10)
