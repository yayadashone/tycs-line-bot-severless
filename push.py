import os
import requests
from dotenv import load_dotenv

load_dotenv()

LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

headers = {
    "Authorization": f"Bearer {LINE_TOKEN}",
    "Content-Type": "application/json"
}

def send_push(user_ids, message):
    for i in range(0, len(user_ids), 500):
        data = {
            "to": user_ids[i:i+500],
            "messages": [{"type": "text", "text": message}]
        }
        r = requests.post("https://api.line.me/v2/bot/message/multicast", json=data, headers=headers)
        print(r.status_code, r.text)
