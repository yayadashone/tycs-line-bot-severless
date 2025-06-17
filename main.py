from fastapi import FastAPI, Request
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

LINE_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()
    events = body.get("events", [])
    for event in events:
        if event["type"] == "follow":
            user_id = event["source"]["userId"]
            reply_token = event["replyToken"]
            reply_message(reply_token, "歡迎加入 LINE 活動通知服務！")
    return {"status": "ok"}

def reply_message(token, text):
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "replyToken": token,
        "messages": [{"type": "text", "text": text}]
    }
    requests.post("https://api.line.me/v2/bot/message/reply", json=data, headers=headers)
