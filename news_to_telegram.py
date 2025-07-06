import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# מפתחות
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# מפתח OpenAI
client_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# הפקת עדכון חדשותי
def generate_news():
    prompt = (
        "צור הודעת חדשות בפורמט הבא:\n"
        "📰 כותרת חדשותית קצרה, אקטואלית ועדכנית\n"
        "📡 מקור (שם אתר חדשות או גוף תקשורת)\n"
        "💡 משפט אחד או שניים שמסבירים למה זה חשוב לציבור ליברלי-דמוקרטי בישראל"
    )

    response = client_ai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "אתה כתב חדשות ליברלי-דמוקרטי שמסקר חדשות בעברית."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return response.choices[0].message.content.strip()

# שליחת ההודעה לטלגרם
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    print("הודעה נשלחה:", response.status_code, response.text)

# הפעלת הבוט
if __name__ == "__main__":
    news = generate_news()
    send_to_telegram(news)
