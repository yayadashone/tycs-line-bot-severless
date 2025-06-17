from linebot import LineBotApi
from linebot.models import TextSendMessage
from google_sheet import get_all_user_ids
import os

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))

def send_push(message):
    user_ids = get_all_user_ids()
    chunks = [user_ids[i:i + 150] for i in range(0, len(user_ids), 150)]
    for chunk in chunks:
        line_bot_api.multicast(chunk, TextSendMessage(text=message))
