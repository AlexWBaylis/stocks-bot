import requests
import time

TOKEN = "8645313086:AAH8JfIEpDoiNaKZ4RvkbQ4AJg8U3vP0_Ig"
CHAT_ID = "6213751254"

SEEN = set()

print("Bot started...")

def get_pairs():
    url = "https://api.dexscreener.com/latest/dex/search/?q=SOL"
    return requests.get(url).json()["pairs"]

while True:
    try:
        pairs = get_pairs()

        for pair in pairs:
            name = pair["baseToken"]["name"]
            mc = pair.get("fdv", 0)
            link = pair["url"]

            if mc and mc >= 15000 and name not in SEEN:
                SEEN.add(name)

                msg = f"{name} hit {mc}$ 🚀\n{link}"
                requests.get(
                    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                    params={"chat_id": CHAT_ID, "text": msg}
                )

        time.sleep(30)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)
FROM python:3.11

WORKDIR /app
COPY . .

RUN pip install python-telegram-bot requests

CMD ["python", "bot.py"]
